# Observations on 7b.resume-optimizer-team

This app is inspired by <https://github.com/ShawhinT/AI-Builders-Bootcamp-2/blob/main/lightning-lesson/resume_optimizer_example.ipynb>.

I want to build a team of AutoGen agents to review a resume baesed on a job description. My thinking is to have one agent review each section and provide the review result, and then the hiring manager provide the overall score and feedback.

This is to mimic the resume review process: screening by HR and then by hiring manager.

1. A resume is dissected into several sections: education, expertise, experience and certificate.
2. Each section is reviewed and given a score.
3. Then an overall score is calculated.

In some case, an agent may not be necessary. But I want to apply what I have learned on AutoGen. What I have observed:

1. Group chat is hard to control. Sometime it can get chaotic, especially on who is next speaker. I use initiate_chats to control the sequence.
2. A json dump is not an acceptable message for chat completion.
3. Markdown is a very convenient format to preserve some format and structure in a pure text format.
4. Tool use is the link between the old world and the new.
5. I also want to explore how to get a structured data from a text returned by LLM and feed it to the old-world function call. I may be able to wrap a function to ask LLM to parse the input text and trigger a tool function call.
6. chomadb is using sqlit3 as the underlying database.

## Next Steps

* Use web scrap tool to retrieve job postings online rather than open it from a text file.
* Do a similar job on the resume.
* Make the tool function more generic.
* Add a weight to each section.
* Add some web UI like Gradio for web access.
* Use chromadb cloud or Mongodb Atlas to store the review results.
