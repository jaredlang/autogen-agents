import os
from autogen import ConversableAgent, initiate_chats

gpt4o_llm_config = {
    "config_list": [
        # {"model": "gpt-3.5-turbo", "api_key": os.getenv("OPENAI_API_KEY")},
        # {"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")},
        {"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")},
    ]
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

onboarding_personal_information_agent = ConversableAgent(
    name="Onboarding_Personal_Information_Agent",
    system_message="""You are a helpful customer onboarding agent,
    you are here to help new customers get started with our product.
    Your job is to gather customer's name and location.
    Do not ask for other information. Return 'TERMINATE' 
    when you have gathered all the information.""",
    llm_config=gpt4o_llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

onboarding_topic_preference_agent = ConversableAgent(
    name="Onboarding_Topic_preference_Agent",
    system_message="""You are a helpful customer onboarding agent,
    you are here to help new customers get started with our product.
    Your job is to gather customer's preferences on news topics.
    Do not ask for other information.
    Return 'TERMINATE' when you have gathered all the information.""",
    llm_config=gpt4o_llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

customer_engagement_agent = ConversableAgent(
    name="Customer_Engagement_Agent",
    system_message="""You are a helpful customer service agent
    here to provide fun for the customer based on the user's
    personal information and topic preferences.
    This could include fun facts, jokes, or interesting stories.
    Make sure to make it engaging and fun!
    Return 'TERMINATE' when you are done.""",
    llm_config=gpt4o_llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

customer_proxy_agent = ConversableAgent(
    name="customer_proxy_agent",
    llm_config=False,
    code_execution_config=False,
    human_input_mode="ALWAYS",
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

seqential_chats = [
    {
        "sender": onboarding_personal_information_agent,
        "recipient": customer_proxy_agent,
        "message": "Hello, I'm here to help you get started with our product. Could you tell me your name and location?",
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": """Return the customer information as JSON object only:
                             {'name': '', 'location': ''} """
        },
        # when 2 is specified, the agent always ask the question twice, 
        # even when the user provides the information in the first turn
        "max_turns": 1,
        "clear_history": True,
    },
    {
        "sender": onboarding_topic_preference_agent,
        "recipient": customer_proxy_agent,
        "message": "Great! Could you tell me what topics you are interested in reading about?",
        # only interested in the chat summary
        "summary_method": "reflection_with_llm",
        "max_turns": 1,
        # preserve the history for next chat
        "clear_history": False,
    },
    {
        "sender": customer_proxy_agent,
        "recipient": customer_engagement_agent,
        "message": "Let's find something fun to read.",
        "max_turns": 1,
        "summary_method": "reflection_with_llm",
    },
]

chat_results = initiate_chats(seqential_chats)

for chat_result in chat_results:
    print(chat_result.summary)
    print("\n")

for chat_result in chat_results:
    print(chat_result.cost)
    print("\n")
