from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp_tools.availability import router as availability_router
from mcp_tools.schedule import router as schedule_router
from mcp_registry import get_tool_registry
from mcp_tools.availability import router as availability_router
from mcp_tools.schedule import router as schedule_router
from mcp_tools.summary import router as summary_router
from mcp_tools.latest import router as latest_router
from mcp_tools.doctor_summary import router as doctor_summary_router


app = FastAPI(title="MCP Doctor Agent")

# Allow all origins for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP Endpoints
@app.get("/mcp/tools")
def list_tools():
    return get_tool_registry()

app.include_router(availability_router, prefix="/mcp/tool/check_availability", tags=["Tools"])
app.include_router(schedule_router, prefix="/mcp/tool/schedule_appointment", tags=["Tools"])
app.include_router(summary_router, prefix="/mcp/tool/generate_summary", tags=["Tools"])
app.include_router(latest_router, prefix="/mcp/tool/get_latest_appointment", tags=["Tools"])
app.include_router(doctor_summary_router, prefix="/mcp/tool/doctor_summary", tags=["Tools"])




# Basic test
@app.get("/")
def root():
    return {"msg": "MCP Doctor Agent API is live"}
