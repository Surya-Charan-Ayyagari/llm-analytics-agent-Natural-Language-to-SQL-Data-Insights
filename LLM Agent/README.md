# 🤖 LLM Analytics Agent  
### *AI-powered Data Analysis using Natural Language, SQL, and OpenAI GPT-4o-mini*

---

## 📘 Overview  
The **LLM Analytics Agent** is an AI-driven data analytics assistant that converts natural language questions into SQL queries, executes them on a PostgreSQL database, visualizes the results, and summarizes insights automatically.  

It bridges the gap between **business users and data analysts**, enabling self-service analytics and automated insight generation — powered by **OpenAI’s GPT-4o-mini** and an intuitive **Streamlit** interface.

---

## 🧠 Features
✅ Convert plain English questions into safe, optimized SQL queries  
✅ Execute SQL queries on PostgreSQL (Neon, Supabase, or local)  
✅ Generate charts (Matplotlib) for instant visualization  
✅ Summarize insights automatically using GPT-4o-mini  
✅ Built-in guardrails to prevent unsafe SQL (no DML/DDL)

---

## ⚙️ Tech Stack
| Layer | Tools & Technologies |
|-------|----------------------|
| **Frontend (UI)** | Streamlit |
| **Database** | PostgreSQL (Neon) |
| **AI/LLM Engine** | OpenAI GPT-4o-mini |
| **Data Processing** | Python, Pandas, SQLAlchemy |
| **Visualization** | Matplotlib |
| **Environment** | dotenv, virtualenv |

---

## 🚀 Quick Start

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Surya-Charan-Ayyagari/llm-analytics-agent-Natural-Language-to-SQL-Data-Insights.git
cd 'LLM Agent'
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure your environment
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-...
LLM_BACKEND=openai
LLM_MODEL=gpt-4o-mini
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname?sslmode=require
```

### 5️⃣ Load sample schema & data
```bash
python -c "import os,sqlalchemy as sa;from dotenv import load_dotenv;load_dotenv();eng=sa.create_engine(os.getenv('DATABASE_URL'));eng.exec_driver_sql(open('schema.sql').read())"
```

### 6️⃣ Run the Streamlit app
```bash
streamlit run app_streamlit.py
```

---

## 🧩 Example Use Case
Ask questions like:
> “Show me monthly revenue by region for 2024.”  
> “List the top 5 products by sales volume.”  
> “Compare West vs Midwest revenue growth.”  

The agent will:
1. Generate an SQL query  
2. Run it safely on your database  
3. Plot the results  
4. Provide a natural language summary  

---

## 📊 Example Output
| Region | Revenue ($) |
|---------|-------------|
| West | 82,500 |
| Midwest | 79,300 |
| South | 60,200 |
| East | 58,900 |

*(Chart + summary generated automatically)*

---

## 🧱 Architecture Overview
```text
User → Streamlit UI
       ↓
    LLM Planner (GPT-4o-mini)
       ↓
   SQL Validator & Runner (Postgres)
       ↓
  Pandas + Matplotlib → Chart + Insights
```

---

## 🔒 Safety & Guardrails
- Only executes `SELECT` statements  
- Blocks dangerous keywords (`UPDATE`, `DELETE`, `DROP`, etc.)  
- Read-only DB connections  
- Schema introspection ensures LLM sees only allowed columns  

---

## 🧑‍💻 Author
**Surya Charan Ayyagari**  
🎓 Master’s in Data Analytics
💼 Data Analyst | Python | SQL | Power BI | AI Enthusiast  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/surya-charan-ayyagari/)

---

## 🪪 License
This project is licensed under the **MIT License** – free to use and modify with attribution.

---

## ⭐ Acknowledgments
Special thanks to the OpenAI, Streamlit, and PostgreSQL communities for enabling powerful open-source data and AI tools.  

If you find this project useful, ⭐ **star the repo** and share it with fellow data & AI enthusiasts!
