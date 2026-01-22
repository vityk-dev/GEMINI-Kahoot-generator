# Kahoot Quiz Architect ✨

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gemini-kahoot.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Gemini_1.5-8E75B2?logo=google&logoColor=white)

> **Transform your PDF study materials into engaging Kahoot games in seconds using Google Gemini AI.**

---

## 📖 About

**Kahoot Quiz Architect** is a modern web application designed for educators, students, and trainers. It streamlines the tedious process of creating quizzes by automating the extraction of knowledge from PDFs and formatting it into ready-to-play Kahoot games.

Powered by the **Google GenAI SDK** and **Gemini 1.5 models**, this tool ensures high-quality, context-aware questions in multiple languages.

## 🚀 Key Features

* **📄 Instant PDF Extraction**: Drag and drop your textbooks, slide decks, or notes to instantly extract text content.
* **🧠 Intelligent AI Generation**: Uses **Gemini 1.5 Flash** (for speed) or **Pro** (for depth) to craft relevant multiple-choice questions.
* **🌍 Multi-Language Support**: Generate quizzes in **English, Polish, Spanish, German, or French**, regardless of the source PDF's language.
* **✏️ Interactive Quiz Editor**: Review the AI-generated questions in a spreadsheet-like editor. Fix typos, adjust time limits, or change answers *before* downloading.
* **🔢 Customizable Scope**: You decide the length of the quiz (from 1 to 50 questions).
* **⚡️ Kahoot-Ready Export**: One-click download of an `.xlsx` file formatted specifically for Kahoot's "Import from spreadsheet" feature.
* **🔒 Privacy First**: Your API Key is used strictly for the session and is never stored.

## 🛠️ Tech Stack

* **Framework**: [Streamlit](https://streamlit.io/)
* **AI Model**: Google Gemini 1.5 (via `google-genai` SDK)
* **PDF Processing**: `pypdf`
* **Data Handling**: `pandas` & `openpyxl`
* **Deployment**: Streamlit Community Cloud

## 🏁 Getting Started

### Prerequisites
* Python 3.10 or higher.
* A **Google Gemini API Key** (Get it free at [Google AI Studio](https://aistudio.google.com/)).

### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/vityk-dev/GEMINI-Kahoot-generator.git](https://github.com/vityk-dev/GEMINI-Kahoot-generator.git)
    cd GEMINI-Kahoot-generator
    ```

2.  **Install Dependencies**
    We recommend using **uv** for lightning-fast setup, but standard pip works fine.

    **Option A: Using uv (Fast ⚡️)**
    ```bash
    pip install uv
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -r requirements.txt
    ```

    **Option B: Standard pip**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Check for Template**
    Ensure the file `KahootQuizTemplate.xlsx` is present in the main project folder. This is required for the Excel export to work.

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 💡 How to Use

1.  **Enter Credentials**: Paste your Gemini API Key in the sidebar.
2.  **Configure**:
    * Select a Model (Flash is faster, Pro is smarter).
    * Choose the **Output Language** (e.g., Polish).
    * Set the desired **Number of Questions**.
3.  **Upload**: Upload your PDF file.
4.  **Generate**: Click the **Generate Quiz** button.
5.  **Review**: Use the table editor to tweak any questions if needed.
6.  **Download**: Click **Download Kahoot Quiz** to save the Excel file.
7.  **Play**: Go to [create.kahoot.it](https://create.kahoot.it/), create a new Kahoot, and select **"Add question" -> "Import from spreadsheet"**.

## 🌐 Live Demo

You can try the application without installing anything here:

[👉 **Launch Kahoot Quiz Architect**](https://gemini-kahoot.streamlit.app/)

## ✍️ Author

Created by **Wiktor Goszczyński**
