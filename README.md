# MB_MCP (Model Context Protocol)

A Python package for integrating various services with Claude and other LLMs using the Model Context Protocol (MCP).

## Overview

MB_MCP provides connectors for various services like Slack, Google Drive, GitHub, Atlassian, PostgreSQL, and more. It allows you to build applications that leverage these services through a unified interface, making it easy to create powerful AI-powered applications.

## Features

- **Multiple Service Connectors**:
  - Slack
  - Google Drive
  - GitHub
  - Atlassian (Confluence & Jira)
  - PostgreSQL
  - Brave Search
  - Formatter

- **Web Dashboard**: A simple web interface for querying the services
- **Environment-based Configuration**: All API keys and credentials are stored in a `.env` file for security

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker (for running some of the services)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/bigmb/mb_mcp.git
   cd mb_mcp
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your API keys and credentials.

## Configuration

The following environment variables need to be set in the `.env` file:

### API Keys
```
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Slack Configuration
```
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_APP_TOKEN=your_slack_app_token
SLACK_TEAM_ID=your_slack_team_id
```

### PostgreSQL Configuration
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
PG_CONNECTION_STRING=postgresql://host.docker.internal:5432/mydb
```

### Google Drive Configuration
```
GDRIVE_CREDENTIALS_PATH=/path/to/your/gdrive/credentials.json
```

### GitHub Configuration
```
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
```

### Atlassian Configuration
```
# For Confluence Cloud
CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_USERNAME=your.email@domain.com
CONFLUENCE_API_TOKEN=your_api_token

# For Jira Cloud
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your.email@domain.com
JIRA_API_TOKEN=your_api_token
```

### Brave Search Configuration
```
BRAVE_API_KEY=your_brave_api_key
```

## Usage

### Running the Web Dashboard

```bash
python -m mb_mcp.app
```

This will start a Flask server on http://localhost:5000 where you can interact with the services.

### Using the Connectors Programmatically

```python
import asyncio
from mb_mcp.slack_connecter import run_app as run_slack_app

async def main():
    question = "Provide the recent updates in the channel in proper format: <channel_id>"
    result = await run_slack_app(question)
    print(result['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

### Project Structure

- `mb_mcp/`: Main package directory
  - `app.py`: Flask web application
  - `*_connecter.py`: Connector modules for different services
  - `formatter_server.py`: Local MCP server for text formatting
- `query_dashboard/`: Web dashboard frontend
- `servers/`: MCP server implementations. From here, the docker image is built. mcp_servers (Anthropic MCP's servers)

## License

MIT
