import os

import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder

config_file_or_env = "OAI_CONFIG_LIST"
llm_config = {"temperature": 0}
config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4o", "gpt-4-turbo"]})

# populate api_key from the env variables
# for config in config_list: 
#     config["api_key"] = os.getenv(config["api_key"])
#

def start_task(execution_task: str, agent_list: list, coding=True):
    group_chat = autogen.GroupChat(
        agents=agent_list,
        messages=[],
        max_round=12,
        allow_repeat_speaker=agent_list[:-1] if coding is True else agent_list,
    )
    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": config_list, **llm_config},
    )
    agent_list[0].initiate_chat(manager, message=execution_task)


builder = AgentBuilder(
    config_file_or_env=config_file_or_env, builder_model=["gpt-4-turbo"], agent_model=["gpt-4o"]
)


# building_task = """
# Generate some agents that can find papers on arxiv by programming and analyzing them in specific domains related to computer science and medical science.
# """
building_task = """
    Find 'iPhone 15' products from the inventory website: https://mpk-inventory.azurewebsites.net/
    Please refer to the website OpenAPI specification at https://raw.githubusercontent.com/jaredlang/sample-services/refs/heads/main/inventory/inventory-query-service-api-spec.yaml
    """ 

agent_list, agent_configs = builder.build(building_task, llm_config)

start_task(
    execution_task="Find a recent paper about gpt-4 on arxiv and find its potential applications in software.",
    agent_list=agent_list,
    coding=agent_configs["coding"],
)