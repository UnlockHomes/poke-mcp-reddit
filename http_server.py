"""
HTTP Server wrapper for MCP Reddit Server
This allows the MCP server to be accessed via HTTP/HTTPS for Railway deployment
"""
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp.types import Tool
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server_reddit.server import RedditServer, RedditTools

app = FastAPI(title="Reddit MCP Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Reddit server
reddit_server = RedditServer()

# Tool definitions for MCP protocol
def get_tool_definitions():
    """List available Reddit tools."""
    from mcp_server_reddit.server import RedditTools
    return [
        Tool(
            name=RedditTools.GET_FRONTPAGE_POSTS.value,
            description="Get hot posts from Reddit frontpage",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                }
            }
        ),
        Tool(
            name=RedditTools.GET_SUBREDDIT_INFO.value,
            description="Get information about a subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit_name": {
                        "type": "string",
                        "description": "Name of the subreddit (e.g. 'Python', 'news')",
                    }
                },
                "required": ["subreddit_name"]
            }
        ),
        Tool(
            name=RedditTools.GET_SUBREDDIT_HOT_POSTS.value,
            description="Get hot posts from a specific subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit_name": {
                        "type": "string",
                        "description": "Name of the subreddit (e.g. 'Python', 'news')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["subreddit_name"]
            }
        ),
        Tool(
            name=RedditTools.GET_SUBREDDIT_NEW_POSTS.value,
            description="Get new posts from a specific subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit_name": {
                        "type": "string",
                        "description": "Name of the subreddit (e.g. 'Python', 'news')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["subreddit_name"]
            }
        ),
        Tool(
            name=RedditTools.GET_SUBREDDIT_TOP_POSTS.value,
            description="Get top posts from a specific subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit_name": {
                        "type": "string",
                        "description": "Name of the subreddit (e.g. 'Python', 'news')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "time": {
                        "type": "string",
                        "description": "Time filter for top posts (e.g. 'hour', 'day', 'week', 'month', 'year', 'all')",
                        "default": "",
                        "enum": ["", "hour", "day", "week", "month", "year", "all"]
                    }
                },
                "required": ["subreddit_name"]
            }
        ),
        Tool(
            name=RedditTools.GET_SUBREDDIT_RISING_POSTS.value,
            description="Get rising posts from a specific subreddit",
            inputSchema={
                "type": "object",
                "properties": {
                    "subreddit_name": {
                        "type": "string",
                        "description": "Name of the subreddit (e.g. 'Python', 'news')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["subreddit_name"]
            }
        ),
        Tool(
            name=RedditTools.GET_POST_CONTENT.value,
            description="Get detailed content of a specific post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "string",
                        "description": "ID of the post",
                    },
                    "comment_limit": {
                        "type": "integer",
                        "description": "Number of top-level comments to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "comment_depth": {
                        "type": "integer",
                        "description": "Maximum depth of comment tree (default: 3)",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name=RedditTools.GET_POST_COMMENTS.value,
            description="Get comments from a post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "string",
                        "description": "ID of the post",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of comments to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["post_id"]
            }
        ),
    ]
    return tools

async def call_tool(name: str, arguments: dict):
    """Handle tool calls for Reddit API."""
    try:
        match name:
            case RedditTools.GET_FRONTPAGE_POSTS.value:
                limit = arguments.get("limit", 10)
                result = reddit_server.get_frontpage_posts(limit)

            case RedditTools.GET_SUBREDDIT_INFO.value:
                subreddit_name = arguments.get("subreddit_name")
                if not subreddit_name:
                    raise ValueError("Missing required argument: subreddit_name")
                result = reddit_server.get_subreddit_info(subreddit_name)

            case RedditTools.GET_SUBREDDIT_HOT_POSTS.value:
                subreddit_name = arguments.get("subreddit_name")
                if not subreddit_name:
                    raise ValueError("Missing required argument: subreddit_name")
                limit = arguments.get("limit", 10)
                result = reddit_server.get_subreddit_hot_posts(subreddit_name, limit)

            case RedditTools.GET_SUBREDDIT_NEW_POSTS.value:
                subreddit_name = arguments.get("subreddit_name")
                if not subreddit_name:
                    raise ValueError("Missing required argument: subreddit_name")
                limit = arguments.get("limit", 10)
                result = reddit_server.get_subreddit_new_posts(subreddit_name, limit)

            case RedditTools.GET_SUBREDDIT_TOP_POSTS.value:
                subreddit_name = arguments.get("subreddit_name")
                if not subreddit_name:
                    raise ValueError("Missing required argument: subreddit_name")
                limit = arguments.get("limit", 10)
                time = arguments.get("time", "")
                result = reddit_server.get_subreddit_top_posts(subreddit_name, limit, time)

            case RedditTools.GET_SUBREDDIT_RISING_POSTS.value:
                subreddit_name = arguments.get("subreddit_name")
                if not subreddit_name:
                    raise ValueError("Missing required argument: subreddit_name")
                limit = arguments.get("limit", 10)
                result = reddit_server.get_subreddit_rising_posts(subreddit_name, limit)

            case RedditTools.GET_POST_CONTENT.value:
                post_id = arguments.get("post_id")
                if not post_id:
                    raise ValueError("Missing required argument: post_id")
                comment_limit = arguments.get("comment_limit", 10)
                comment_depth = arguments.get("comment_depth", 3)
                result = reddit_server.get_post_content(post_id, comment_limit, comment_depth)

            case RedditTools.GET_POST_COMMENTS.value:
                post_id = arguments.get("post_id")
                if not post_id:
                    raise ValueError("Missing required argument: post_id")
                limit = arguments.get("limit", 10)
                result = reddit_server.get_post_comments(post_id, limit)

            case _:
                raise ValueError(f"Unknown tool: {name}")

        # Convert result to JSON-serializable format
        if hasattr(result, 'model_dump'):
            return result.model_dump()
        elif isinstance(result, list):
            return [item.model_dump() if hasattr(item, 'model_dump') else item for item in result]
        else:
            return result

    except Exception as e:
        raise ValueError(f"Error processing mcp-server-reddit query: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "Reddit MCP Server"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP protocol endpoint - JSON-RPC 2.0"""
    try:
        body = await request.json()
        
        # Handle MCP protocol messages
        if body.get("jsonrpc") == "2.0":
            method = body.get("method")
            params = body.get("params", {})
            
            if method == "tools/list":
                tools = get_tool_definitions()
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "tools": [tool.model_dump() for tool in tools]
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = await call_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, default=str, indent=2)
                            }
                        ]
                    }
                }
            elif method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "serverInfo": {
                            "name": "mcp-reddit",
                            "version": "0.2.0"
                        }
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
        else:
            return {"error": "Invalid JSON-RPC request"}
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in locals() else None,
            "error": {"code": -32603, "message": str(e)}
        }

@app.get("/tools")
async def list_tools_endpoint():
    """List all available tools"""
    tools = get_tool_definitions()
    return {
        "tools": [tool.model_dump() for tool in tools]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

