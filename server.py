#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/03/31 11:07:38
# @Author  : WinJayX
# @Email   : WinJayX@Gmail.com
# @File    : server.py

from contextlib import asynccontextmanager
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import jenkins
import asyncio

from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("Mcp Jenkins Server", log_level="ERROR")


@dataclass
class JenkinsContext:
    client: jenkins.Jenkins


@asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    load_dotenv()
    jenkins_url = os.getenv('JENKINS_URL')
    jenkins_user = os.getenv('JENKINS_USER')
    jenkins_token = os.getenv('JENKINS_TOKEN')

    client = await asyncio.to_thread(
        jenkins.Jenkins,
        jenkins_url,
        username=jenkins_user,
        password=jenkins_token
    )
    try:
        yield JenkinsContext(client=client)
    finally:
        pass

mcp = FastMCP("Mcp Jenkins Server", lifespan=app_lifespan, log_level="ERROR")


@mcp.tool()
def get_jenkins_info(ctx: Context):
    """Get Jenkins info"""
    client = ctx.request_context.lifespan_context.client
    return client.get_info()


@mcp.tool()
def list_jobs(ctx: Context):
    """List all Jenkins jobs"""
    client = ctx.request_context.lifespan_context.client
    return client.get_jobs()


@mcp.tool()
def get_job_info(ctx: Context, job_name: str):
    """Get Jenkins job info"""
    client = ctx.request_context.lifespan_context.client
    return client.get_job_info(job_name)

@mcp.tool()
def get_last_builds(ctx: Context, job_name: str, count: int = 3):
    """
    Retrieve the last 'count' builds for a Jenkins job.

    Args:
        ctx (Context): The FastMCP context.
        job_name (str): The name of the Jenkins job.
        count (int, optional): Number of recent builds to retrieve. Defaults to 3.

    Returns:
        list: A list of dictionaries containing build information.
    """
    client = ctx.request_context.lifespan_context.client
    job_info = client.get_job_info(job_name, fetch_all_builds=True)
    builds = job_info.get('builds', [])[:count]
    build_summaries = []

    for build in builds:
        build_number = build.get('number')
        build_info = client.get_build_info(job_name, build_number)
        summary = {
            'build_number': build_number,
            'result': build_info.get('result'),
            'timestamp': build_info.get('timestamp'),
            'duration': build_info.get('duration'),
            'url': build_info.get('url')
        }
        build_summaries.append(summary)

    return build_summaries


@mcp.tool()
def get_build_info(ctx: Context, job_name: str, build_number: int):
    """Get Jenkins build info"""
    client = ctx.request_context.lifespan_context.client
    return client.get_build_info(job_name, build_number)


@mcp.tool()
def get_build_console_output(ctx: Context, job_name: str, build_number: int):
    """Get Jenkins build console output"""
    client = ctx.request_context.lifespan_context.client
    return client.get_build_console_output(job_name, build_number)


@mcp.tool()
def get_views(ctx: Context):
    """Get Jenkins views"""
    client = ctx.request_context.lifespan_context.client
    return client.get_views()


@mcp.tool()
def trigger_job_build(ctx: Context, job_name: str, parameters: dict = None):
    """
    Trigger a Jenkins job build with optional parameters without checking the result of the build.

    Args:
        ctx (Context): The FastMCP context.
        job_name (str): The name of the Jenkins job to trigger.
        parameters (dict, optional): A dictionary of parameters to pass to the job.

    Returns:
        dict: Confirmation message with queue item number.
    """
    client = ctx.request_context.lifespan_context.client
    queue_item_number = client.build_job(job_name, parameters=parameters)
    return {
        "message": f"Build for job '{job_name}' has been triggered.",
        "queue_item_number": queue_item_number
    }

@mcp.tool()
def TestMcp(ctx: Context, parameters: dict = None):
    """
    test jenkins mcp
    """
    
    return "hello world"


if __name__ == "__main__":
    mcp.run()
