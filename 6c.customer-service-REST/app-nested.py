import os
import tempfile

from autogen import (
    AssistantAgent,
    UserProxyAgent,
    ConversableAgent,
    GroupChat,
    GroupChatManager,
)
from autogen.coding import DockerCommandLineCodeExecutor
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
from autogen import Cache

gpt4o_llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}],
}

claude_llm_config = {
    "config_list": [
        {
            "model": "claude-3-5-sonnet-20240620",
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "api_type": "anthropic",
        }
    ]
}

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


user_proxy = UserProxyAgent(
    name="user_proxy",  # "user assistant" threw an error. see user-assistant-error-msg.txt
    code_execution_config=False,  # we don't want to execute code in this case.
)

product_manager = AssistantAgent(
    name="product manager",
    llm_config=claude_llm_config,
    system_message="You are a product manager. Come up with a product design to accomplish the user's request. You do not write code."
)

dev_manager = AssistantAgent(
    name="software development manager",
    llm_config=claude_llm_config,
    system_message="You are a software development manager. Rely the output of software_engineer and code_executor. You do not write code."
)

# The code writer agent's system message is to instruct the LLM on how to use
# the code executor in the code executor agent.
code_writer_system_message = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
3. For any library required by the python code, you need to write a shell script in a separate code block and execute the installation.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
"""

software_engineer = AssistantAgent(
    name="Software Engineer",
    llm_config=claude_llm_config,
    system_message=code_writer_system_message,
#     system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
# Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
# If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
# """,
    code_execution_config=False,  # Turn off code execution for this agent.  
    is_termination_msg=termination_msg,
    default_auto_reply="Reply `TERMINATE` if the task is done.",
)

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()
# Create a Docker command line code executor.
docker_executor = DockerCommandLineCodeExecutor(
    image="python:3.12-slim",  # Execute code using the given docker image name.
    timeout=60,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration.
code_executor = ConversableAgent(
    "code_executor",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={
        "executor": docker_executor
    },  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

# This agent is nothing about a proxy. 
code_executor_proxy = AssistantAgent(
    name="code_executor_proxy",
    is_termination_msg=termination_msg,
    llm_config=claude_llm_config,
)

def deliver_requirement(recipient, messages, sender, config):
    print("Reflecting...", "yellow")
    return f"""Follow the instruction to execute the scripts. If there is more than one code block, execute them sequentially. 
    [INSTRUCTION]
    {recipient.chat_messages_for_summary(sender)[-1]['content']}
    """

user_proxy.register_nested_chats(
    [
        {
            "sender": code_executor_proxy,
            "recipient": code_executor,
            "message": deliver_requirement,
            "max_turns": 2,
            "summary_method": "last_msg",
        }
    ],
    trigger=software_engineer,  # condition=my_condition,
)

if __name__ == "__main__":

    # user_request = "find products from https://mpk-inventory.azurewebsites.net/products"
    user_request = """
    Find flagship-900 products from the inventory website: https://mpk-inventory.azurewebsites.net/
    Please refer to the website OpenAPI specification at https://raw.githubusercontent.com/jaredlang/sample-services/refs/heads/main/inventory/inventory-query-service-api-spec.yaml
    """

    with Cache.disk() as cache:
        # user_proxy.initiate_chat(product_manager, message=user_request, cache=cache)
        user_proxy.initiate_chat(software_engineer, message=user_request)
