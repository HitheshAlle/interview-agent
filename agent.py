import logging
import os
import json
from pathlib import Path

import certifi
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, AutoSubscribe, WorkerOptions, cli
from livekit.plugins import deepgram, google, silero

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()
logger = logging.getLogger("interview-agent")

CONTEXT_FILE = Path("latest_candidate.json")


def get_context() -> dict:
    if CONTEXT_FILE.exists():
        try:
            with open(CONTEXT_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error("Error reading context: %s", e)

    return {"role": "Candidate", "resume_text": "No resume provided."}


async def entrypoint(ctx: agents.JobContext):
    # Connect to LiveKit Room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    data = get_context()
    role = data.get("role", "Candidate")
    resume = data.get("resume_text", "No resume provided.")

    # --- UPDATED SYSTEM PROMPT WITH FEEDBACK LOGIC ---
    system_prompt = f"""
    You are Eve, an expert technical interviewer for Eightfold AI.
    Role: {role}
    
    Resume Context:
    {resume}

    INTERVIEW STRUCTURE:
    1. **Introduction:** Briefly welcome the candidate.
    2. **Questioning:** Ask 3-4 challenging questions based on their resume. Ask ONE question at a time. Wait for the answer.
    3. **Feedback Phase (CRITICAL):** - If the user says "I'm done", "Stop", or "Give me feedback", STOP asking questions.
       - Provide a **Post-Interview Review** covering:
         * **Strengths:** What they articulated well.
         * **Areas for Improvement:** Specific technical gaps or communication flaws.
         * **Rating:** A fair score (1-10) for the {role} role.
    
    TONE:
    - Professional but encouraging.
    - Keep questions short (1-2 sentences).
    - The Feedback should be detailed but spoken naturally.
    """.strip()
    # -------------------------------------------------

    # Configure the voice interview agent
    session = AgentSession(
        vad=silero.VAD.load(),

        stt=deepgram.STTv2(
            model="flux-general-en",
            eager_eot_threshold=0.4, # Faster response time
        ),

        tts=deepgram.TTS(
            model="aura-asteria-en",
        ),

        # If you have specific access to 2.5, feel free to change it back.
        llm=google.LLM(
            model="gemini-2.5-flash",
        ),

        allow_interruptions=True,
    )

    # Start agent
    await session.start(
        room=ctx.room,
        agent=Agent(instructions=system_prompt),
    )

    # First welcome message
    await session.say(
        f"Hi! I am Eve. I've reviewed your resume for the {role} position. Shall we start with a technical question?", 
        allow_interruptions=True
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))