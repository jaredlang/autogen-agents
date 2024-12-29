# Observations on 6.customer-service

## memory for agents

Use [mem0](https://mem0.ai/) for memory storage. I had a difficulty to find a managed service for RAG and Long-term Memory, as well as the structured data storage. Mem0 seems having everything.

1. memory loading is kind of slow. Even with a short chat history, it takes about 30 seconds.
2. It is not good at being aware of the conversation context. For example,
  a. When I asked "What's my email address?", it could find relevant chat.
  b. My guess is that the user-side conversation has only an email address, but it is not in a complete sentence. But the context is pretty clear for any human.
  c. When I complete that sentence, it is able to find relevant chats in the memory.
  d. But what's nice about mem0 is that mem0 can improve its memory from the response.
  e. When relevant memory is not found, a human should step in and provide the answer and ingest it into the memory.
3. Cache is very useful. When it is a hit, the response is almost instant.
