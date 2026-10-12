TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": (
                "Get the current status, product, and delivery info for a "
                "single order by its order ID. Use this when the customer "
                "asks about a specific order (e.g. 'where is my order #12')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The numeric ID of the order to look up.",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_orders",
            "description": (
                "Get a list of all orders belonging to a customer, by "
                "customer ID. Use this when the customer asks about their "
                "orders in general, not one specific order."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The numeric ID of the customer.",
                    }
                },
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search the company's policy documents (shipping, returns, "
                "refunds, and FAQs) for information relevant to a customer's "
                "question. Use this for general policy questions like "
                "'what is your refund policy' or 'how do returns work' — "
                "NOT for questions about a specific customer's order status."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The customer's question or topic to search for.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": (
                "Escalate the conversation to a human support agent by "
                "creating a support ticket. Use this when: you are uncertain "
                "about the correct answer, the available tools did not "
                "return enough information to help the customer, the "
                "customer seems frustrated or upset, or the request requires "
                "manual action you cannot perform (e.g. processing a refund, "
                "changing an order, overriding a policy). Do not guess or "
                "make promises on the company's behalf — escalate instead."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "enum": [
                            "uncertain_answer",
                            "insufficient_info",
                            "customer_frustrated",
                            "requires_manual_action",
                            "other",
                        ],
                        "description": "Why this conversation needs a human.",
                    },
                    "summary": {
                        "type": "string",
                        "description": (
                            "A brief summary of the customer's issue and "
                            "what has been tried so far, for the human agent."
                        ),
                    },
                    "customer_id": {
                        "type": "integer",
                        "description": "The customer's ID, if known.",
                    },
                },
                "required": ["reason", "summary"],
            },
        },
    },
]