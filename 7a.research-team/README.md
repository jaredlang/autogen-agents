# Observations on 7a.Research Team

The research team is another use case of a group chat, similar to the dev team. This is based on <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_research#create-group-chat-without-critic-for-comparison>

The team is made up of agents with specific roles. It is to go through a typical research workflow: planning, review, create and execute.  

## Changes on the existing Source Code

The changes I added to the AutoGen example.

1. Change the local code executor to the docker executor.
2. Refine the prompt to include the library installation.
3. Add AgentOps for tracking and tracing.
4. Tried to use Claude in the Engineer agent, but got the Overloaded error.

## Training Course in Deeplearning.ai

One of the downsides with a group chat is the uncertainty of the speaker selection. It depends on the group chat manager. When the conversation gets longer, the manager is less likely able to select a speaker appropriately. 

- <L6-Planning_and_Stock_Report_Generation.ipynb> demonstrates how the speaker transition can be specified with a disallowed or allowed dictionary.

```python
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, writer, executor, planner],
    messages=[],
    max_round=10,
    allowed_or_disallowed_speaker_transitions={
        user_proxy: [engineer, writer, executor, planner],
        engineer: [user_proxy, executor],
        writer: [user_proxy, planner],
        executor: [user_proxy, engineer, planner],
        planner: [user_proxy, engineer, writer],
    },
    speaker_transitions_type="allowed",
)
```

- <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_customized/> demonstrates how the speaker transition logic is capsulated in a function. This can be the most controlled.

```python
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor],
    messages=[],
    max_round=20,
    speaker_selection_method=custom_speaker_selection_func,
)

def custom_speaker_selection_func(last_speaker: Agent, groupchat: autogen.GroupChat):
    """Define a customized speaker selection function.
    A recommended way is to define a transition for each speaker in the groupchat.

    Returns:
        Return an `Agent` class or a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
    """
    messages = groupchat.messages

    if len(messages) <= 1:
        return planner

    if last_speaker is user_proxy:
        if "Approve" in messages[-1]["content"]:
            # If the last message is approved, let the engineer to speak
            return engineer
        elif messages[-2]["name"] == "Planner":
            # If it is the planning stage, let the planner to continue
            return planner
        elif messages[-2]["name"] == "Scientist":
            # If the last message is from the scientist, let the scientist to continue
            return scientist

    elif last_speaker is planner:
        # Always let the user to speak after the planner
        return user_proxy

    elif last_speaker is engineer:
        if "```python" in messages[-1]["content"]:
            # If the last message is a python code block, let the executor to speak
            return executor
        else:
            # Otherwise, let the engineer to continue
            return engineer

    elif last_speaker is executor:
        if "exitcode: 1" in messages[-1]["content"]:
            # If the last message indicates an error, let the engineer to improve the code
            return engineer
        else:
            # Otherwise, let the scientist to speak
            return scientist

    elif last_speaker is scientist:
        # Always let the user to speak after the scientist
        return user_proxy

    else:
        return "random"
```
