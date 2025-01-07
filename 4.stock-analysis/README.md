# Observation on 4.stock-analysis

This app is based on <https://microsoft.github.io/autogen/0.2/docs/tutorial/code-executors>.

## Code Generation

1. The code generation is still pretty poor with gpt-4.
  a. The generated code is in \code-gen\plot_stock_gains_with_GPT-4o.py.
2. I had to specifically tell it "When you need to retrieve stock prices, use the yfinance python library"
3. When executing the pip install, it times out. Not sure why? I was able to manually run the install command on the docker container.
  a. the command line doesn't leave any log. It is hard to troubleshoot.
  b. I increased the timeout setting to 60s and the installation was successful.
4. The timeout error throws the code-writer-agent off. It made the code worse. I had to tell it to use the previous version.
  b. just like junior developers :)
5. After switching to gpt-4o, it was able to write the correct code. How can I use a non-OpenAI model?
6. When running it for the second time, the code-writer still uses the non-existing field name 'Adj Close'.
7. After I installed the libs and switched to gpt-4o, it was able to plot the stock gains properly.
8. It is always safer to use the Docker execution than the local execution.

## Training Course on deeplearning.ai

L5_Coding_and_Financial_Analysis.ipynb is from <https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/lesson/6/coding-and-financial-analysis>.

- It shows the system prompt of AssistantAgent. **Reading the system prompt is a great way to learn how to write an effective prompt.** And you can customize the system message for specific tasks.

```python
code_writer_agent_system_message = code_writer_agent.system_message
print(code_writer_agent_system_message)
```

- It also demostrates how to **instruct the agent to use pre-written functions**, which allows collaboration between human coders and the code writing agent.

```python
executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding",
    functions=[get_stock_prices, plot_stock_prices],
)
code_writer_agent_system_message += executor.format_functions_for_prompt()
print(code_writer_agent_system_message)
```

- The user-written functions need to have **detailed descriptions on its input and output as well as the purpose**. What happens if the user-written function is too? It would be better to wrap it into a web service. The agent can write additional code complementary with the given functions.

```python
def get_stock_prices(stock_symbols, start_date, end_date):
    """Get the stock prices for the given stock symbols between the start and end dates.

    Args:
        stock_symbols (str or list): The stock symbols to get the prices for.
        start_date (str): The start date in the format 'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
    
    Returns:
        pandas.DataFrame: The stock prices for the given stock
        symbols indexed by date, with one column per stock symbol.
    """
    import yfinance

    stock_data = yfinance.download(
        stock_symbols, start=start_date, end=end_date
    )
    return stock_data.get("Close")
```
