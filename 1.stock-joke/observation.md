# Observation on 1.stock-joke

## define agents, at least two for a chat

- UserProxyAgent is the proxy to the human input.
- AssistantAgent is the actor.

Each agent is given a name and a dependent LLM.

The chat is initiated from UserProxyAgent to AssistantAgent.
