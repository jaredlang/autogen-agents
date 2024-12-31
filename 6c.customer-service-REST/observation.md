# Observations on 6c. Customer Service with REST

## app-flat.py

1. When "user assistant" is assigned to the name of user_proxy, the app throws an error. see [user-assistant-error-msg.txt](./user-assistant-error-msg.txt). Why???
2. The error is gone when I used "user_proxy" or "boss". Is "Assistant" a reserved word?
3. I also noticed the same error when autogen doesn't know which spoker should be selected.
4. Agents in app-flat.py are flat-structured. One big group.
5. It is critical to manage the group chat and keep the conversation details within the group. Only return the result to the requestor.
6. This leads me to nested_chat and state_of_mind agent.
7. For example, product manager may not need to be aware of the code_executor agent or code reviewer. In such a case, it may be better to keep the coding conversation within a nested chat or a state-of-mind agent. Product manager only needs to know the output of executing the code.

## app-som.py

1. Introduce a dev manager that "contain" the dev chat within the dev agents, and report the result to user_proxy.
2. Keep getting the mysterious errors. See [som-eng-error-msg.txt](./som-eng-error-msg.txt) when using only engineer.
3. A similar error. See [som-pm-error-msg.txt](./som-pm-error-msg.txt) when adding product manager.

## app-flat.py update-1

1. try a more complex task. GPT4o failed with the error [add-product-error-msg.txt](./add-product-error-msg.txt), while **Claude scored**!

> Add a new product (manufacturer: Xiaomi, product: dragon-01) to the inventory website: https://mpk-inventory.azurewebsites.net/products
> Please refer to the website OpenAPI specification at https://raw.githubusercontent.com/jaredlang/sample-services/refs/heads/main/inventory/inventory-query-service-api-spec.yaml

## app-som.py update-1

1. SOM is executed successfully on Claude too. Claude rocks!
2. What's going on OpenAPI?
