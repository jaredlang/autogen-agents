# Observations on 6a.mental-consular

## A different Use Case

Technically this is almost identical to 6.customer-service. But this is a different use case. Customer Service is more fact search, which requires a quick and accurate response. 6a.mental-consular requires a gentle and compassionate conversation. It needs more language skills and a broad knowledge in general.

I also add AgentOps to visualize how the health_consular agent and the care_bot are communicating with each other. In this case, the health_consular agent is merely a user proxy who relays the patient's response to care_bot and adds the patient into the conversation.

## Observations

1. AgentOps is not able to capture the agent names. It just labels them as default agents.
2. Memory initial loading has a slight delay with just a few lines of a conversation.
3. Compared with RAG, the chat history is very personal. RAG usually is new info and non-personal. But I still feel like one storage service should and care support both.
