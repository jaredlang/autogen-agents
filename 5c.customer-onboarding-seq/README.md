# Observations on 5c.customer-onboarding-seq

This app uses sequntial chats to guide the onboarding flow and gather user info along the way.

## Training Course on deeplearning.ai

<https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/3/sequential-chats-and-customer-onboarding>

1. Each chat is configured independently on two parties.
2. max_turns is a very rigid way to end a conversation.
  a. **How to deal with the uncertainty in the user input?**
3. *clear_history* helps reduce the past chat storage. When it is false, the chat history is passed to the next chat as a context.
4. *summary_prompt* is to prompt how to summarize the conversation. It can extract data from the convesation and structure it in a programmatic format.
5. *customer_proxy_agent* doesn't have llm config. What model does it use?
6. Sometimes GPT returns this error, but Claude doesn't.

```json
openai.BadRequestError: Error code: 400 - {'error': {'message': "Invalid 'messages[1].name': string does not match pattern. Expected a string that matches the pattern '^[a-zA-Z0-9_-]+$'.", 'type': 'invalid_request_error', 'param': 'messages[1].name', 'code': 'invalid_value'}}
```

- Another error message

```json
C:\source\ai.dev\autogen-agent\.venv\Lib\site-packages\autogen\agentchat\conversable_agent.py:1277: UserWarning: Cannot extract summary using reflection_with_llm: Error code: 400 - {'error': {'message': "Invalid 'messages[0].name': string does not match pattern. Expected a string that matches the pattern '^[a-zA-Z0-9_-]+$'.", 'type': 'invalid_request_error', 'param': 'messages[0].name', 'code': 'invalid_value'}}. Using an empty str as summary.
  warnings.warn(
```

## The invalid_request_error is fixed

I found this post at <https://stackoverflow.com/questions/78649446/autogen-groupchat-error-code-openai-badrequesterror-error-code-400>
I removed the space from the agent names. **It solved the problem.**
