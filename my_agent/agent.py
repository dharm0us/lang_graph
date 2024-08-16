from dotenv import load_dotenv

load_dotenv()
# from my_agent.utils.interceptor import enable_httpx_logging,enable_request_logging

# enable_request_logging()
# enable_httpx_logging()

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from my_agent.utils.nodes import call_model, should_continue, tool_node
from my_agent.utils.state import AgentState
import os

# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai"]

# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Set the entrypoint as `agent`
workflow.set_entry_point("agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

# Add a normal edge from `action` to `agent`
workflow.add_edge("action", "agent")

if __name__ == "__main__":
    graph = workflow.compile(debug=True)
    result = graph.invoke({"messages": [{"role": "user", "content": "What is the weather in Tokyo?"}]})
    print(result)
else:
    graph = workflow.compile()
