# 🔬 Deep Research AI Agent

An automated AI research assistant built with **LangChain**, **Groq (Llama 3)**, and **DuckDuckGo**. The agent performs in-depth web research on any given topic, synthesizes the findings, and generates a structured, professional, and downloadable PDF report.

## ✨ Features

- **Multi-Agent Pipeline**: 
  - **Researcher**: Searches the web using DuckDuckGo to gather facts, stats, and expert opinions.
  - **Summarizer**: Organizes raw research findings into clean, structured summaries.
  - **Presenter**: Synthesizes the summarized data into a professional research report.
- **Configurable Research**: Adjust the breadth (number of sub-queries) and depth (number of search rounds per query) directly from the UI.
- **Fast & Free**: Uses Groq's high-speed inference for Llama 3.3 70B and DuckDuckGo for zero-cost web search.
- **Export to PDF**: Generate and download a beautifully formatted PDF version of the final report, powered by ReportLab.
- **Interactive UI**: Clean, responsive interface built with Streamlit.

## 🛠️ Tech Stack

- **LLM**: [Groq](https://groq.com/) / Llama 3.3 70B
- **Framework**: [LangChain](https://www.langchain.com/)
- **Search**: DuckDuckGo
- **Frontend**: [Streamlit](https://streamlit.io/)
- **PDF Generation**: [ReportLab](https://www.reportlab.com/)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A free API key from [Groq](https://console.groq.com/keys)

### Installation

1. **Clone the repository (or download the files)**:
   ```bash
   git clone <repository_url>
   cd DRAA
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the App

Start the Streamlit server:
```bash
streamlit run app.py
```

The app will open automatically in your default web browser at `http://localhost:8501`.

## 📁 Project Structure

- `app.py`: The main Streamlit UI and app entry point.
- `chains.py`: Contains the LangChain setup, agent initialization, and the multi-step research pipeline.
- `tools.py`: Defines the DuckDuckGo web search tool used by the Researcher agent.
- `report.py`: Handles the conversion of the final markdown report into a downloadable PDF format using ReportLab.
- `.env`: Stores environment variables (e.g., API keys).

## 💡 How It Works

1. **Input**: Enter a topic you want to research (e.g., "Impact of AI on healthcare in 2025").
2. **Research**: The application generates diverse sub-queries and fetches up-to-date search results from the web.
3. **Summarization**: Findings are grouped, de-duplicated, and summarized logically.
4. **Presentation**: A comprehensive, multi-section report is generated.
5. **Download**: Read the report on the screen or download it as a styled PDF.

## 📄 License

This project is open-source and available for personal or educational use.
