# Personalized News Digest

🚀 **Live Demo:** [Hugging Face Space](https://huggingface.co/spaces/arnavthak/Personalized_News_Digest)

## Overview
Personalized News Digest is an **AI-powered news summarization and delivery system**.  
It automatically gathers the latest news, filters it based on your interests, and sends you a **personalized daily news digest** directly to your email.

The project uses:
- **Gradio** for a simple frontend
- **Python (venv)** for backend workflows
- **ChromaDB** for vectorized semantic search
- **OpenAI Agents SDK** for orchestrating news retrieval, summarization, and email generation
- **NewsAPI** for fetching daily news headlines
- **SendGrid** (or email integration) for sending personalized HTML emails

---

## Features
- 🔹 Collects **up-to-date news daily** using NewsAPI  
- 🔹 Stores headlines in a **ChromaDB vector database** (vectorized & ready for semantic search)  
- 🔹 Uses an **agentic AI workflow** to:
  1. **Semantic Search:** Match your preferences with relevant news headlines  
  2. **Article Fetching:** Retrieve full articles from URLs via an MCP server  
  3. **Digest Writing:** Summarize selected articles into a **markdown-formatted digest**  
  4. **Email Generation:** Convert markdown into an **HTML email** and send it to you  

---

## How to Run Locally
1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/PersonalizedNewsDigest.git
   cd PersonalizedNewsDigest
2. Activate the Python virtual environment
   ```bash
   source venv/bin/activate   # Mac/Linux
   .\venv\Scripts\activate    # Windows
3. Start the app
   ```bash
   cd workflow
   python3 app.py

---

## Usage
- Open the Gradio interface  
- Enter:
  - **Your email address**
  - **A short paragraph describing your news preferences**  
- The system will:
  - Collect and process relevant news
  - Summarize it into a personalized digest
  - Email it to your inbox 📩 (check your spam folder for the email)

---

## Tech Stack
- **Python** (async workflows)  
- **Gradio** (frontend)  
- **ChromaDB** (vector DB for semantic search)  
- **OpenAI Agents SDK** (orchestration of search, summarization, and email generation)  
- **MCP Server** (fetching full articles from URLs)  
- **NewsAPI** (news source)  
- **SendGrid** (email delivery)

---

## License
This project is licensed under the **MIT License**.  
Feel free to fork, modify, and build upon it.
