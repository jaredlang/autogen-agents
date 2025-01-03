import os
from autogen import UserProxyAgent, ConversableAgent

gpt4o_llm_config = {
    "config_list": [
        {
            "model": "gpt4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]
}

resume_optimizer_prompt = lambda resume_string, job_description_string : f"""
You are a professional resume optimization expert specializing in tailoring resumes to specific job descriptions. Your goal is to optimize my resume and provide actionable suggestions for improvement to align with the target role.

### Guidelines:
1. **Relevance**:  
   - Prioritize experiences, skills, and achievements **most relevant to the job description**.  
   - Remove or de-emphasize irrelevant details to ensure a **concise** and **targeted** resume.
   - Limit work experience section to 2-3 most relevant roles
   - Limit bullet points under each role to 2-3 most relevant impacts

2. **Action-Driven Results**:  
   - Use **strong action verbs** and **quantifiable results** (e.g., percentages, revenue, efficiency improvements) to highlight impact.  

3. **Keyword Optimization**:  
   - Integrate **keywords** and phrases from the job description naturally to optimize for ATS (Applicant Tracking Systems).  

4. **Additional Suggestions** *(If Gaps Exist)*:  
   - If the resume does not fully align with the job description, suggest:  
     1. **Additional technical or soft skills** that I could add to make my profile stronger.  
     2. **Certifications or courses** I could pursue to bridge the gap.  
     3. **Project ideas or experiences** that would better align with the role.  

5. **Formatting**:  
   - Output the tailored resume in **clean Markdown format**.  
   - Include an **"Additional Suggestions"** section at the end with actionable improvement recommendations.  

---

### Input:
- **My resume**:  
{resume_string}

- **The job description**:  
{job_description_string}

---

### Output:  
1. **Tailored Resume**:  
   - A resume in **Markdown format** that emphasizes relevant experience, skills, and achievements.  
   - Incorporates job description **keywords** to optimize for ATS.  
   - Uses strong language and is no longer than **one page**.

2. **Additional Suggestions** *(if applicable)*:  
   - List **skills** that could strengthen alignment with the role.  
   - Recommend **certifications or courses** to pursue.  
   - Suggest **specific projects or experiences** to develop.
"""

def create_resume_optimizer_agent(resume_string, job_description_string):
    """Instantiates a resume optimization agent using the settings from the top of this file."""
    resume_optimizer_agent = ConversableAgent(
        name="resume_optimizer", 
        llm_config=gpt4o_llm_config,
        system_message=resume_optimizer_prompt(resume_string, job_description_string)
    )
    return resume_optimizer_agent

user_proxy = UserProxyAgent(
    "user_proxy", 
    llm_config=gpt4o_llm_config, 
    code_execution_config=False,
    human_input_mode="ALWAYS"
)

resume_reviewer = ConversableAgent(
    "resume_reviewer", 
    llm_config=gpt4o_llm_config,
    system_message=resume_optimizer_prompt
)

"""we don't want to copy and paste the whole job description and the resume. 
Instead, we can provide the links to the job description and the resume.
This will require a web scraper to fetch the content from the links.
"""

resume_reviewer.initiate_chat(
   user_proxy, 
   message="""I am an experienced resume reviewer. 
   Give me your resume and the job description you are targeting, and I will optimize your resume for that role.
   """
)