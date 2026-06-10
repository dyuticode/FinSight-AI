💰 FinSight AI

An AI-powered Personal Finance Advisor that transforms bank statements into actionable financial insights using Machine Learning, Forecasting, and Generative AI.

🚀 Features
📂 Upload PDF or CSV bank statements
🏷️ Automatic expense categorization
📊 Interactive spending analytics dashboard
🚨 Unusual expense detection using Machine Learning
📈 Future spending forecasts
🤖 AI-powered savings recommendations
💬 Chat with your financial data using natural language
📄 Export financial summaries and reports
🛠️ Tech Stack
Frontend: Streamlit
Data Processing: Pandas, NumPy
Visualization: Plotly
Machine Learning: Scikit-Learn
Forecasting: Prophet
LLM: Google Gemini
PDF Parsing: pdfplumber
Database: SQLite
📂 Project Structure
FinSight-AI/
│
├── app.py
├── requirements.txt
├── .env
│
├── uploads/
├── data/
├── models/
│
└── utils/
    ├── parser.py
    ├── categorizer.py
    ├── analyzer.py
    ├── forecasting.py
    └── ai_advisor.py
⚙️ Installation
git clone https://github.com/yourusername/FinSight-AI.git

cd FinSight-AI

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
🔑 Environment Setup

Create a .env file in the project root:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
▶️ Run the Application
streamlit run app.py

Open:

http://localhost:8501
📊 Example Workflow
Upload a bank statement.
Transactions are extracted and categorized.
Dashboard displays spending insights.
ML model detects anomalies.
Forecasting predicts future expenses.
AI advisor generates personalized savings recommendations.
🎯 Future Enhancements
OCR for scanned statements
Multi-bank support
Voice assistant
Financial health score
RAG-based finance chatbot
WhatsApp/Email alerts
📜 License

MIT License

⭐ FinSight AI — Turning Financial Data into Intelligent Decisions.
