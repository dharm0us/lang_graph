from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    elif model_name == "anthropic":
        model =  ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


# system_prompt = """You will be given a country's name. You take a neighbouring country to the east, and give weather in its capital."""
system_prompt = """You are a sarcastic assistant."""
# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "anthropic")
    model = _get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def call_openai_model(state):
    messages = state["input_messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model = _get_model('openai')
    response = model.invoke(messages)
    state['openai_response'] = response
    return state

def call_anthropic_model(state):
    messages = state["input_messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model = _get_model('anthropic')
    response = model.invoke(messages)
    state['anthropic_response'] = response
    return state

# Define the function to execute tools
tool_node = ToolNode(tools)