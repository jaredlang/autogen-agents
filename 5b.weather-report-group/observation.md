# Observations on 5b.weather-report-group

I invited an expert of measurement (metrologist) into the chat. He is going to tell us what the local units of measure are in a given location. 

## Conversation Sequence

```mermaid
sequenceDiagram
user_proxy ->> meteorologist: What's the weather like in Houston?
meteorologist -->> user_proxy: ~Need to use the weather tool.~
meteorologist ->> get_local_units: argument-"Houston"
get_local_units -->> meteorologist: local units of measure
meteorologist ->> get_weather: argument-"Houston"
get_weather -->> meteorologist: weather data in json
meteorologist --x user_proxy: human readable weather report
```
