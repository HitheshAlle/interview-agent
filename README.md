# Eve - AI Interview Practice Partner 🎙️

**Submitted for the Eightfold.ai AI Agent Assignment**

## 🚀 Project Overview
**Eve** is a real-time, multimodal Voice AI agent designed to simulate realistic job interviews. Unlike standard chatbots, Eve operates over **WebRTC (LiveKit)**, enabling **sub-500ms latency**, natural turn-taking, and the ability to handle user interruptions ("barge-in").

The system is context-aware: it parses the candidate's uploaded resume and selected role to generate a dynamic, unique interview session every time.

## 🧠 Key Features (Agentic Behavior)
* **Dynamic Persona Injection:** The agent reads the user's resume and target role at runtime to generate specific, relevant questions.
* **Interruptibility (Barge-In):** The user can cut the agent off mid-sentence, and the agent stops speaking immediately to listen.
* **Adaptive Feedback Loop:** At the user's request ("I'm done, give me feedback"), the agent switches to "Evaluator Mode" and provides a structured rating.

## 🏗️ Architecture & Tech Stack
1.  **Transport Layer:** **LiveKit (WebRTC)** for real-time streaming audio.
2.  **Orchestration:** **Python `livekit-agents` (v1.3.3)**.
3.  **Intelligence:** **Google Gemini 2.5 Flash**. Selected for superior speed and reasoning capabilities.
4.  **Transcriber:** **Deepgram Nova-2**.
5.  **Voice:** **Deepgram Aura**.
6.  **Context Server:** **`aiohttp` + `pypdf`**. A lightweight server to parse PDFs and stage the context.

## 🛠️ Setup Instructions

### Prerequisites
* Python 3.10+
* API Keys for LiveKit, Deepgram, and Google Gemini.

### Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Create a `.env` file:
    ```env
    LIVEKIT_URL=...
    LIVEKIT_API_KEY=...
    LIVEKIT_API_SECRET=...
    DEEPGRAM_API_KEY=...
    GOOGLE_API_KEY=...
    ```

### Usage
1.  Start the UI Server: `python server.py`
2.  Start the Agent: `python agent.py dev`
3.  Open `http://localhost:8080`, select a role, upload a resume, and connect.
