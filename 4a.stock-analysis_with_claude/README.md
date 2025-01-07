# Observation on 4.accounting

This app is based on <https://microsoft.github.io/autogen/0.2/docs/tutorial/code-executors>.

## Code Generation

1. Compared with gpt-4o the claude dev is noticeably better!
  a. The code is better structured, including the comments.
  b. It looks like some developers would have written the code.
  c. It also gets the field name 'Close' right at the first time.
  d. It plots the percentage, which is a nice touch.
  e. The generated code is in \code-gen\plot_stock_gains_with_Claude-3.5.py.
2. code_executor_agent doesn't consume any OpenAI credit.
3. Using Claude LLM is just like using GPT models. Good job, AutoGen!
