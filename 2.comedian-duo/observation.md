# Observation on 2.comedian-duo

This app is based on <https://microsoft.github.io/autogen/0.2/docs/tutorial/chat-termination>.

## How to control the termination of a chat?

On each agent, set the termination config.

- is_termination_msg. A critiera is defined as a function and determine if a chat is to be terminated.
- max_consecutive_auto_reply. The max number of auto replies.
- max_turns. The max number of times an agent speaks.
