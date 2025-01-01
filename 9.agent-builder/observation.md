# Observations on 9.agent-builder

This is an amazing idea to build a team of agents based on the given task.

Also it is useful to see the generated agents and their system messages (instructions and roles).

I tried the tasks given to 6c.customer service with REST service <./6c.customer-service-REST>, and learn how it generates agents to solve the same problem.

1. The builder generates ['API_Expert', 'WebScraping_Expert', 'YAML_Expert', 'InventoryManagement_Expert', 'ProductSearch_Expert']. Those are more than what I have used in 6c.
2. The auto-built agents were not able to give the correct answer.
3. WebScraping_Expert tried to use arxiv to find papers related to the task.

Besides, I am not a fan of using OAI_CONFIG_LIST. It has duplicate entries for the api key. It is not secure or suitable for key management.
