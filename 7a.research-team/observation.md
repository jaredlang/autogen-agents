# Observations on 7a.Research Team

The research team is another use case of a group chat, similar to the dev team. This is based on <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_research#create-group-chat-without-critic-for-comparison>


The team is made up of agents with specific roles. It is to go through a typical research workflow: planning, review, create and execute.  

## Changes on the existing Source Code

The changes I added to the AutoGen example.

1. Change the local code executor to the docker executor.
2. Refine the prompt to include the library installation.
3. Add AgentOps for tracking and tracing.
4. Tried to use Claude in the Engineer agent, but got the Overloaded error.
