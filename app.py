import streamlit as st
import pypdf
import io
from google import genai # Using the new SDK
import os
import json
from openpyxl import load_workbook

st.title("Kahoot Quiz Generator")

# --- 1. Sidebar Configuration ---
st.sidebar.title("API Key")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# --- 2. Model Selection Logic (Updated for New SDK) ---
display_models = []

if api_key:
    try:
        # NEW SDK: Initialize Client to fetch models
        client = genai.Client(api_key=api_key)
        
        # Fetch models using the new client structure
        # We look for models that support 'generateContent'
        all_models = client.models.list()
        
        for m in all_models:
            # We filter for Gemini models that are likely text generators
            if "gemini" in m.name and ("flash" in m.name or "pro" in m.name):
                # Clean the name (remove "models/" prefix if present)
                clean_name = m.name.replace("models/", "")
                if clean_name not in display_models:
                    display_models.append(clean_name)

    except Exception as e:
        # Silent fail or fallback if listing fails
        pass

# Fallback defaults if list is empty
if not display_models:
    display_models = ['gemini-1.5-flash', 'gemini-1.5-pro']

# Set default selection
default_index = 0
if 'gemini-1.5-flash' in display_models:
    default_index = display_models.index('gemini-1.5-flash')

selected_model = st.sidebar.selectbox(
    "Choose a Gemini Model",
    display_models,
    index=default_index
)

# Number of questions input
num_questions = st.sidebar.number_input(
    "Number of Questions", 
    min_value=1, 
    max_value=50, 
    value=10
)

# Difficulty Level
difficulty_level = st.sidebar.selectbox(
    "Difficulty Level",
    ['Child (Very Easy & Short)', 'Easy', 'Medium', 'Hard'],
    index=2
)

# Output Language selector
selected_language = st.sidebar.selectbox(
    "Output Language",
    ['English', 'Polish', 'Spanish', 'German', 'French'],
    index=1 # Default to English
)

st.sidebar.divider()
st.sidebar.markdown("<p style='text-align: center;'>Created by Wiktor Goszczyński</p>", unsafe_allow_html=True)

# --- 3. Main Application ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    
    # Read PDF
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        st.text_area("Extracted Text", text, height=150)
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        text = ""
    
    if api_key: 
        if st.button("Generate Quiz"):
            # --- FIX STARTS HERE (New SDK Implementation) ---
            
            # 1. Initialize the Client (Replaces genai.configure)
            client = genai.Client(api_key=api_key)
            
            # Specialized instructions for Child mode
            child_mode_instructions = ""
            if "Child" in difficulty_level:
                child_mode_instructions = """
                - **CHILD MODE SPECIAL INSTRUCTIONS:**
                    - **Strict Character Limit:** Questions must be VERY short (under 60 characters).
                    - **Vocabulary:** Use simple words suitable for a 6-year-old.
                    - **Sentence Structure:** Absolutely NO complex sentences. Keep it simple.
                    - **Emojis:** Use emojis in the questions if helpful for context (e.g., "What color is the apple? 🍎").
                    - **Context:** REINFORCE: Do NOT use phrases like 'According to the text'. Questions must be direct facts.
                """
            
            prompt = f"""
            You are an expert in creating engaging quizzes. Based on the following text from a PDF document, please generate a series of {num_questions} multiple-choice quiz questions.

            **Text to analyze:**
            ---
            {text}
            ---

            **Instructions and Constraints:**
            1.  **Number of Questions:** You MUST generate exactly {num_questions} quiz questions.
            2.  **Output Language:** Generate the questions and answers strictly in {selected_language} language, regardless of the source text language.
            3.  **Analyze the text:** Read the provided text and create questions that test understanding of the key concepts.
            4.  **Difficulty Level:** Adapt the complexity of questions based on the selected '{difficulty_level}'.
            {child_mode_instructions}
            5.  **Question Context:** **CRITICAL RULE**: The questions must be self-contained contextually. STRICTLY FORBID phrases like 'Based on the text', 'According to the passage', 'As mentioned in the document', or 'In the text'. The question implies the context is known facts, not a reading comprehension test.
            6.  **Question Style:** Questions should be clear and concise.
            7.  **Character Limits:**
                - The 'question' must be a maximum of 120 characters.
                - Each answer ('answer1', 'answer2', 'answer3', 'answer4') must be a maximum of 75 characters.
            8.  **Time Limit:** The 'time_limit' must be one of the following integers: 30.
            9.  **Correct Answer:** The 'correct_answer' MUST be an integer (1, 2, 3, or 4), strictly indicating the index of the correct answer among answer1, answer2, answer3, or answer4.
            10. **Output Format:** Your final output must be a single, valid JSON array of objects. Do not include any text or formatting before or after the JSON array. Each object in the array should represent a single quiz question and must follow this exact schema:
                {{
                  "question": "What is the capital of France?",
                  "answer1": "Berlin",
                  "answer2": "Madrid",
                  "answer3": "Paris",
                  "answer4": "Rome",
                  "time_limit": 30,
                  "correct_answer": 3
                }}

            Now, generate the quiz based on the provided text.
            """
            
            with st.spinner("Generating quiz..."):
                try:
                    # 2. Generate Content using the Client (Replaces model.generate_content)
                    # Note: We pass 'model=' as an argument here
                    response = client.models.generate_content(
                        model=selected_model,
                        contents=prompt
                    )
                    
                    st.text_area("Raw AI Response", response.text, height=300) 
                    
                    # 3. Parse Response
                    json_response = response.text.strip()
                    # Remove markdown formatting if present
                    if json_response.startswith("```json"):
                        json_response = json_response[7:]
                    if json_response.endswith("```"):
                        json_response = json_response[:-3]
                        
                    quiz_data = json.loads(json_response)
                    
                    # --- NEW LOGIC: Enforce Time Limits Immediately ---
                    for q in quiz_data:
                        if "Child" in difficulty_level:
                            q["time_limit"] = 60
                        else:
                            q["time_limit"] = 30
                            
                    st.session_state.quiz_data = quiz_data

                except json.JSONDecodeError:
                    st.error("Failed to parse JSON. The AI might have included extra text.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    else:
        st.warning("Please enter your Gemini API Key in the sidebar to generate the quiz.")

# --- 4. Display and Edit Quiz (New Section) ---
if 'quiz_data' in st.session_state and st.session_state.quiz_data:
    st.subheader("Generated Quiz")
    edited_quiz_data = st.data_editor(st.session_state.quiz_data)
    st.session_state.quiz_data = edited_quiz_data

# --- 5. Download Section ---
if 'quiz_data' in st.session_state:
    st.subheader("Download Quiz")
    
    try:
        workbook = load_workbook("KahootQuizTemplate.xlsx")
        sheet = workbook.active

        start_row = 9
        for i, question_data in enumerate(st.session_state.quiz_data):
            row = start_row + i
            sheet[f"A{row}"] = i + 1  
            sheet[f"B{row}"] = question_data.get("question", "")
            sheet[f"C{row}"] = question_data.get("answer1", "")
            sheet[f"D{row}"] = question_data.get("answer2", "")
            sheet[f"E{row}"] = question_data.get("answer3", "")
            sheet[f"F{row}"] = question_data.get("answer4", "")
            sheet[f"G{row}"] = question_data.get("time_limit", 30)
            sheet[f"H{row}"] = question_data.get("correct_answer", 1)

        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)
        excel_buffer.seek(0)

        st.download_button(
            label="Download Kahoot Quiz (.xlsx)",
            data=excel_buffer,
            file_name="kahoot_quiz.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except FileNotFoundError:
        st.error("KahootQuizTemplate.xlsx not found.")
    except Exception as e:
        st.error(f"Excel Error: {e}")