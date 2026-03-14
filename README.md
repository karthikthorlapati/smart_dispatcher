# LLM-Powered Prompt Router for Intent Classification

## Project Overview
This project implements a sophisticated **Intent-Based Routing** system. Instead of using a single, monolithic prompt to handle all user queries, this service acts as a "Smart Dispatcher." It first classifies the user's intent using a fast LLM call and then routes the request to a specialized "Expert Persona" for the final response.

This architecture ensures high-quality, specialized responses while keeping costs low and responses focused.

---

## 📂 Project Structure

| File | Purpose | Key Responsibility |
| :--- | :--- | :--- |
| `main.py` | **Entry Point** | Runs the 15-message test suite and handles initial environment checks. |
| `router.py` | **Orchestration** | Manages classification, routing logic, and the Groq API client calls. |
| `prompts.py` | **Configuration** | Stores the 4 Expert Personas and the Classifier system prompt. |
| `.env` | **Security** | Contains the `GROQ_API_KEY` (Not committed to version control). |
| `route_log.jsonl` | **Observability** | An append-only log recording every request for auditing and debugging. |
| `Dockerfile` | **Portability** | Defines the Python 3.11-slim environment for containerization. |
| `docker-compose.yml` | **Deployment** | Handles volume mapping and environment variable injection for Docker. |

---

## 🧠 Technical Design Decisions

* **Groq Llama-3-70b Integration:** Chosen for ultra-fast inference. Since the system requires two LLM calls (Classify + Respond), Groq ensures the total latency remains sub-second.
* **Structured Output (JSON Mode):** The classifier is programmed to return a strict JSON object. This allows the backend to programmatically extract the `intent` and `confidence` without fragile string parsing.
* **Persona Decoupling:** Expert prompts are separated from the logic. This makes the system "pluggable"—new specialized experts can be added simply by updating the `EXPERT_PROMPTS` dictionary.
* **Confidence Thresholding:** If the classifier's confidence is below **0.7** or the intent is **unclear**, the system defaults to a clarifying question rather than guessing, preventing AI hallucinations.

---

## 🚀 Setup & Execution

### Prerequisites
* Docker and Docker Compose installed.
* A Groq API Key (get one at [console.groq.com](https://console.groq.com/)).

### Environment Setup
1. Create a `.env` file in the root directory.
2. Add your key: `GROQ_API_KEY=your_key_here`

### Running with Docker (Recommended)
```bash
docker-compose up --build