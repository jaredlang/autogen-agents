# Observations on 5b.weather-report-group

I invited an expert of measurement (metrologist) into the chat. He is going to tell us what the local units of measure are in a given location.

## Conversation Sequence (intended)

```mermaid
sequenceDiagram
user_proxy ->> metrologist: what are the local units of measure in Beijing?
metrologist -->> user_proxy: ~the local units~
user_proxy --> meteorologist ->> Describe the weather in Beijing using its local standard units of measure.
meteorologist ->> get_weather: argument-"Beijing" argument-"metric" 
get_weather -->> meteorologist: weather data in json
meteorologist --x user_proxy: human readable weather report
```

## Observations

1. metrologist's input is not taken in consideration.
  a. Even after I comment out the metrologist, it doesn't affect the response.
  b. meteorologist is able to infer the local standard unit by itself.
  c. It makes the LLM reply in the local units by adding to the system prompt "using its local standard units of measure." I found out this from its LLM context. Need to speak its language for a quality response, just like a human.
2. There are great similiarities to a conversation among humans.

## Need a different use case for group chats

1. where the second chat requires the output of the first one.
2. it is necessary to use multiple tools

## Add cache

1. This is a huge cost saver for learning and debugging.
2. AutoGen cache is deterministic, unlike OpenAI's seed. Here is the [reference](https://microsoft.github.io/autogen/0.2/docs/topics/llm-caching#difference-between-cache_seed-and-openais-seed-parameter)

## Add AgentOps for Observability

1. LangSmith is also promoted for observability. AgentOps is a direct competitor.
2. AgentOps is sooo simple to use. Instrumentation is not intrusive and takes 3 lines of code.
3. The drilldown dashboard is intutive and very easy to track all activities, agents and flows.
4. So much better than LangSmith. I love it!

## Add AutoGen Runtime logging

1. AutoGen has a structured way of logging.
2. What AgentOps displays comes from the runtime logging. AgentOps gives a nice UI and an easy way to explore.
3. AgentOps also supports other agent frameworks too. But they are based on similar data models. The instructmentation layer is different.
4. What a smart way to start up.
