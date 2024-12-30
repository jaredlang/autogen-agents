import os
import chromadb
from typing import Annotated

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen import runtime_logging

import agentops

llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}],
    "timeout": 60,
    "temperature": 0.8,
    "seed": 1234,
}

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


boss = UserProxyAgent(
    name="Boss",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    code_execution_config=False,  # we don't want to execute code in this case.
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    description="The boss who ask questions and give tasks.",
)

boss_aid = RetrieveUserProxyAgent(
    name="Boss_Assistant",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    default_auto_reply="Reply `TERMINATE` if the task is done.",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md",
        "chunk_token_size": 1000,
        "model": llm_config["config_list"][0]["model"],
        # "vector_db": "chroma", # use the default location
        # "embedding_model": "all-MiniLM-L6-v2",
        # "collection_name": "flaml_integrated_with_spark"
        # "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
    description="Assistant who has extra content retrieval power for solving difficult problems.",
)

coder = AssistantAgent(
    name="Senior_Python_Engineer",
    is_termination_msg=termination_msg,
    system_message="You are a senior python engineer, you provide python code to answer questions. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
    description="Senior Python Engineer who can write code to solve problems and answer questions.",
)

pm = AssistantAgent(
    name="Product_Manager",
    is_termination_msg=termination_msg,
    system_message="You are a product manager. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
    description="Product Manager who can design and plan the project.",
)

reviewer = AssistantAgent(
    name="Code_Reviewer",
    is_termination_msg=termination_msg,
    system_message="You are a code reviewer. Reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config,
    description="Code Reviewer who can review the code.",
)


def _reset_agents():
    boss.reset()
    boss_aid.reset()
    coder.reset()
    pm.reset()
    reviewer.reset()


def norag_chat(problem):
    _reset_agents()
    groupchat = GroupChat(
        agents=[boss, pm, coder, reviewer],
        messages=[],
        max_round=10,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=problem,
    )


def rag_chat(problem):
    _reset_agents()
    groupchat = GroupChat(
        agents=[boss_aid, pm, coder, reviewer],
        messages=[],
        max_round=10,
        speaker_selection_method="round_robin",
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss_aid as this is the user proxy agent.
    boss_aid.initiate_chat(
        manager,
        message=boss_aid.message_generator,
        problem=problem,
        n_results=3,
    )


def call_rag_chat(problem):
    _reset_agents()

    # In this case, we will have multiple user proxy agents and we don't initiate the chat
    # with RAG user proxy agent.
    # In order to use RAG user proxy agent, we need to wrap RAG agents in a function and call
    # it from other agents.
    def retrieve_content(
        message: Annotated[
            str,
            "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
        ],
        n_results: Annotated[int, "number of results"] = 3,
    ) -> str:
        boss_aid.n_results = n_results  # Set the number of results to be retrieved.
        _context = {"problem": message, "n_results": n_results}
        ret_msg = boss_aid.message_generator(boss_aid, None, _context)
        return ret_msg or message

    boss_aid.human_input_mode = (
        "NEVER"  # Disable human input for boss_aid since it only retrieves content.
    )

    # register_for_llm is to understand and create the source code.
    for caller in [pm, coder, reviewer]:
        d_retrieve_content = caller.register_for_llm(
            description="retrieve content for code generation and question answering.",
            api_style="function",
        )(retrieve_content)

    # register_for_execution is to instruct the source code to be executed.
    for executor in [boss, pm]:
        executor.register_for_execution()(d_retrieve_content)

    groupchat = GroupChat(
        agents=[boss, pm, coder, reviewer],
        messages=[],
        max_round=10,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
    )

    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message=problem,
    )


if __name__ == "__main__":

    problem = "How to use spark for parallel training in FLAML? Give me sample code."

    # Start logging
    logging_session_id = runtime_logging.start(config={"dbname": "call_rag_chat-logs.db"})
    print("Logging session ID: " + str(logging_session_id))

    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), default_tags=["autogen", "dev-team", "call_rag_chat"])

    call_rag_chat(problem)

    agentops.end_session("Success")

    runtime_logging.stop()
