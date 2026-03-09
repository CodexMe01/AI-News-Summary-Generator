# AI News Summarizer

An intelligent, agentic AI application built using **LangGraph**, **LangChain**, and **Streamlit** to fetch, analyze, and summarize the latest Artificial Intelligence news based on a specific timeframe (Daily, Weekly, or Monthly).

## 🌟 Features

- **Agentic AI Workflow:** Orchestrates complex reasoning and tasks utilizing a node-based architecture provided by LangGraph.
- **Real-Time Web Search:** Uses the **Tavily Search API** to scour the web for the most current and relevant AI articles and trends.
- **Advanced Summarization:** Integrates high-performance **Groq LLMs** for fast, high-quality, and intelligent summarization of search results.
- **Interactive UI:** A minimal and responsive **Streamlit** interface that enables users to easily configure APIs, select LLM models, and query news.
- **Automated Reporting:** Generates markdown files for Daily, Weekly, and Monthly summaries (saved in the `AINews/` directory).

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web-based interactive UI.
- **LangChain & LangGraph**: Agentic workflow definition, integration, and state management.
- **Groq**: Fast language model inference (via `langchain-groq`).
- **Tavily API**: Web search capabilities (via `tavily-python`).
- **FAISS**: Vector-based operations (`faiss-cpu`).

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd AI-News-Summerizer
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Configure the application in the UI:**
   - In the sidebar, select the LLM provider (e.g., Groq) and your preferred model.
   - Enter your **Groq API Key**.
   - Under "Select Usecases", choose **AI News**.
   - Enter your **Tavily API Key**.

3. **Fetch News:**
   - Use the **AI News Explorer** to choose a time frame: **Daily**, **Weekly**, or **Monthly**.
   - Click **Fetch Latest News** or enter a custom prompt in the chat input.

## 🔑 Required API Keys

To run this application, you will need to provision active API keys for the following services (you can input these directly into the Streamlit UI):
- [Groq API Key](https://console.groq.com/keys)
- [Tavily API Key](https://app.tavily.com/home)

## 📂 Project Structure

```text
AI-News-Summerizer/
├── app.py                   # Entry point for the Streamlit application
├── requirements.txt         # Project dependencies
├── AINews/                  # Generated markdown summaries (daily, weekly, monthly)
├── scripts/                 # Additional scripts and utilities
└── src/                     # Core application source code
    └── langgraphagenticai/
        ├── LLMS/            # LLM configuration (Groq)
        ├── graph/           # LangGraph setup and building logic
        ├── nodes/           # Graph nodes configuration
        ├── state/           # Application state management
        ├── tools/           # External tool integrations (e.g., Tavily Search)
        └── ui/              # Streamlit UI configuration and components
```
