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

## Training Course in Deeplearning.ai

<https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/7/planning-and-stock-report-generation>

- **system_message** is an instruction on how an agent should behave, which is accessible to the agent itself. **description** is a description of what the agent is. That infomration is visible to other agents and group chat manager. Imagine that *description* is the signature of a python function (input, output and what it does) while *system_message* is the internal logic of how it completes the task.
