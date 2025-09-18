import os
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

TARGET_FOLDER_PATH = ".."
filesystem_toolset = MCPToolset(
    connection_params = StdioConnectionParams(
        server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",  # Argument for npx to auto-confirm install
                "@modelcontextprotocol/server-filesystem",
                os.path.abspath(TARGET_FOLDER_PATH),
            ],
        ),
    ),
)

from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-2.0-flash",
    name="filesystem_agent",
    tools=[filesystem_toolset],
    instruction="파일 시스템에서 파일을 읽고 쓰는 작업을 수행하십시오.",
)
