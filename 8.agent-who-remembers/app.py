import os

from autogen import UserProxyAgent, ConversableAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen.formatting_utils import colored

gpt4o_llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}],
    "timeout": 120,
    "cache_seed": None,  # Disable caching.
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

def create_teachable_agent(reset_db=False):
    """Instantiates a teachable agent using the settings from the top of this file."""
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample
    # config_list = config_list_from_json(env_or_file=OAI_CONFIG_LIST, filter_dict=filter_dict, file_location=KEY_LOC)

    # Start by instantiating any agent that inherits from ConversableAgent.
    teachable_agent = ConversableAgent(
        name="teachable_agent", # The name is flexible, but should not contain spaces to work in group chat.
        llm_config=gpt4o_llm_config,  # Disable caching.
    )

    # Instantiate the Teachability capability. Its parameters are all optional.
    teachability = Teachability(
        verbosity=0,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
        reset_db=reset_db,
        path_to_db_dir="./tmp/8-teachable/teachability_db",
        recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
    )

    # Now add the Teachability capability to the agent.
    teachability.add_to_agent(teachable_agent)

    return teachable_agent



def interact_freely_with_user():
    """Starts a free-form chat between the user and a teachable agent."""

    # Create the agents.
    print(colored("\nLoading previous memory (if any) from disk.", "light_cyan"))
    teachable_agent = create_teachable_agent(reset_db=False) # Preseve what has been learned into a vector db! 
    # By default, Using docker is safer than running the generated code directly.
    user_proxy = UserProxyAgent("user_proxy", human_input_mode="ALWAYS", code_execution_config={})

    # Start the chat.
    teachable_agent.initiate_chat(user_proxy, message="Greetings, I'm a teachable user assistant! What's on your mind today?")



if __name__ == "__main__":
    """Lets the user test a teachable agent interactively."""
    interact_freely_with_user()

