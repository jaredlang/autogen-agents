import os
from pprint import pprint

from autogen import ConversableAgent

gpt4o_llm_config = {
        "config_list": [
            {
                "model": "gpt-4",
                "temperature": 0.9, # creative
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
    }

cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config=gpt4o_llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = ConversableAgent(
    "joe",
    system_message="""Your name is Joe and you are a part of a duo of comedians. 
    Start the next joke from the punchline of the previous joke.""",
    llm_config=gpt4o_llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
    max_consecutive_auto_reply=1,  # Limit the number of consecutive auto-replies.
    # is_termination_msg=lambda msg: "goodbye" in msg["content"].lower(),
)

# generate a reply from one agent. generate_reply() doesn't preserve the chat history.
reply = cathy.generate_reply(
    messages=[{"content": "Tell me a joke.", "role": "user"}]
)
print(reply)

# Start the conversation.
chat_result = joe.initiate_chat(
    cathy,
    # message="Cathy, tell me a joke and then say the words GOODBYE.",
    message="Cathy, tell me a joke.",
    max_turns=2,
)

pprint(chat_result.chat_history)
pprint(chat_result.summary) # by default, the last message is the summary
pprint(chat_result.cost)

cathy.send(message="What's last joke we talked about?", recipient=joe)
