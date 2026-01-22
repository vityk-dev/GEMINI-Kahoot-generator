# Project Specification: PDF to Kahoot Converter

## 1. Project Overview
A web-based tool that allows users to upload a slide deck (PDF format, exported from PowerPoint), processes the visual and textual content using Google Gemini 1.5 Pro, and automatically generates a quiz file compatible with Kahoot's import format.

## 2. Tech Stack & Dependencies
- **Language:** Python 3.10+
- **Frontend/App Framework:** Streamlit
- **AI Model:** Google Gemini 1.5 Pro (via `google-generativeai` SDK)
- **Data Processing:** Pandas, OpenPyXL
- **Environment Management:** `python-dotenv` (for local dev)

## 3. Architecture Flow
1. **User Input:** Upload PDF file via Streamlit `file_uploader`.
2. **Preprocessing:** Save file to temporary local path (required by Gemini API).
3. **AI Processing:** - Upload file to Gemini File API (`genai.upload_file`).
   - Wait for state `ACTIVE`.
   - Send prompt with strict JSON schema requirements.
4. **Post-Processing:**
   - Parse JSON response into a Pandas DataFrame.
   - Enforce Kahoot character limits (truncate if necessary).
   - Rename columns to match Kahoot's official template.
5. **Output:** Provide a downloadable `.xlsx` (Excel) file.

## 4. Kahoot Strict Constraints (Critical)
The generated output **MUST** adhere to these limits to ensure successful import into Kahoot:
- **Question:** Max 120 characters.
- **Answers (1-4):** Max 75 characters.
- **Time Limit:** Integer (standard values: 10, 20, 30, 60).
- **Correct Answer:** Integer (1, 2, 3, or 4).

## 5. Data Structure (Target Schema)
The AI should be prompted to return a JSON array of objects. 
**Pandas Transformation Mapping:**
| JSON Key | Kahoot Excel Header |
| :--- | :--- |
| `question` | `Question - max 120 char` |
| `answer1` | `Answer 1 - max 75 char` |
| `answer2` | `Answer 2 - max 75 char` |
| `answer3` | `Answer 3 - max 75 char` |
| `answer4` | `Answer 4 - max 75 char` |
| `time_limit` | `Time Limit` |
| `correct_answer`| `Correct Answer` |

## 6. Security Guidelines
- **NEVER** hardcode API keys.
- **Method:** Use `st.secrets["GEMINI_API_KEY"]` for Cloud deployment and `os.getenv("GEMINI_API_KEY")` for local development.
- **Git Ignore:** Ensure `.env`, `*.pdf`, and `.streamlit/secrets.toml` are in `.gitignore`.

## 7. Implementation Roadmap
1. **Setup:** Initialize `app.py` and `requirements.txt`.
2. **UI:** Create the sidebar for API key input and the main file uploader.
3. **Backend:** Implement `get_quiz_from_gemini(file_path)` function.
4. **Validation:** Add error handling for API quotas and file parsing errors.
5. **Export:** Implement `to_excel` conversion using a buffer (BytesIO).

## 8. Prompt Engineering Strategy
Use a System Instruction or specialized prompt that emphasizes:
- "Visual analysis of charts/diagrams on the slides."
- "Creating challenging, higher-order thinking questions."
- "Strict adherence to JSON output for programmatic parsing."