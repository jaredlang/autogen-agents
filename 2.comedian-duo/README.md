# Observation on 2.comedian-duo

This app is based on <https://microsoft.github.io/autogen/0.2/docs/tutorial/chat-termination>.

## How to control the termination of a chat?

On each agent, set the termination config.

- is_termination_msg. A critiera is defined as a function and determine if a chat is to be terminated.
- max_consecutive_auto_reply. The max number of auto replies.
- max_turns. The max number of times an agent speaks.

## Training Course on deeplearning.ai

<https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/2/multi-agent-conversation-and-stand-up-comedy>

1. *generate_reply* invoke an agent to act, but it doesn't preserve the history. *initiate_chat* does.
2. By default, AutoGen uses cache to generate the same response to the same input.
  a. **Without specifying cache, where is the cache stored?**
  b. **How to clear the cache?**
3. By default, the chat summary is the last response.
4. To get the summary of the whole conversation, use *summary_method* and *summary_prompt*.

```python
chat_result = joe.initiate_chat(
    cathy, 
    message="I'm Joe. Cathy, let's keep the jokes rolling.", 
    max_turns=2, 
    summary_method="reflection_with_llm",
    summary_prompt="Summarize the conversation",
)
```

## Chat termination

- define max_turns. This approach doesn't prepare any memory in agents. The following line doesn't produce a response from Joe.

```python
cathy.send(message="What's last joke we talked about?", recipient=joe)
```

- define a keyword to end the conversation. This approach does prepare any memory in agents. Joe remembers the last joke.

```python
joe = ConversableAgent(
    name="joe",
    system_message=
    "Your name is Joe and you are a stand-up comedian. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
)
```

**Why is there such a discrepency?**
