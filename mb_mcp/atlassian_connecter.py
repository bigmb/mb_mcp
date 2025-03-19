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
if not os.environ.get('CONFLUENCE_URL') or not os.environ.get('CONFLUENCE_USERNAME') or not os.environ.get('CONFLUENCE_API_TOKEN'):
    print("Error: Confluence environment variables must be set")
    print("Current values:")
    print(f"CONFLUENCE_URL: {os.environ.get('CONFLUENCE_URL')}")
    print(f"CONFLUENCE_USERNAME: {os.environ.get('CONFLUENCE_USERNAME')}")
    print(f"CONFLUENCE_API_TOKEN: {os.environ.get('CONFLUENCE_API_TOKEN')}")

if not os.environ.get('JIRA_URL') or not os.environ.get('JIRA_USERNAME') or not os.environ.get('JIRA_API_TOKEN'):
    print("Error: Jira environment variables must be set")
    print("Current values:")
    print(f"JIRA_URL: {os.environ.get('JIRA_URL')}")
    print(f"JIRA_USERNAME: {os.environ.get('JIRA_USERNAME')}")
    print(f"JIRA_API_TOKEN: {os.environ.get('JIRA_API_TOKEN')}")

server_params = StdioServerParameters(
    command="sudo",
    args=["docker", "run", "-i", "--rm", 
          "-e", f"CONFLUENCE_URL={os.environ.get('CONFLUENCE_URL')}", 
          "-e", f"CONFLUENCE_USERNAME={os.environ.get('CONFLUENCE_USERNAME')}", 
          "-e", f"CONFLUENCE_API_TOKEN={os.environ.get('CONFLUENCE_API_TOKEN')}", 
          "-e", f"JIRA_URL={os.environ.get('JIRA_URL')}", 
          "-e", f"JIRA_USERNAME={os.environ.get('JIRA_USERNAME')}", 
          "-e", f"JIRA_API_TOKEN={os.environ.get('JIRA_API_TOKEN')}", 
          "mcp/atlassian"],
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
    user_question = 'Search for Confluence pages about project documentation'
    res = asyncio.run(run_app(user_question=user_question))
    
    # Simply print the response
    print(res)
