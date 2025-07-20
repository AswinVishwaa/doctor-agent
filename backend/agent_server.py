from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from functools import partial
import requests
import os
import json
import ast

app = FastAPI(title="LLM Agent Server")
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSION_STORE = {}

# Get tool metadata from MCP
MCP_SERVER = os.getenv("MCP_SERVER", "http://localhost:8000")
TOOLS_ENDPOINT = f"{MCP_SERVER}/mcp/tools"


def fetch_tool(tool_name, tool_input, method):
    url = f"{MCP_SERVER}/mcp/tool/{tool_name}"
    print(f"URL: {url}")
    print(f"Params: {tool_input}")
    print(f"Method: {method}")
    try:
        if method.upper() == "GET":
            res = requests.get(url, params=tool_input)
        elif method.upper() == "POST":
            res = requests.post(url, json=tool_input)
        else:
            return {"error": f"Unsupported HTTP method {method}"}

        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def fetch_tools():
    res = requests.get(TOOLS_ENDPOINT)
    res.raise_for_status()
    tools_meta = res.json()

    tools = []
    for meta in tools_meta:
        name = meta["name"]
        method = meta["method"]
        endpoint = meta["endpoint"]
        description = meta["description"]

        def tool_func(input_data, name=name, method=method, endpoint=endpoint):
            try:
                if isinstance(input_data, dict):
                    print(f"its dictionary {input_data}")
                    parsed = input_data
                elif isinstance(input_data, str):
                    print(f"its string {input_data}")
                    try:
                        parsed = ast.literal_eval(input_data)
                        print(f"its parsed data {parsed}")
                    except (json.JSONDecodeError, ValueError, SyntaxError):
                        parsed = {}
                        for pair in input_data.split(","):
                            if "=" in pair:
                                k, v = pair.split("=", 1)
                                parsed[k.strip()] = v.strip().strip("\"'")
                        print(f"its exception parsed data {parsed}")
                else:
                    return {"error": "Invalid input format."}

                print(f"📞 Calling {endpoint} with params:", parsed)
                return fetch_tool(name, parsed, method)
            except Exception as e:
                return {"error": str(e)}

        # ✅ Updated handling for different param structures
        raw_params = meta.get("params", [])
        required_params = []

        if isinstance(raw_params, list):
            for p in raw_params:
                if isinstance(p, dict) and p.get("required", True):
                    required_params.append(p.get("name", "unknown"))
                elif isinstance(p, str):
                    required_params.append(p)  # fallback if params is just list of strings
        elif isinstance(raw_params, dict):
            required_params = list(raw_params.keys())

        param_str = ", ".join(required_params)

        tools.append(Tool(
            name=name,
            func=tool_func,
            description=f"{description} Required parameters: {param_str}"
        ))

    return tools

@app.post("/agent")
async def agent_chat(request: Request):
    data = await request.json()
    query = data.get("query")
    session_id = data.get("session_id", "default")
    email = data.get("email")
    role = data.get("role")

    identity_info = f"""You are talking to a {role} with email {email}.
                        If no appointments or slots are found after checking 3 dates, stop and return a summary. 
                        When scheduling an appointment, never guess the date.
                        Always use the slot datetime exactly as returned by the availability tool (e.g., '2025-07-21T08:00:00').
                        NEVER schedule appointments unless the user clearly says 'book', 'schedule', or 'make an appointment'. 
                        Even if availability is known, do not assume intent. Return only information.
                        Do NOT ask follow-up questions or wait for input. Return information only and stop.
                                                                                                                            """

    if query:
        query = f"{identity_info}{query}"
    else:
        return {"error": "Empty query received."}

    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output",
        chat_memory=SESSION_STORE[session_id],
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192"
    )

    tools = fetch_tools()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
         max_iterations=5,             # prevent infinite loop
        max_execution_time=30 
    )

    print("🧠 Calling LLM Agent with query:", query)
    print("🔧 Available tools:", [t.name for t in tools])
    result = agent.invoke({"input": query})
    return {"response": result}
