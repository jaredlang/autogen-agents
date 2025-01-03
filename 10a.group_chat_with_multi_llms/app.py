import asyncio
import os

from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

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

is_termination_msg = lambda x: x.get("content", "") and x.get(
    "content", ""
).rstrip().endswith("TERMINATE")

user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "groupchat",
        "use_docker": True,
    },
)

research_assistant = AssistantAgent(
    name="Researcher",
    llm_config=gpt4o_llm_config,
    is_termination_msg=is_termination_msg,
)

writer = AssistantAgent(
    name="Writer",
    llm_config=gpt4o_llm_config,
    system_message="""
    You are a professional writer, known for
    your insightful and engaging articles.
    You transform complex concepts into compelling narratives.
    Reply "TERMINATE" in the end when everything is done.
    """,
)

critic = AssistantAgent(
    name="Critic",
    system_message="""Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.
    Reply "TERMINATE" in the end when everything is done.
    """,
    llm_config=gpt4o_llm_config,
)

groupchat_1 = GroupChat(
    agents=[user_proxy, research_assistant, critic], messages=[], max_round=50
)

groupchat_2 = GroupChat(agents=[user_proxy, writer, critic], messages=[], max_round=50)

manager_1 = GroupChatManager(
    groupchat=groupchat_1,
    name="Research_manager",
    llm_config=gpt4o_llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "groupchat",
        "use_docker": True,
    },
)
manager_2 = GroupChatManager(
    groupchat=groupchat_2,
    name="Writing_manager",
    llm_config=gpt4o_llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "groupchat",
        "use_docker": True,
    },
)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": True,
    },
)

# Start the chat.

financial_tasks = [
    """What are the current stock prices of NVDA and TESLA, and how is the performance over the past month in terms of percentage change?""",
    """Investigate possible reasons of the stock performance.""",
    """Plot a graph comparing the stock prices over the past month.""",
]

writing_tasks = ["""Develop an engaging blog post using any information provided."""]

asyncio.run(
    user.a_initiate_chats(  # noqa: F704
        [
            {
                "chat_id": 1,
                "recipient": research_assistant,
                "message": financial_tasks[0],
                "summary_method": "last_msg",
            },
            {
                "chat_id": 2,
                "prerequisites": [1],
                "recipient": manager_1,
                "message": financial_tasks[1],
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 3,
                "prerequisites": [1],
                "recipient": manager_1,
                "message": financial_tasks[2],
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 4,
                "prerequisites": [1, 2, 3],
                "recipient": manager_2,
                "message": writing_tasks[0],
            },
        ]
    )
)
