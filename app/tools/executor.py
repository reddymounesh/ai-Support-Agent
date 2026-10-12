import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.tools.escalation_tools import escalate_to_human
from app.tools.knowledge_tools import search_knowledge_base
from app.tools.order_tools import get_customer_orders, get_order_status

# Tools that need a DB session as their first argument.
_DB_TOOL_REGISTRY = {
    "get_order_status": get_order_status,
    "get_customer_orders": get_customer_orders,
    "escalate_to_human": escalate_to_human,
}

# Tools that are self-contained and don't need a DB session.
_STANDALONE_TOOL_REGISTRY = {
    "search_knowledge_base": search_knowledge_base,
}


async def execute_tool_call(db: AsyncSession, tool_name: str, arguments_json: str) -> str:
    """
    Safely execute a tool the LLM requested.
    Returns a JSON string (tool results are sent back to the LLM as text).
    """
    try:
        arguments = json.loads(arguments_json)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid arguments format from model"})

    try:
        if tool_name in _DB_TOOL_REGISTRY:
            result = await _DB_TOOL_REGISTRY[tool_name](db, **arguments)
        elif tool_name in _STANDALONE_TOOL_REGISTRY:
            result = await _STANDALONE_TOOL_REGISTRY[tool_name](**arguments)
        else:
            return json.dumps({"error": f"Unknown tool '{tool_name}'"})
    except TypeError as e:
        return json.dumps({"error": f"Invalid arguments for {tool_name}: {e}"})

    return json.dumps(result)