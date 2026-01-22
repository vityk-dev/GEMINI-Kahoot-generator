import streamlit as st
import pypdf
import io
import google.genai as genai
import os
import json

st.title("Kahoot Quiz Generator")

# Add a section for API Key instructions
st.sidebar.title("API Key Configuration")
st.sidebar.info(
    "Please set your Gemini API Key as an environment variable named `GEMINI_API_KEY` "
    "or use Streamlit's secrets management (`.streamlit/secrets.toml`).\n\n"
    "Example for local environment variable:\n"
    "`export GEMINI_API_KEY='YOUR_API_KEY'`"
)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    st.text_area("Extracted Text", text, height=150)
    
    # Check if API Key is available from environment or secrets
    # The genai library will automatically pick it up if set correctly.
    # We still need to check if it's there before attempting to generate.
    if os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY"):
        if st.button("Generate Quiz"):
            # genai.configure(api_key=api_key) # This line caused AttributeError
            # The API key should be picked up automatically from the environment or st.secrets
            
            model = genai.GenerativeModel('models/gemini-2.5-pro')
            
            prompt = f"""
            You are an expert in creating engaging quizzes. Based on the following text from a PDF document, please generate a series of 5-10 multiple-choice quiz questions.

            **Text to analyze:**
            ---
            {text}
            ---

            **Instructions and Constraints:**
            1.  **Analyze the text:** Read the provided text and create questions that test understanding of the key concepts.
            2.  **Question Style:** Questions should be clear and concise.
            3.  **Character Limits:**
                - The 'question' must be a maximum of 120 characters.
                - Each answer ('answer1', 'answer2', 'answer3', 'answer4') must be a maximum of 75 characters.
            4.  **Time Limit:** The 'time_limit' must be one of the following integers: 10, 20, 30, 60.
            5.  **Correct Answer:** The 'correct_answer' MUST be an integer (1, 2, 3, or 4), strictly indicating the index of the correct answer among answer1, answer2, answer3, or answer4.
            6.  **Output Format:** Your final output must be a single, valid JSON array of objects. Do not include any text or formatting before or after the JSON array. Each object in the array should represent a single quiz question and must follow this exact schema:
                {{
                  "question": "Your question here",
                  "answer1": "First possible answer",
                  "answer2": "Second possible answer",
                  "answer3": "Third possible answer",
                  "answer4": "Fourth possible answer",
                  "time_limit": 20,
                  "correct_answer": 1
                }}

            **Example Output:**
            [
              {{
                "question": "What is the capital of France?",
                "answer1": "Berlin",
                "answer2": "Madrid",
                "answer3": "Paris",
                "answer4": "Rome",
                "time_limit": 20,
                "correct_answer": 3
              }}
            ]

            Now, generate the quiz based on the provided text.
            """
            
            with st.spinner("Generating quiz..."):
                response = model.generate_content(prompt)
                
                st.text_area("Raw AI Response", response.text, height=300) # Temporary for debugging
                
                try:
                    # Clean the response to get only the JSON part
                    json_response = response.text.strip().replace("```json", "").replace("```", "")
                    quiz_data = json.loads(json_response)
                    
                    st.subheader("Generated Quiz")
                    st.table(quiz_data)
                    
                    # Store the generated data in the session state for later download
                    st.session_state.quiz_data = quiz_data

                except json.JSONDecodeError:
                    st.error("Failed to parse the quiz data from the AI's response. The response was not valid JSON.")
                    st.text_area("Raw Response from AI (for review)", response.text) # Keep raw for failed parsing
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    st.text_area("Raw Response from AI (for review)", response.text) # Keep raw for unexpected errors

    else:
        st.warning("Please enter your Gemini API Key in the sidebar to generate the quiz.")

# Add a download button (it will be enabled once the quiz is generated)
if 'quiz_data' in st.session_state:
    st.subheader("Download Quiz")
    
    # Use openpyxl to create the Excel file
    from openpyxl import load_workbook
    import io

    # Load the template
    try:
        workbook = load_workbook("KahootQuizTemplate.xlsx")
        sheet = workbook.active

        # Start writing from row 9 (index 8), as per the spec
        start_row = 9
        for i, question_data in enumerate(st.session_state.quiz_data):
            row = start_row + i
            sheet[f"A{row}"] = question_data.get("question", "")
            sheet[f"B{row}"] = question_data.get("answer1", "")
            sheet[f"C{row}"] = question_data.get("answer2", "")
            sheet[f"D{row}"] = question_data.get("answer3", "")
            sheet[f"E{row}"] = question_data.get("answer4", "")
            sheet[f"F{row}"] = question_data.get("time_limit", 20)
            sheet[f"G{row}"] = question_data.get("correct_answer", 1)

        # Save the workbook to a BytesIO object
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
        st.error("KahootQuizTemplate.xlsx not found. Please make sure the template file is in the same directory as the app.")
    except Exception as e:
        st.error(f"An error occurred while creating the Excel file: {e}")

