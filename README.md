# MCP Jenkins Server

A Model Context Protocol (MCP) server that provides Jenkins integration tools.

## Features

- Get Jenkins server information
- List and inspect Jenkins jobs
- Get recent builds and their summaries
- Get build information and console output
- Manage Jenkins views
- Trigger job builds with parameters

## Requirements

- Python 3.10+
- Jenkins server with API access
- Jenkins API token for authentication

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file with your Jenkins credentials:

```ini
JENKINS_URL=https://your-jenkins-server
JENKINS_USER=your-username
JENKINS_TOKEN=your-api-token
```

## CLI Configuration

To add this MCP server to your CLI, use the following configuration:
Change 'Support/Claude/claude_desktop_config.json' file content to : 

```json
{
  "mcpServers": {
    "mcp-jenkins-server": {
      "command": "/Users/username/.local/bin/uv -> //uv full path", 
      "args": [
        "--directory", 
        "/Users/username/Desktop/mcp-jenkins-server -> //project path ", 
        "run",
        "server.py"
      ],
      "env": {
        "JENKINS_URL": "http://localhost:8080",
        "JENKINS_USERNAME": "xx",
        "JENKINS_PASSWORD": "xx"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Available Tools

This MCP server provides the following tools:

### `get_jenkins_info`
Get Jenkins server information

### `list_jobs`
List all Jenkins jobs

### `get_job_info`
Get information about a specific job  
- Parameters:
  - `job_name`: Name of the job to inspect

### `get_last_builds`
Get a summary of the most recent builds for a job  
- Parameters:
  - `job_name`: Name of the job  
  - `count` (optional): Number of recent builds to retrieve (default: 3)

### `get_build_info`
Get detailed information about a specific build  
- Parameters:
  - `job_name`: Name of the job  
  - `build_number`: Build number to inspect

### `get_build_console_output`
Get console output for a specific build  
- Parameters:
  - `job_name`: Name of the job  
  - `build_number`: Build number to inspect

### `get_views`
List all Jenkins views

### `trigger_job_build`
Trigger a Jenkins job build with optional parameters  
- Parameters:
  - `job_name`: Name of the job  
  - `parameters` (optional): Dictionary of parameters to pass to the job



### demo video : 
[Demo](link)
