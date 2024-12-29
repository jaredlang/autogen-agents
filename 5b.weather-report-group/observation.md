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
