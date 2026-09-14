from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Sammar RAG AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_USERNAME = "AI-Engineer-Sammar"

KNOWLEDGE_BASE = {
    "name": "Sammar",
    "role": "AI Engineer & Software Developer",
    "bio": "Sammar is an AI Engineer specializing in Python, FastAPI, LangChain, LangGraph, Production RAG Architectures, Machine Learning, and Deep Learning.",
    "linkedin": "https://linkedin.com",
    "whatsapp": "+92 301 4095463",
    "whatsapp_link": "https://wa.me/923014095463",
    "github_url": f"https://github.com/{GITHUB_USERNAME}",
    "skills": [
        "Python Backend (FastAPI, Pydantic, OOP)",
        "Agentic AI & Orchestration (LangChain, LangGraph)",
        "Vector Stores & RAG (ChromaDB, Unstructured PDF Reader)",
        "Local LLMs (Ollama, Gemma 2, Qwen, Llama 3.2)",
        "Google Gemini Models Integration",
        "Frontend & 3D (React, Vite, Node.js, Three.js)"
    ]
}

class QueryRequest(BaseModel):
    query: str

def fetch_github_realtime_data():
    try:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=5"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            repos = response.json()
            return [
                {
                    "name": r.get("name"),
                    "description": r.get("description") or "No description provided",
                    "url": r.get("html_url"),
                    "language": r.get("language") or "Python/AI"
                }
                for r in repos
            ]
    except Exception as e:
        print(f"GitHub Real-Time Search Error: {e}")
    return []

# Serve Static Index HTML at Root Route
@app.get("/")
def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "index.html not found"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "engine": "FastAPI RAG Backend"}

@app.post("/api/rag")
def rag_search(payload: QueryRequest):
    query = payload.query.lower().strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query text is required.")

    if any(k in query for k in ["github", "repo", "project", "code", "work"]):
        live_repos = fetch_github_realtime_data()
        
        if live_repos:
            repos_formatted = "<br/>".join([
                f"• <b><a href='{r['url']}' target='_blank' class='text-indigo-400 underline'>{r['name']}</a></b> "
                f"({r['language']}) - {r['description']}"
                for r in live_repos
            ])
            response_text = (
                f"<b>Real-Time GitHub Search Results for {GITHUB_USERNAME}:</b><br/><br/>"
                f"{repos_formatted}<br/><br/>"
                f"View profile: <a href='{KNOWLEDGE_BASE['github_url']}' target='_blank' class='text-indigo-400 underline'>{KNOWLEDGE_BASE['github_url']}</a>"
            )
        else:
            response_text = f"Sammar's GitHub profile: <a href='{KNOWLEDGE_BASE['github_url']}' target='_blank' class='text-indigo-400 underline'>{KNOWLEDGE_BASE['github_url']}</a>"
        return {"response": response_text}

    elif any(k in query for k in ["linkedin", "social", "connect"]):
        return {"response": f"LinkedIn: <a href='{KNOWLEDGE_BASE['linkedin']}' target='_blank' class='text-blue-400 underline'>{KNOWLEDGE_BASE['linkedin']}</a>"}

    elif any(k in query for k in ["contact", "whatsapp", "phone", "hire"]):
        return {"response": f"WhatsApp: <a href='{KNOWLEDGE_BASE['whatsapp_link']}' target='_blank' class='text-emerald-400 underline'>{KNOWLEDGE_BASE['whatsapp']}</a>"}

    elif any(k in query for k in ["skill", "stack", "tool", "python", "fastapi"]):
        skills_str = "<br/>".join([f"• {s}" for s in KNOWLEDGE_BASE['skills']])
        return {"response": f"<b>Sammar's Core Skills:</b><br/>{skills_str}"}

    elif any(k in query for k in ["who", "about", "sammar"]):
        return {"response": f"<b>{KNOWLEDGE_BASE['name']}</b> - {KNOWLEDGE_BASE['role']}<br/>{KNOWLEDGE_BASE['bio']}"}

    else:
        return {"response": "I am Sammar's RAG Assistant! Ask about his live GitHub repos, skills, LinkedIn, or WhatsApp contact."}
