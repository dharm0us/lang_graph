from dotenv import load_dotenv

load_dotenv()

import os
from typing import Dict, List, Tuple
from langgraph.graph import Graph, END
from langchain_core.messages import HumanMessage

from my_agent.utils.nodes import call_openai_model, call_anthropic_model

# Initialize language models

def combine_responses(state: Dict) -> Dict:
    openai_response = state["openai_response"]
    anthropic_response = state["anthropic_response"]
    state["combined_response"] = {
        "OpenAI": openai_response,
        "Anthropic": anthropic_response
    }
    return state

# Define the graph
workflow = Graph()

# Add nodes to the graph
workflow.add_node("OpenAI", call_openai_model)
workflow.add_node("Anthropic", call_anthropic_model)
workflow.add_node("Combine", combine_responses)

# Define the edges
workflow.add_edge("Anthropic", "OpenAI")
workflow.add_edge("OpenAI", "Combine")
workflow.add_edge("Combine", END)

# Set the entrypoint
workflow.set_entry_point("Anthropic")

# Compile the graph
app = workflow.compile()

# Function to run the workflow
def run_workflow(prompt: str) -> Dict:

    inputs = {"input_messages": [{"role": "user", "content": prompt}]}
    result = app.invoke(inputs)
    return result["combined_response"]

# Example usage
if __name__ == "__main__":
    user_prompt = "Explain the concept of quantum entanglement in simple terms."
    result = run_workflow(user_prompt)
    
    print("OpenAI response:")
    print(result["OpenAI"])
    print("\nAnthropic response:")
    print(result["Anthropic"])