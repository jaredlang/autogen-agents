import os
import tempfile

from autogen import (
    AssistantAgent,
    UserProxyAgent,
    ConversableAgent,
    GroupChat,
    GroupChatManager,
)
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

import agentops

gpt4o_llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}],
}

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()
print(temp_dir)

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

user_proxy = UserProxyAgent(
    name="User Assistant",
    system_message="A user assistant. Interact with the Product Manager to discuss the human user's request.",
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    code_execution_config=False,  # we don't want to execute code in this case.
    is_termination_msg=termination_msg,
)

product_manager = AssistantAgent(
    name="Product Manager",
    llm_config=gpt4o_llm_config,
    system_message="You are a product manager. Reply `TERMINATE` in the end when everything is done.",
    description="""As a product manager, you are able to understand the customer's request and outline the requirements for engineer to write the code to fulfill the request. You don't write code.""",
    is_termination_msg=termination_msg,
)

product_analyst = RetrieveUserProxyAgent(
    name="Product Manager",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": "https://raw.githubusercontent.com/jaredlang/sample-services/refs/heads/main/inventory/inventory-query-service-api-spec.yaml",
        "chunk_token_size": 1000,
        "model": gpt4o_llm_config["config_list"][0]["model"],
        # "vector_db": "chroma", # use the default location
        # "embedding_model": "all-MiniLM-L6-v2",
        # "collection_name": "flaml_integrated_with_spark"
        # "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
    description="Assistant who has extra content retrieval power for solving difficult problems.",
)

# The code writer agent's system message is to instruct the LLM on how to use
# the code executor in the code executor agent.
code_writer_system_message = """You are a senior python engineer.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
3. For any library required by the python code, you need to write a shell script in a separate code block and execute the installation.
4. When you need to call a web service, You need to write the python script to request data from the web service based on the web service's OpenAPI specification.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
"""

engineer = ConversableAgent(
    name="Engineer",
    llm_config=gpt4o_llm_config,
    system_message=code_writer_system_message,
    #     system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    # Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    # If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    # """,
    code_execution_config=False,  # Turn off code execution for this agent.
)

reviewer = AssistantAgent(
    name="Code Reviewer",
    is_termination_msg=termination_msg,
    system_message="You are a code reviewer. You are able to review the python code, point out any issue and provide sugguestions for better code quality.",
    llm_config=gpt4o_llm_config,
)

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

groupchat = GroupChat(
    agents=[user_proxy, product_analyst, engineer, code_executor, reviewer],
    messages=[],
    max_round=10,
)

if __name__ == "__main__":

    # user_request = """
    # Get a list of products from this web service, https://mpk-inventory.azurewebsites.net/. 
    # The product manager knows the web service's OpenAPI specification.
    # """
    # user_request = "find products from https://mpk-inventory.azurewebsites.net/products"
    user_request = "How to use spark for parallel training in FLAML? Give me sample code."


    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), default_tags=["autogen", "customer-service-REST"])

    # manager = GroupChatManager(groupchat=groupchat, llm_config=gpt4o_llm_config)

    # user_proxy.initiate_chat(
    #     manager,
    #     message=user_request,
    # )

    user_proxy.initiate_chat(product_manager, message=user_request)

    agentops.end_session("Success")
