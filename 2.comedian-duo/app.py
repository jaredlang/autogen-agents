import os

from autogen import ConversableAgent

cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "temperature": 0.9,
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
    },
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "temperature": 0.7,
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }
        ]
    },
    human_input_mode="NEVER",  # Never ask for human input.
    max_consecutive_auto_reply=1,  # Limit the number of consecutive auto-replies.
    # is_termination_msg=lambda msg: "goodbye" in msg["content"].lower(),
)

result = joe.initiate_chat(
    cathy,
    # message="Cathy, tell me a joke and then say the words GOODBYE.",
    message="Cathy, tell me a joke.",
    max_turns=3,
)
