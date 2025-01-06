# Observations on 7.Development Team

This app is based on <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_auto_feedback_from_code_execution>.

The dev team is made up of agents with specific roles.
It is to go through a typical real-world workflow: planning, review, create and execute.
Besides, it includes someone with access to confidential material. That's common in today's business world.

## How to utilize the RAG?

1. Use Chroma as Vector DB. The sqlite3 and other db files are under /tmp.
2. Add the agent with access to the confidential material into the chat.
3. Have another agent call that special agent.
4. Add a critic agent for quality check. Even though the quality is less reliable due to LLM, but the step is necessary.