# Kahoot Quiz Architect ✨

> Transform your PDFs into engaging Kahoot quizzes with the power of Google Gemini AI!

## About 📄

Kahoot Quiz Architect is a cutting-edge web application built with Streamlit that streamlines the quiz creation process. Simply upload your PDF documents, and let the integrated Google Gemini 1.5 Pro AI analyze the content, generate intelligent multiple-choice questions, and prepare them in a Kahoot-ready Excel format. Perfect for educators, trainers, and anyone looking to quickly create interactive learning experiences.

## Key Features 🚀

*   **PDF Content Extraction**: Seamlessly extracts text from your uploaded PDF documents.
*   **AI Question Generation**: Leverages Google Gemini 1.5 Pro to intelligently generate quiz questions and answers.
*   **Customizable Questions**: Specify the exact number of questions you want the AI to generate.
*   **Multi-language Output**: Choose your desired quiz output language (English, Polish, Spanish, German, French), irrespective of the source PDF's language.
*   **Editable Quiz Table**: Review and refine AI-generated questions and answers directly within an interactive table before export.
*   **Kahoot-Ready Excel Export**: Download your finalized quiz in a `.xlsx` format, perfectly structured for direct import into Kahoot.
*   **Secure API Handling**: Integrates securely with the Gemini API Key, keeping your credentials safe.

## Tech Stack 🛠️

*   <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white">
*   <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit&logoColor=white">
*   <img alt="Google Gemini" src="https://img.shields.io/badge/Google_Gemini-1.5_Pro-green?style=for-the-badge&logo=google&logoColor=white">
*   `pypdf`
*   `openpyxl`
*   `python-dotenv`
*   `pandas`

## Getting Started 🏁

Follow these steps to get your Kahoot Quiz Architect up and running locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/kahoot-quiz-architect.git
    cd kahoot-quiz-architect
    ```
2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` contains `google-generativeai` which is the correct package name for `Google GenAI SDK`)*
3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    This will open the application in your web browser.

**Important:** You will need your own Google Gemini API Key. Obtain one from the [Google AI Studio](https://ai.google.dev/). Enter this key into the sidebar of the application to enable AI functionalities. For local development, you can use `.env` files, and for Streamlit Cloud, utilize `st.secrets`.

## Live Demo 🌐

A live demo of this application will be available soon on Streamlit Community Cloud!

[Live Demo Link (Coming Soon!)](https://kahoot-quiz-architect.streamlit.app/)

## Author ✍️

Created by Wiktor Goszczyński
