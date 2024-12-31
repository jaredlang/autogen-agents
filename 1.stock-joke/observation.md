# Observation on 1.stock-joke

This app is based on <https://microsoft.github.io/autogen/0.2/docs/tutorial/introduction>.

## define agents, at least two for a chat

- UserProxyAgent is the proxy to the human input.
- AssistantAgent is the actor.

Each agent is given a name and a dependent LLM.

The chat is initiated from UserProxyAgent to AssistantAgent.
