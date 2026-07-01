from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from pydantic import SecretStr  # <-- NEW IMPORT: This fixes the API key type error
import os

# This is the "notebook" that the robots pass to each other
class AgentState(TypedDict):
    topic: str
    research: str
    extracted_facts: List[str]
    summary: str

# FIX: Wrap os.getenv() inside SecretStr to match the expected type
# This also handles the case where the key might be missing (falls back to empty string)
api_key_value = os.getenv("OPENROUTER_API_KEY", "")
llm = ChatOpenAI(
    model="openrouter/free",
    base_url="https://openrouter.ai/api/v1",
    api_key=SecretStr(api_key_value),  # <-- FIXED: Wrapped in SecretStr
)

# Robot 1: The Reader
def researcher(state: AgentState):
    topic = state['topic']
    response = llm.invoke(f"Research this topic and give a short paragraph: {topic}")
    return {"research": response.content}

# Robot 2: The Fact-Picker
def extractor(state: AgentState):
    research = state['research']
    response = llm.invoke(f"From this text, list exactly 3 main facts: {research}")
    content = str(response.content)  # Convert to string to be safe
    facts = content.split('\n')
    facts = [f for f in facts if f.strip()]
    return {"extracted_facts": facts}

# Robot 3: The Writer
def summarizer(state: AgentState):
    facts = state['extracted_facts']
    response = llm.invoke(f"Write a one-sentence summary of these facts: {facts}")
    return {"summary": response.content}

# Draw the map for the robots
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher)
workflow.add_node("extractor", extractor)
workflow.add_node("summarizer", summarizer)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "extractor")
workflow.add_edge("extractor", "summarizer")
workflow.add_edge("summarizer", END)

# Compile the map so the robots can run
app_agent = workflow.compile()