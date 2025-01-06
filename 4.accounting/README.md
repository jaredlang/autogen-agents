# Observation on 4.accounting

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
