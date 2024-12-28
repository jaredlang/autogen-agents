import os
from autogen import ConversableAgent

from typing import Annotated, Literal

Operator = Literal["+", "-", "*", "/"]

# Define a tool as a function
# Always use type hints to define the types of the arguments and the return value 
# as they provide helpful hints to the agent about the tool's usage.
# Annotated - something new 
def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")


# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# # Register the tool signature with the assistant agent.
# assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)

# # Register the tool function with the user proxy agent.
# user_proxy.register_for_execution(name="calculator")(calculator)

from autogen import register_function

# Register the calculator function to the two agents.
# Why does it need to register with two agents? Because 
# - the one (caller) needs to understand the tool enough to suggest using it. 
# - the other (executor) needs to understand the tool to execute it. 
# The tool schema is derived from the function signature. 
# If needed, you can use pydentic to define the tool schema with additional details. 
register_function(
    calculator,
    caller=assistant,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="calculator",  # By default, the function name is used as the tool name.
    description="A simple calculator",  # A description of the tool.
)

chat_result = user_proxy.initiate_chat(assistant, message="What is (44232 + 13312 / (232 - 32)) * 5?")
