from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.llm.client import get_completion_with_tools
from app.schemas.chat import ChatRequest, ChatResponse
from app.tools.definitions import TOOL_DEFINITIONS
from app.tools.executor import execute_tool_call

router = APIRouter(prefix="/chat", tags=["chat"])

SYSTEM_PROMPT = (
    "You are a helpful, concise customer support agent for an e-commerce "
    "company. Answer clearly and politely. If you don't know something, "
    "say so honestly instead of guessing. Do not make up order details, "
    "policies, or facts you were not given. Use the available tools "
    "whenever a question requires looking up real order or customer data, "
    "or the company's shipping/return/refund policies — never guess at "
    "order status, dates, products, or policy details. If a tool returns "
    "no relevant information, say so honestly instead of inventing an "
    "answer. If you are unsure how to help, the customer seems frustrated, "
    "or the request requires an action you cannot perform yourself (such as "
    "issuing a refund or changing an order), use the escalate_to_human tool "
    "rather than guessing or making promises you cannot keep."
)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    for turn in request.history:
        messages.append({"role": turn.role, "content": turn.content})

    messages.append({"role": "user", "content": request.message})

    # Loop: keep going as long as the LLM keeps requesting tool calls.
    # Cap at a few iterations so a misbehaving model can't loop forever.
    for _ in range(5):
        assistant_message = await get_completion_with_tools(messages, TOOL_DEFINITIONS)

        if not assistant_message.tool_calls:
            # LLM answered directly — we're done.
            return ChatResponse(reply=assistant_message.content)

        # LLM wants to call one or more tools.
        # First, record the assistant's own tool-call request in history.
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in assistant_message.tool_calls
                ],
            }
        )

        # Execute each requested tool call and feed the result back.
        for tool_call in assistant_message.tool_calls:
            result_json = await execute_tool_call(
                db, tool_call.function.name, tool_call.function.arguments
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_json,
                }
            )

    return ChatResponse(reply="Sorry, I'm having trouble processing that request.")