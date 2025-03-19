from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import os
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file
load_dotenv()

model = ChatOpenAI(model="gpt-4o")

# Use the local formatter server
server_params = StdioServerParameters(
    command="python",
    args=["-m", "mb_mcp.formatter_server"],
    env=None
)   

async def run_app(user_question):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": f"{user_question}"})
            return agent_response

if __name__ == "__main__":
    user_question = 'Format this text into a concise message: The quarterly financial report indicates that revenue has increased by 15% compared to the previous quarter. This growth is primarily attributed to the expansion of our product line and entry into new markets. However, operating expenses have also risen by 8%, mainly due to increased marketing efforts and hiring of additional staff. Despite this, the overall profit margin has improved by 3 percentage points.'
    res = asyncio.run(run_app(user_question=user_question))
    
    # Simply print the response
    print(res)
