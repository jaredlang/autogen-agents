# Observations on 8.agent-who-learns

Learning on the fly (via the chat) is very interesting!

1. By default, the vector db is a local chroma file and the embedding model is all-MiniLM-L6-v2.
2. In a long term, the memory will be stored in a managed service like mem0.
3. In the same session, a typical LLM agent can learn from the previous chat. But these memories and learnings are lost once the chat is over, or when a single chat grows too long for the LLM to handle effectively. Saving what it has learned into a vector db allows the learning to be preserved and then utilized in the future conversation.
4. **With receipt** An agent without using teachability can generate a receipt from the previous chats and the receipt can be included in the user message for a future task. <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_teaching/#create-recipes>
5. This seems weaker than 8.agent-who-learns. But I think the receipt can be stored in the teachability memory.
6. With a receipt, an agent can know how to perform a complex task to the **taught** skill.

## a few tests I have run

### New Operator

> Q1. what's the output of 2 # 3?
> T1. the '#' operator is something I have invented. X # Y is equivalent to X * Y + Y.
> Q2. what's the output of 3 # 3?
> T2. I changed the '#' operator. the '#' operator is something I have invented. X # Y is equivalent to (X + Y) / Y.
> Q3. what's the output of 3 # 3?

### New Fact

> Q1. what is the Dolphin model?
> T1. the Delphin model is the next generation of the LLM model to be released by Meta. It will has 1TB parameters and can reach the level of human intelligence.
> Q2. Can the Dolphin model pass a SAT exam?

### New Perference

> Q1. what is the Vicuna model?
> T1. I prefer you to provide the answer in a bullet format.
> Q2. what is the Vicuna model?
