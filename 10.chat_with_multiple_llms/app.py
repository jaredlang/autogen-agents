import asyncio
import os

from autogen import UserProxyAgent, ConversableAgent, AssistantAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen.formatting_utils import colored

import agentops

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


def create_teachable_agent(
    reset_db=False, llm_config=gpt4o_llm_config, agent_name="teachable_agent"
):
    """Instantiates a teachable agent using the settings from the top of this file."""
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample
    # config_list = config_list_from_json(env_or_file=OAI_CONFIG_LIST, filter_dict=filter_dict, file_location=KEY_LOC)

    # Start by instantiating any agent that inherits from ConversableAgent.
    teachable_agent = ConversableAgent(
        name=agent_name,  # The name is flexible, but should not contain spaces to work in group chat.
        llm_config=llm_config,  # Disable caching.
        human_input_mode="NEVER",  # That is default value of AssistantAgent.
        code_execution_config=False,  # That is default value of AssistantAgent.
        system_message="Reply 'TERMINATE' in the end when everything is done."
    )

    # Instantiate the Teachability capability. Its parameters are all optional.
    teachability = Teachability(
        verbosity=0,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
        reset_db=reset_db,
        path_to_db_dir=f"./tmp/10-chat-with-multi-llms/{agent_name}/agent_mem_db",
        recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
    )

    # Now add the Teachability capability to the agent.
    teachability.add_to_agent(teachable_agent)

    return teachable_agent


async def interact_freely_with_user(user_input: str):
    """Starts a free-form chat between the user and a teachable agent."""

    # Create the agents.
    print(colored("\nLoading previous memory (if any) from disk.", "light_cyan"))
    # Preseve what has been learned into a vector db!
    gpt4o_agent = create_teachable_agent(
        reset_db=False, llm_config=gpt4o_llm_config, agent_name="gpt4o_agent"
    )
    claude_agent = create_teachable_agent(
        reset_db=False, llm_config=claude_llm_config, agent_name="claude_agent"
    )

    reviewer_agent = AssistantAgent(
        name="reviewer",
        llm_config=gpt4o_llm_config,
        system_message="""
        You review the generated answers from previous agents, and write the final summary.
        Reply "TERMINATE" in the end when everything is done.
        """,
    )

    # By default, Using docker is safer than running the generated code directly.
    user_proxy = UserProxyAgent(
        "user_proxy",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )

    # Start the chat.
    chat_results = await user_proxy.a_initiate_chats(
        [
            {
                "chat_id": 1,
                "recipient": gpt4o_agent,
                "message": user_input,
                "silent": False,
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 2,
                "recipient": claude_agent,
                "message": user_input,
                "silent": False,
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 3,
                "prerequisites": [1, 2],
                "recipient": reviewer_agent,
                "message": "write a final summary to include answers from previous agents. The summary should be concise and informative.",
                "silent": False,
            },
        ]
    )


if __name__ == "__main__":
    agentops.init(os.getenv("AGENTOPS_API_KEY"), default_tags=["chat_with_multiple_llms", "a_initiate_chats", "ConversableAgent"])
    """Lets the user test a teachable agent interactively."""
    asyncio.run(
        interact_freely_with_user(
            "What's the Orca model?"
            # "what's the deepseek model?"
            # "which one is a better LLM model, GPT-4o or Claude?"
        )
    )
    agentops.end_session("Success")
