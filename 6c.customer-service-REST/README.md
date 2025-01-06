# Observations on 6c. Customer Service with REST

This app is built with a brief that very few organizations allow sql agent to query the database directly. From my experience, the data model is often quite complex and the table and field names are often cryptic. With a wave of API enablement, the API is often external-facing and very well-documented. I think an agent is more useful if it can understand the api specs and talk with the API services.

I approached the agent framework as a developer. An agent is like a simple service. I send a request and get a response. The difference is that the language is a natural language instead of a programming language. Natural languages are not quite accurate or reliable. Is there more than that?

I believe QA is the main way to communicate with the agents. That's the most natural way to communicate. If we expect the agents to produce app UIs at the same quality as the human, the AI has a long way to go. And that's unnecessary. If an agent can tell me what I need to know, why will I need a nice computer UI like today's apps?

## app-flat.py

1. This app is based on <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_auto_feedback_from_code_execution>.
2. When "user assistant" is assigned to the name of user_proxy, the app throws an error. see [user-assistant-error-msg.txt](./user-assistant-error-msg.txt). Why???
3. The error is gone when I used "user_proxy" or "boss". Is "Assistant" a reserved word?
4. I also noticed the same error when autogen doesn't know which spoker should be selected.
5. Agents in app-flat.py are flat-structured. One big group.
6. It is critical to manage the group chat and keep the conversation details within the group. Only return the result to the requestor.
7. This leads me to nested_chat and state_of_mind agent.
8. For example, product manager may not need to be aware of the code_executor agent or code reviewer. In such a case, it may be better to keep the coding conversation within a nested chat or a state-of-mind agent. Product manager only needs to know the output of executing the code.

## app-som.py

1. It is based on this example <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_society_of_mind>
2. Introduce a dev manager that "contain" the dev chat within the dev agents, and report the result to user_proxy.
3. Keep getting the mysterious errors. See [som-eng-error-msg.txt](./som-eng-error-msg.txt) when using only engineer.
4. A similar error. See [som-pm-error-msg.txt](./som-pm-error-msg.txt) when adding product manager.

## app-flat.py update-1

1. try a more complex task. GPT4o failed with the error [add-product-error-msg.txt](./add-product-error-msg.txt), while **Claude scored**!

> Add a new product (manufacturer: Xiaomi, product: dragon-01) to the inventory website: https://mpk-inventory.azurewebsites.net/products
> Please refer to the website OpenAPI specification at https://raw.githubusercontent.com/jaredlang/sample-services/refs/heads/main/inventory/inventory-query-service-api-spec.yaml

## app-som.py update-1

1. SOM is executed successfully on Claude too. Claude rocks!
2. What's going on OpenAPI?

## app-nested.py

1. This app is based on <https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nestedchat>.
2. I added code_executor_proxy, which is nothing about a proxy to software engineer.
3. The app works with Claude after several rounds. The nested chat is totally unecessary.

## app-flat.py update-2

1. I remove product_manager and keep only three participants: user_proxy, engineer and code_executor.
2. The engineer agent is able to understand the request.
3. It shows the criticality of having the right people in a conversation.
4. Azure free-tier web app returns an error message because of throttling, which gets the agent confused. It kept modifying the code and then trying again, which made the situation worse.
5. I also noticied some assumptions made by Claude.
  a. Claude keeps assuming the requests lib be installed. I had to manually run the installation on the docker container.
  b. Claude assumes the api spec have the query parameters in the component definition.
  c. Rather than use the component definition, Claude adds some non-existing fields like color, price. It is funny and annoying like developers trying to be smart.
  d. BUT at the end Claude was able to query the service and provide the correct answer, unlike GPT-4o.

## Next steps

1. API spec download and analysis are required for any API service call. It should be stored in the memory for the future use.
2. The requests lib is not included in the docker image. I wonder if it is possible to use some custom images with popular libs preloaded.
3. We all say AI gets better than we use it more because it can learn. How can an agent learn from the past conversation?
