# extract the content related to a given topic from a resume
import asyncio
import os
import json
from datetime import datetime

import mammoth
from markdownify import markdownify
from apify_client import ApifyClient

import chromadb

from typing import Annotated

from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from autogen import register_function
from autogen import Cache

gpt4o_llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ],
    "temperature": 0.1,  # fact-based responses
}

# NO trailing slash
RESUME_FILE_STORE = "./resume-test-data"
REVIEW_DB_PATH = "./resume-test-data/review-db"

# open a web page
def Scrape_web_page(
    url: Annotated[str, "The URL of the web page to scrape"]
) -> Annotated[str, "Scraped content"]:
    # Initialize the ApifyClient with your API token
    client = ApifyClient(token=os.getenv("APIFY_API_TOKEN"))

    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": url}],
        "useSitemaps": False,
        "crawlerType": "playwright:firefox",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "ignoreCanonicalUrl": False,
        "maxCrawlDepth": 0,
        "maxCrawlPages": 1,
        "initialConcurrency": 0,
        "maxConcurrency": 200,
        "initialCookies": [],
        "proxyConfiguration": {"useApifyProxy": True},
        "maxSessionRotations": 10,
        "maxRequestRetries": 5,
        "requestTimeoutSecs": 60,
        "dynamicContentWaitSecs": 10,
        "maxScrollHeightPixels": 5000,
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
        "removeCookieWarnings": True,
        "clickElementsCssSelector": '[aria-expanded="false"]',
        "htmlTransformer": "readableText",
        "readableTextCharThreshold": 100,
        "aggressivePrune": False,
        "debugMode": True,
        "debugLog": True,
        "saveHtml": True,
        "saveMarkdown": True,
        "saveFiles": False,
        "saveScreenshots": False,
        "maxResults": 9999999,
        "clientSideMinChangePercentage": 15,
        "renderingTypeDetectionPercentage": 10,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    text_data = ""
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        text_data += item.get("text", "") + "\n"

    average_token = 0.75
    max_tokens = 20000  # slightly less than max to be safe 32k
    text_data = text_data[: int(average_token * max_tokens)]
    return text_data

# resume converter (convert pdf to markdown)
def convert_word_to_markdown(
    word_file_path: Annotated[str, "the file path of a word document"],
    markdown_file_path: Annotated[str, "the file path of a markdown document"],
) -> str:
    # intermediary html file
    tmp_html_file_path = markdown_file_path + ".html"
    # convert
    with open(word_file_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value  # The generated HTML
        messages = result.messages  # Any messages, such as warnings during conversion
        with open(tmp_html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(html)

    with open(tmp_html_file_path, "r") as html_file:
        html = html_file.read()
        markdown = markdownify(html)
        with open(markdown_file_path, "w") as md_file:
            md_file.write(markdown)
        return markdown

# open a text file
def open_text_file(
    text_file_path: Annotated[str, "the file path of a text document"]
) -> str:
    with open(text_file_path, "r") as f:
        return f.read()

is_termination_msg = lambda x: x.get("content", "") and x.get(
    "content", ""
).rstrip().endswith("TERMINATE")

user_proxy = UserProxyAgent(
    "user_proxy",
    llm_config=gpt4o_llm_config,
    system_message="""
    Reply "TERMINATE" in the end when everything is done.
    """,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)

resume_extractor = AssistantAgent(
    "resume_extractor",
    llm_config=gpt4o_llm_config,
    system_message="""
    You extract the content related to a given topic from a resume. The resume is in the markdown format.
    Reply "TERMINATE" in the end when everything is done.
    """,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)

resume_reviewer = AssistantAgent(
    "resume_reviewer",
    llm_config=gpt4o_llm_config,
    system_message="""
    You review the qualification based on the given job requirements. 
    You must provide a score between 0 and 10 based on the match between the qualification and the job requirements. 0 means no match and 10 means a perfect match.
    If the score is lower than 5, you must provide the reasons and the feedback on how to improve the match.
    Reply "TERMINATE" in the end when everything is done.
    """,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)

register_function(
    convert_word_to_markdown,
    caller=resume_extractor,
    executor=user_proxy,
    name="convert_word_to_markdown",
    description="Convert a word document to a text in the markdown format",
)

register_function(
    open_text_file,
    caller=resume_reviewer,
    executor=user_proxy,
    name="open_local_text_file_for_job_requirement",
    description="Open a local text file for job requirements",
)

register_function(
    Scrape_web_page,
    caller=resume_extractor,
    executor=user_proxy,
    name="Scrape_web_page_for_job_requirements",
    description="Scrape a web page for job requirements",
)

# screening_group_chat = GroupChat(
#     agents=[user_proxy, resume_extractor, resume_reviewer], messages=[], max_round=50
# )

# screening_manager = GroupChatManager(
#     groupchat=screening_group_chat,
#     name="Screening_manager",
#     llm_config=gpt4o_llm_config,
#     code_execution_config=False,
#     is_termination_msg=is_termination_msg,
# )

# user = UserProxyAgent(
#     name="User",
#     human_input_mode="NEVER",
#     llm_config=gpt4o_llm_config,
#     code_execution_config=False,
#     is_termination_msg=is_termination_msg,
# )

hiring_manager = AssistantAgent(
    name="Hiring_manager",
    llm_config=gpt4o_llm_config,
    system_message="""
    You are the hiring manager. You need to evaluate the feedback from the resume reviewer and calculate the overall score of the resume.
    between 0 and 10 based on the match between the qualification and the job requirements. 0 means no match and 10 means a perfect match.
    ** If the overall score is less than 5, the next step is to reject the resume.
    ** If the overall score is between 5 and 7, the next step is to provide your reasons why the resume is not a good match.
    ** If the overall score is more than 7, the next step is to recommend an interview and include the reason why the resume is not a good match.
    Reply "TERMINATE" in the end when everything is done.
    """,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)


# start chat
def extract_content(topic: str, resume_path: str) -> str:
    # "Give me the path to the resume and the topic you want to extract."
    chat_result = user_proxy.initiate_chat(
        resume_extractor,
        message=f"extract the content related to {topic} from this resume, {resume_path}",
    )


# create the task description
def create_extraction_task(topic: str, resume_path: str) -> str:
    return f"Extract the content related to {topic} from the resume. The resume file is in the markdown format and located at {resume_path}."


def create_review_task(job_requirement_path: str, job_requirement_format: str) -> str:
    return f"""Review the qualification and based on the given job requirement. 
    The job requirement file is in the {job_requirement_format} format and located at {job_requirement_path}."""


def review_resume(
    topic: str,
    resume_path: str,
    job_requirement_path: str,
    job_requirement_format: str = "text",
) -> str:

    screening_tasks = [
        create_extraction_task(topic, resume_path),
        create_review_task(job_requirement_path, job_requirement_format),
    ]

    # refer to https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_multi_task_chats.ipynb
    with Cache.disk() as cache:
        # asyncio.run(
        chat_results = user_proxy.initiate_chats(  # noqa: F704
            [
                {
                    "chat_id": 1,
                    "recipient": resume_extractor,
                    "message": screening_tasks[0],
                    "cache": cache,
                    "summary_method": "last_msg",
                },
                {
                    "chat_id": 2,
                    "prerequisites": [1],
                    "recipient": resume_reviewer,
                    "message": screening_tasks[1],
                    "cache": cache,
                    "summary_method": "reflection_with_llm",
                },
            ]
        )
        # )
        # print(chat_results)

        # save the chat results into Chromadb
        resume_review_result = chat_results[-1].chat_history[-1]["content"]

        return resume_review_result


def store_to_memory(
    candidate_id: str,
    review_topic: str,
    review_result: dict,
    hiring_company: str,
    open_position: str,
):
    client = chromadb.PersistentClient(path=REVIEW_DB_PATH)

    collection = client.get_or_create_collection(name=hiring_company)

    collection.upsert(
        documents=[review_result],
        metadatas=[
            {
                "review_topic": review_topic,
                "open_position": open_position,
                "hiring_company": hiring_company,
                "candidate_id": candidate_id,
                "review_date": datetime.now().isoformat(),
            }
        ],
        ids=f"{hiring_company}-{open_position}-{candidate_id}-{review_topic}",
    )


def query_from_memory(
    candidate_id: str, review_topic: str, hiring_company: str, open_position: str
):
    client = chromadb.PersistentClient(path=REVIEW_DB_PATH)

    collection = client.get_collection(name=hiring_company)

    return collection.get(
        ids=f"{hiring_company}-{open_position}-{candidate_id}-{review_topic}"
    )


def evaulate_feedback(candidate_id: str, hiring_company: str, open_position: str):

    review_result_long_text = "CONTEXT: "

    for topic in review_topics:
        review_result_long_text += f"\n\n [FEEDBACK on {topic}] \n\n"
        review_result = query_from_memory(  # query the result from Chromadb
            candidate_id,
            topic,
            hiring_company,
            open_position,
        )
        review_result_long_text += "\n\n".join(review_result["documents"])

    with Cache.disk() as cache:
        chat_result = user_proxy.initiate_chat(
            hiring_manager, silent=False, message=review_result_long_text, cache=cache
        )

        # save the chat results into Chromadb
        evaluation_result = chat_result.chat_history[-1]["content"]

        return evaluation_result


if __name__ == "__main__":

    review_topics = ["education", "expertise", "work experience", "certificate"]

    resumes = [
        {
            "path": f"{RESUME_FILE_STORE}/resumes/test-word.docx",
            "format": "docx",
            "candidate_id": "candidate-123",
        }
    ]

    job_requirements = [
        {
            "path": f"{RESUME_FILE_STORE}/job-requirements/nova-jd.txt",
            "format": "text",
            #     "https://www.indeed.com/viewjob?jk=fc7efa4613deaaa9&from=shareddesktop",
            #     "web page",
            "open_position": "data-scientist",
            "hiring_company": "nova",
        }
    ]

    for job_requirement in job_requirements:
        for resume in resumes:
            for topic in review_topics:
                # extract_content(topic, resume)
                review_result = review_resume(
                    topic, resume["path"], job_requirement["path"]
                )
                # save the result to Chromadb
                store_to_memory(
                    resume["candidate_id"],
                    topic,
                    json.dumps(review_result),
                    job_requirement["hiring_company"],
                    job_requirement["open_position"],
                )

    for job_requirement in job_requirements:
        for resume in resumes:
            # get the overall evaluation result
            evaluation_result = evaulate_feedback(
                resume["candidate_id"],
                job_requirement["hiring_company"],
                job_requirement["open_position"],
            )
            # save the result to Chromadb
            store_to_memory(
                resume["candidate_id"],
                "overall",
                json.dumps(evaluation_result),
                job_requirement["hiring_company"],
                job_requirement["open_position"],
            )
