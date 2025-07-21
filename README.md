
# 🩺 Doctor-Agent — LLM-Powered Appointment & Reporting System

This is a full-stack AI assistant that enables patients to book doctor appointments using natural language, and allows doctors to receive smart reports about schedules and past visits. It integrates LLMs, Google Calendar, email, and a PostgreSQL backend, all powered by FastAPI, React, and Docker.

---

## 📁 Folder Structure
```
doctor-agent/
├── backend/            # FastAPI backend with LLM tool registry (MCP)
├── frontend/           # React frontend (minimal UI for demo)
├── docker-compose.yml  # Orchestrates backend, database, and seed
```

---

## 🚀 Features

### ✅ Patient Flow
- Book appointments using natural language
- Backend uses MCP tools to check availability, confirm slots, and schedule
- Events auto-created in Google Calendar
- Email confirmation sent to patient

### ✅ Doctor Flow
- View stats like:
  - How many appointments today/yesterday
  - How many patients with specific symptoms
- Triggered via prompt or frontend button

---

## 🧠 Architecture

| Layer       | Tech                          |
|------------|-------------------------------|
| Frontend    | React + Vite                  |
| Backend     | FastAPI + MCP architecture    |
| LLM         | Integrated via langchain + Groq API |
| DB          | PostgreSQL                    |
| External APIs | Google Calendar, Gmail (SMTP) |
| DevOps      | Docker + Docker Compose       |

---

## ⚙️ Backend Setup

The backend uses FastAPI with modular MCP tool routers.

**MCP Tools Implemented:**
- `/mcp/tool/check_availability`
- `/mcp/tool/schedule_appointment`
- `/mcp/tool/doctor_summary`

Each tool is discoverable by the agent at `/mcp/tools`.

---

## 🐳 Dockerized Infrastructure

Everything is containerized using Docker Compose:
- FastAPI backend
- PostgreSQL DB with seeding

---

## 🔧 Commands

```bash
# 1. Build and run everything
docker-compose up --build

# 2. Optional: Run only DB for debugging
docker-compose up db
```

Seeding is handled automatically in `init_db.py`.

---

## 🧪 Backend Env Configuration (`backend/.env`)

```env
GOOGLE_CALENDAR_ID=your_calendar@group.calendar.google.com
GMAIL_APP_PASSWORD=your_gmail_app_password
SMTP_EMAIL=your_email@gmail.com
MCP_SERVER=http://localhost:8000
GROQ_API_KEY=your_groq_api_key
```

**Make sure to:**
- Use a shared calendar (@group.calendar.google.com)
- Share it with your service account
- Enable Gmail App Passwords if you're using SMTP

---

## 🌐 Frontend Setup

The frontend is located in:

```bash
frontend/doctor-agent-ui
```

### 📦 Tech Stack:
- React
- Vite
- Tailwind CSS

### 🛠 Install & Run

```bash
cd frontend/doctor-agent-ui
npm install
npm run dev
```

You can test end-to-end flow from here.

---

## 🧠 Agent Orchestration

The agent is defined in `agent_server.py`, built using langchain.

- LLM tools are loaded dynamically via MCP registry.
- Memory is preserved using `ConversationBufferMemory` by `session_id`.

### Tool Invocation Flow:
```
Natural prompt → Tool selection → API call → Response to user
```

---

## 📸 Sample Prompts

### Patient:
```css
"I want to book an appointment with Dr. Mehta tomorrow morning."
```
→ Agent checks availability, books if slot exists, sends calendar + email.

### Doctor:
```arduino
"How many appointments do I have today?"
```
→ Agent queries DB and returns a structured response.

---

## ✅ Done Highlights

- ✅ Dockerized backend + DB + auto-seeding
- ✅ Google Calendar event creation
- ✅ Email confirmation via SMTP
- ✅ Frontend support for multi-prompt chat
- ✅ LLM tool invocation via MCP
- ✅ Stateless and stateful conversation support
- ✅ Robust exception handling

---

## 📬 Feedback or Questions?

Please contact **Aswin Vishwaa** — this project is fully functional and aligned with the assignment’s architecture using MCP and agentic LLM behavior.
