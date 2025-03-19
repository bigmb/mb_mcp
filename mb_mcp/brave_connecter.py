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

# Ensure environment variables are set
if not os.environ.get('BRAVE_API_KEY') or os.environ.get('BRAVE_API_KEY') == 'YOUR_BRAVE_API_KEY_HERE':
    print("Error: BRAVE_API_KEY environment variable must be set")
    print("Current value:")
    print(f"BRAVE_API_KEY: {os.environ.get('BRAVE_API_KEY')}")

server_params = StdioServerParameters(
    command="sudo",
    args=["docker", "run", "-i", "--rm", 
          "-e", f"BRAVE_API_KEY={os.environ.get('BRAVE_API_KEY')}", 
          "mcp/brave-search"],
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
    user_question = 'Search for the latest news about artificial intelligence'
    res = asyncio.run(run_app(user_question=user_question))
    
    # Simply print the response
    print(res)
