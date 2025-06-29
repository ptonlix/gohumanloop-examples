# GoHumanLoop Example with LangGraph

This example shows how to use the GoHumanLoop package to create a LangGraph agent that augments human control.

## Example List

- Basic example - [langgraph_adapter_example.py](./langgraph_adapter_example.py)
- Conversational example - [langgraph_conversational_example.py](./langgraph_conversational_example.py)
- Mutil-provider example - [langgraph_multi_provider_example.py](./langgraph_multi_provider_example.py)
- LangGraph "interrupt" simple example - [langgraph_interrupt_example.py](./langgraph_interrupt_example.py)
- Gohumanloop callback example - [langgraph_callback_example.py](./langgraph_callback_example.py)
- Gohumanloop wework example - [langgraph_wework.py](./langgraph_wework.py)

## Start

1. Install uv

Go to installation guide: https://github.com/astral-sh/uv

2. Create a `.env` file with your API key:

```bash
cp .env.example .env
```

3. Run the example:

```bash
cd ./LangGraph

uv run langgraph_adapter_example.py
```

## License

This project is released under the MIT License.
