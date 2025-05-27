#!/usr/bin/env python3

import asyncio
import json
import sys
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("test-weather")

@mcp.tool()
def hello() -> str:
    """A simple hello world tool."""
    return "Hello from MCP weather server!"

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    """
    return a + b

if __name__ == "__main__":
    mcp.run() 