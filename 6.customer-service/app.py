import os

from autogen import ConversableAgent
from autogen import Cache

from mem0 import MemoryClient

memory = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))


def preload_data_to_memory(user_id):

    chat_history = [
        {
            "role": "assistant",
            "content": "Hi, I'm Best Buy's chatbot!\n\nThanks for being a My Best Buy TotalTM member.\n\nWhat can I help you with?",
        },
        {
            "role": "user",
            "content": 'Seeing horizontal lines on our tv. TV model: Sony - 77" Class BRAVIA XR A80K OLED 4K UHD Smart Google TV',
        },
        {
            "role": "assistant",
            "content": "Thanks for being a My Best Buy Total™ member. I can connect you to an expert immediately - just one perk of your membership!\n\nSelect the button below when you're ready to chat.",
        },
        {
            "role": "assistant",
            "content": "Good evening, thank you for choosing Best Buy, Fnu. My name is Lovely. I hope you are doing well. I'm sorry to hear that you're seeing horizontal lines on your TV.\n\nI'm absolutely committed to exploring all possible ways to assist you to fix this issue.\n\nTo ensure that we are on the right account, may I please have your email address registered with your Best Buy account?",
        },
        {"role": "user", "content": "dd@gmail.com"},
        {
            "role": "assistant",
            "content": "Perfect! Thank you for providing all the details, surely you have made my job easier by doing this. I really appreciate it.\n\nI also want to take a moment to express our heartfelt appreciation for your trust and loyalty. Thank you for being an amazing customer of BestBuy Total.\n\nCould you please help me with the order number or product's details to check it quickly?\n\nSamsung - 49\" Odyssey OLED G9 (G95SC) DQHD 240Hz 0.03ms G-Sync Compatible Curved Smart Gaming Monitor - Silver - just to confirm this is the item, right?",
        },
        {"role": "user", "content": "Order number: 112217629"},
        {
            "role": "assistant",
            "content": "Superb! Thank you for confirmation.\n\nThank you for your patience. After exploring all possible solutions, I can help you to arrange a home repair appointment for your device. Our Geek Squad experts will visit your home to inspect and fix your device.\n\nIt's great that you have a protection plan - rest assured, we've got your back! As a valued Total member, you can avail this service at a minimal service fee. This fee, applicable to all repairs, covers the cost of diagnosing the issue and any small parts needed for the repair. It's part of our 24-month free protection plan.\n\nPlease click here to review the service fee and plan coverage details -\n\nhttps://www.bestbuy.com/site/best-buy-membership/best-buy-protection/pcmcat1608643232014.c?id=pcmcat1608643232014#jl-servicefees\n\nFnu - just to confirm shall I proceed to schedule the appointment?",
        },
        {"role": "user", "content": "Yes please"},
        {"role": "assistant", "content": "When should I schedule the appointment?"},
        {"role": "user", "content": "Schedule it for tomorrow please"},
    ]

    return memory.add(messages=chat_history, user_id=user_id)


manager = ConversableAgent(
    "manager",
    system_message="You are a manager who helps in resolving customer issues.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "temperature": 0,
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
    },
    human_input_mode="ALWAYS",
)

customer_bot = ConversableAgent(
    "customer_bot",
    system_message="You are a customer service bot who gathers information on issues customers are facing. Keep answers clear and concise.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "temperature": 0,
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
    },
    human_input_mode="NEVER",
)

customer_id = "customer_brian-smith"

# Should be loaded only once
is_committed = preload_data_to_memory(customer_id)
print(f"is the history committed to memory? {is_committed}")

# question = "I forgot the order numnber, can you quickly tell me?"
# question = "When is the appointment?"
question = "What's my email address?" # --> Not able to find the context in the memory

relevant_memories = memory.search(question, user_id=customer_id)
flatten_relevant_memories = "\n".join([m["memory"] for m in relevant_memories])

prompt = f"""
Context:
{flatten_relevant_memories}
\n\n
Question: {question}
"""

result = manager.send(prompt, customer_bot, request_reply=True)

# with Cache.disk() as cache:
#     manager.initiate_chat(customer_bot, message=prompt, cache=cache)

# memory.delete_all(user_id=customer_id)
