"""MCP server for Response-2000 integration."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import analyze_section, ANALYZE_SECTION_SCHEMA

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("response-mcp")

# Create MCP server instance
app = Server("response-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name=ANALYZE_SECTION_SCHEMA["name"],
            description=ANALYZE_SECTION_SCHEMA["description"],
            inputSchema=ANALYZE_SECTION_SCHEMA["inputSchema"],
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool execution requests."""
    
    if name == "analyze_section":
        try:
            # Extract and validate arguments
            width = float(arguments["width"])
            depth = float(arguments["depth"])
            fc = float(arguments["fc"])
            fy = float(arguments["fy"])
            rebar_top = [tuple(layer) for layer in arguments["rebar_top"]]
            rebar_bottom = [tuple(layer) for layer in arguments["rebar_bottom"]]
            axial_load = float(arguments.get("axial_load", 0.0))
            
            # Execute analysis (currently returns stub data)
            result = await analyze_section(
                width=width,
                depth=depth,
                fc=fc,
                fy=fy,
                rebar_top=rebar_top,
                rebar_bottom=rebar_bottom,
                axial_load=axial_load,
            )
            
            # Format response
            response = f"""Section Analysis Results:

Design Moment Capacity (φMn): {result.phi_mn:.2f} kNm
Failure Mode: {result.failure_mode}
Curvature at Capacity: {result.curvature:.6f} 1/mm
Neutral Axis Depth: {result.neutral_axis_depth:.1f} mm
Applied Axial Load: {result.axial_load:.1f} kN

Note: Currently returning stub data. Real Response-2000 integration pending.

Section Parameters:
- Width: {width} mm
- Depth: {depth} mm  
- Concrete Strength (f'c): {fc} MPa
- Rebar Yield (fy): {fy} MPa
- Top Reinforcement: {rebar_top}
- Bottom Reinforcement: {rebar_bottom}
"""
            
            return [TextContent(type="text", text=response)]
            
        except KeyError as e:
            error_msg = f"Missing required parameter: {e}"
            logger.error(error_msg)
            return [TextContent(type="text", text=f"Error: {error_msg}")]
            
        except ValueError as e:
            error_msg = f"Invalid parameter value: {e}"
            logger.error(error_msg)
            return [TextContent(type="text", text=f"Error: {error_msg}")]
            
        except Exception as e:
            error_msg = f"Analysis failed: {e}"
            logger.exception(error_msg)
            return [TextContent(type="text", text=f"Error: {error_msg}")]
    
    else:
        error_msg = f"Unknown tool: {name}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


async def run_server():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Response-MCP server starting...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main():
    """Entry point for the server."""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.exception(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
