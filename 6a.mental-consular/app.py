import os

from autogen import ConversableAgent
from autogen import Cache

import agentops

from mem0 import MemoryClient

gpt4o_llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}]
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

memory = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))


def preload_data_to_memory(user_id):

    chat_history = [
        {
            "role": "assistant",
            "name": "carebot",
            "content": "Hi Cathy, how are you doing today?",
        },
        {
            "role": "user",
            "name": "Cathy",
            "content": "To be honest, I've been feeling a bit down and demotivated lately. It's been tough.",
        },
        {
            "role": "assistant",
            "name": "CareBot",
            "content": "I'm sorry to hear that you're feeling down and demotivated, Cathy. It's understandable given the challenges you're facing. Can you tell me more about what's been going on?",
        },
        {
            "role": "user",
            "name": "Cathy",
            "content": "Well, I'm really struggling to process the passing of my mother.",
        },
        {
            "role": "assistant",
            "name": "CareBot",
            "content": "I'm deeply sorry for your loss, Cathy. Losing a parent is incredibly difficult. It's normal to struggle with grief, and there's no 'right' way to process it. Would you like to talk about your mother or how you're coping?",
        },
        {
            "role": "user",
            "name": "Cathy",
            "content": "Yes, I'd like to talk about my mother. She was a kind and loving person.",
        },
    ]

    return memory.add(messages=chat_history, user_id=user_id)


health_consular = ConversableAgent(
    "health_consular",
    system_message="You are returning to your conversation with care_bot, a mental health bot. Ask the bot about your previous session.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4o",
                "temperature": 0,
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
    },
    human_input_mode="ALWAYS",
)

care_bot = ConversableAgent(
    "care_bot",
    system_message="""You are a compassionate mental health bot and caregiver. Review information about the user and their prior conversation below and respond accordingly.
Keep responses empathetic and supportive. And remember, always prioritize the user's well-being and mental health. Keep your responses very concise and to the point.
""",
    llm_config=claude_llm_config,
    human_input_mode="NEVER",
)

patient_id = "patient_cathy-wong"

# Should be loaded only once
# is_committed = preload_data_to_memory(patient_id)
# print(f"is the history committed to memory? {is_committed}")

# question = "How do you feel about the passing of your mother?"  
question = "Are you feel better today?"  

relevant_memories = memory.search(question, user_id=patient_id)
flatten_relevant_memories = "\n".join([m["memory"] for m in relevant_memories])

prompt = f"""
Context:
{flatten_relevant_memories}
\n\n
Question: {question}
"""

# Start AgentOps Observation
agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), default_tags=["health-consular", patient_id])

with Cache.disk() as cache:
    health_consular.initiate_chat(care_bot, message=prompt, cache=cache)

agentops.end_session("Success")

# memory.delete_all(user_id=customer_id)
