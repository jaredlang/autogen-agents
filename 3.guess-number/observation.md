# Observation on 2.comedian-duo

This app is based on <https://microsoft.github.io/autogen/0.2/docs/tutorial/human-in-the-loop>.

## How does a human input participate in a chat?

On each agent, set human_input_mode

- ALWAYS. Ask for a human input every time when an agent sends a response.
- NEVER. Never ask for a human input.
- TERMINATE. Ask for a human input before terminating the chat.
