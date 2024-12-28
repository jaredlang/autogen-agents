# Observation on 5.Calculator

## register_function

Why does it need to register with two agents? Because

- the one (caller) needs to understand the tool enough to suggest using it.
- the other (executor) needs to understand the tool to execute it.

## define function

The tool schema is derived from the function signature. It is important to provide a concise and clear description.
If needed, you can use pydentic to define the tool schema with additional details.

## Annotation

Annotated is something new.

```python
Annotated[Operator, "operator"]
```
