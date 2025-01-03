# Observations on 10.chat_with_multiple_LLMs

This app is based on <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_multi_task_async_chats/>.

This example allows a better control on the speaker sequence.

1. At first I used ConversableAgent. It always wanted the human input before the conversation can move forward.
  a. Even when I set human_input_model with NEVER and code_execution_config with False, which are the default values of UserAssistant, the conversation between the agent and the user_proxy becomes an infinite loop.
2. I switched UserAssistant. It seems having better handling on when to terminate the conversation so the chat can continue.
3. Claude was smart enough to write code to google the internet, while GPT4o just returned a canned response.
4. Sometimes the chat seems chaotic. It doesn't work in the same way every time.
