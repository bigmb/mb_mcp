from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file
load_dotenv()

# model = ChatOpenAI(model="gpt-4o")
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Ensure environment variables are set
if not os.environ.get('SLACK_BOT_TOKEN') or not os.environ.get('SLACK_TEAM_ID'):
    print("Error: SLACK_BOT_TOKEN and SLACK_TEAM_ID environment variables must be set")
    print("Current values:")
    print(f"SLACK_BOT_TOKEN: {os.environ.get('SLACK_BOT_TOKEN')}")
    print(f"SLACK_TEAM_ID: {os.environ.get('SLACK_TEAM_ID')}")

server_params = StdioServerParameters(
    command="sudo",
    args=["docker", "run", "-i", "--rm", 
          "-e", f"SLACK_BOT_TOKEN={os.environ.get('SLACK_BOT_TOKEN')}", 
          "-e", f"SLACK_TEAM_ID={os.environ.get('SLACK_TEAM_ID')}", 
          "mcp/slack"],
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
    user_question = 'Provide the recent updates in the channel in proper format without username: C0EV9TV53'
    res = asyncio.run(run_app(user_question=user_question))
    
    # Simply print the response
    print(res['messages'][-1].content)
