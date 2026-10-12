from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessage

from app.config import settings

_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)


async def get_chat_completion(messages: list[dict[str, str]]) -> str:
    """
    Send a list of chat messages to the LLM via OpenRouter and return the
    assistant's reply text. No tool-calling support (used by simple flows).
    """
    response = await _client.chat.completions.create(
        model=settings.openrouter_model,
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content


async def get_completion_with_tools(
    messages: list[dict], tools: list[dict]
) -> ChatCompletionMessage:
    """
    Send messages + available tool definitions to the LLM.
    Returns the raw assistant message object, which may contain either:
      - plain text content (message.content), or
      - one or more tool call requests (message.tool_calls)
    The caller is responsible for inspecting which one it got.
    """
    response = await _client.chat.completions.create(
        model=settings.openrouter_model,
        messages=messages,
        tools=tools,
        temperature=0.6,
    )
    return response.choices[0].message