# agent.py
# The brain of the healthcare assistant
# Contains 3 tools + LangChain Agent

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
from vector_store import build_vector_store, search_patient_memory
from patients import PATIENTS, DOCTOR_SCHEDULE, find_patient

load_dotenv(override=True)

# Securely grab the API Key from either local .env or Streamlit Secrets
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

print("OpenAI Key Loaded:", bool(api_key))

if api_key:
    print("Key prefix:", api_key[:10])
else:
    print("No API key found")

# Initialize vector_store as None globally so it can be safely populated later
vector_store = None

# ─────────────────────────────────────────
# TOOL 1 — Get Patient History
# ─────────────────────────────────────────
@tool
def get_patient_history(patient_name: str) -> str:
    """
    Use this tool to get a patient's medical history.
    Input: patient name as a string.
    Example: get_patient_history("Ramesh Kumar")
    """
    global vector_store
    pid, patient = find_patient(patient_name)

    if patient:
        return f"""
Patient Found:
- Name: {patient['name']}
- Age: {patient['age']}
- Disease: {patient['disease']}
- Doctor: {patient['doctor']}
- History: {patient['history']}
        """

    # If not found by name, search FAISS (if vector store is initialized)
    if vector_store:
        result = search_patient_memory(vector_store, patient_name)
        if result and "No matching patient found" not in result:
            return f"Patient found via memory search:\n{result}"

    return f"No patient found with name: {patient_name}"


# ─────────────────────────────────────────
# TOOL 2 — Book Appointment
# ─────────────────────────────────────────
@tool
def book_appointment(patient_name: str, doctor_name: str) -> str:
    """
    Use this tool to book a doctor appointment for a patient.
    Input: patient name and doctor name.
    Example: book_appointment("Ramesh Kumar", "Dr. Sharma")
    """
    pid, patient = find_patient(patient_name)
    if not patient:
        return f"Cannot book. Patient '{patient_name}' not found."

    doctor = None
    for doc_name in DOCTOR_SCHEDULE:
        if doctor_name.lower() in doc_name.lower():
            doctor = doc_name
            break

    if not doctor:
        doctor = patient.get("doctor", None)
        if not doctor or doctor not in DOCTOR_SCHEDULE:
            return f"Doctor '{doctor_name}' not found."

    schedule = DOCTOR_SCHEDULE[doctor]
    if not schedule["available_slots"]:
        return f"No available slots for {doctor} today."

    slot = schedule["available_slots"][0]
    schedule["available_slots"].remove(slot)
    schedule["booked_slots"].append({
        "patient": patient["name"],
        "slot": slot
    })

    return f"""
Appointment Booked!
- Patient : {patient['name']}
- Doctor  : {doctor}
- Slot    : {slot}
- Status  : Confirmed ✓
    """


# ─────────────────────────────────────────
# TOOL 3 — Search Disease Information
# ─────────────────────────────────────────
@tool
def search_disease_info(disease_name: str) -> str:
    """
    Returns basic medical information.
    """
    return f"Information requested for: {disease_name}. Please use the language model's medical knowledge to answer."
    

# ─────────────────────────────────────────
# BUILD THE AGENT
# ─────────────────────────────────────────
def build_agent():
    global vector_store
    
    # Safely build the vector database only when this function is explicitly invoked
    print("Loading patient memory...")
    vector_store = build_vector_store()
    print("Memory ready!")

    tools = [get_patient_history, book_appointment, search_disease_info]

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=200,
        api_key=api_key
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional healthcare assistant for a hospital.
You have access to 3 tools:
1. get_patient_history  — look up patient medical records
2. book_appointment     — book doctor appointments  
3. search_disease_info  — search medical information

Rules:
- Always use get_patient_history before booking an appointment
- Be professional, clear and concise
- If you cannot find information, say so honestly"""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        early_stopping_method="generate"
    )

    return agent_executor


# ─────────────────────────────────────────
# TEST LOCALLY
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Healthcare AI Agent — Testing")
    print("="*50)

    agent = build_agent() 

    result = agent.invoke({
        "input": "What are the symptoms of kidney stones?"
    })

    print("\nFinal Answer:", result["output"])
    print("\n" + "="*50)
    print("Agent test complete!")
    print("="*50)
