# Observations on 7c.blogpost-writing-team

This app uses nested chats to gather feedback from a team of reviewers. I can use this conversation pattern in 7b.resume-optimizer-team.
It also be used in the podcast creation, fraud detection, document validation and etc..

## Training Course on deeplearning.ai

<https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/4/reflection-and-blogpost-writing>

1. A nested chat is a 'silo' conversation within a team. This use case is perfect.
2. The nested chat is 'hidden' from the writer, but the writer is the trigger for critic.
3. The critic agent becomes a mere relay between writer and a team of reviewers.
4. The json format adds some structure to the feedback text, especially when the text comes from multiple reviewers.
5. Make sure no space is the agent name. Otherwise it would cause *Invalid 'messages[0].name* when using *reflection_with_llm*.
6. AgentOps has a conflicting version of the open-telemetry libs. But it seems working fine.
