# Observations on 6c. Customer Service with REST

1. When "user assistant" is assigned to the name of user_proxy, the app throws an error. see [user-assistant-error-msg.txt](./user-assistant-error-msg.txt). Why???
2. The error is gone when I used "user_proxy" or "boss". Is "Assistant" a reserved word?
3. I also noticed the same error when autogen doesn't know which spoker should be selected.
4. It is critical to manage the group chat and keep the conversation details within the group. Only return the result to the requestor.
5. This leads me to nested_chat and state_of_mind agent.
6. For example, product manager may not need to be aware of the code_executor agent or code reviewer. In such a case, it may be better to keep the coding conversation within a nested chat or a state-of-mind agent. Product manager only needs to know the output of executing the code.
