# Response-MCP

MCP (Model Context Protocol) server for Response-2000 sectional analysis of reinforced concrete.

## Project Status

**Current Phase**: Initial MCP skeleton with stub implementation

- ✅ MCP server infrastructure complete
- ✅ Tool schema defined (`analyze_section`)
- ⏳ Response-2000 integration (pending file format investigation)
- ⏳ Real analysis execution (pending)

The server currently returns **stub data** - real Response-2000 integration will be added after manual investigation of file formats.

## Installation

### Prerequisites

- Python 3.10 or higher
- Response-2000 installed (Windows executable)
- WSL or native Windows environment

### Setup

```bash
# Clone repository
git clone https://github.com/maczout/response-mcp.git
cd response-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Running the Server

The MCP server communicates via stdio. For development/testing:

```bash
# Run directly
python -m response_mcp.server

# Or use the installed script
response-mcp
```

### Testing with Claude Desktop

Add to your Claude Desktop MCP configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "response-mcp": {
      "command": "python",
      "args": ["-m", "response_mcp.server"],
      "cwd": "/path/to/response-mcp"
    }
  }
}
```

Restart Claude Desktop to load the server.

### Example Usage in Claude

```
Analyze a rectangular concrete section:
- Width: 400 mm
- Depth: 600 mm  
- Concrete strength: 35 MPa
- Rebar yield: 400 MPa
- Top reinforcement: 4 × 25mm bars, 60mm cover
- Bottom reinforcement: 4 × 25mm bars, 60mm cover
```

Claude will use the `analyze_section` tool with these parameters.

## Tool Reference

### `analyze_section`

Analyzes a rectangular reinforced concrete section.

**Parameters:**
- `width` (number): Section width in mm
- `depth` (number): Section depth in mm
- `fc` (number): Concrete compressive strength in MPa
- `fy` (number): Reinforcement yield strength in MPa
- `rebar_top` (array): Top reinforcement as `[[count, diameter_mm, cover_mm], ...]`
- `rebar_bottom` (array): Bottom reinforcement as `[[count, diameter_mm, cover_mm], ...]`
- `axial_load` (number, optional): Applied axial load in kN (positive = compression)

**Returns:**
- Design moment capacity (φMn) in kNm
- Failure mode (compression/tension/balanced)
- Curvature at capacity (1/mm)
- Neutral axis depth (mm)

## Development Roadmap

### Phase 1: Investigation (Current)
- [ ] Run Response-2000 manually on sample sections
- [ ] Document .r2k input file format
- [ ] Capture and analyze .out output files
- [ ] Test command-line execution with /b /r flags

### Phase 2: Adapter Implementation
- [ ] Implement `InputFileGenerator` for .r2k files
- [ ] Implement `Response2000Runner` for subprocess execution
- [ ] Implement `OutputFileParser` for .out files
- [ ] Add comprehensive error handling
- [ ] Write unit tests against known results

### Phase 3: Integration
- [ ] Replace stub implementation in `tools.py`
- [ ] Add configuration for Response.exe path
- [ ] Test end-to-end with Claude
- [ ] Handle edge cases and convergence failures

### Phase 4: Polish
- [ ] Add more section types (T-beams, etc.)
- [ ] Improve error messages
- [ ] Add logging and diagnostics
- [ ] Write comprehensive documentation
- [ ] Create example calculations

## Project Structure

```
response-mcp/
├── src/
│   └── response_mcp/
│       ├── __init__.py       # Package initialization
│       ├── server.py          # MCP server entry point
│       ├── tools.py           # Tool definitions (stub implementation)
│       └── adapter.py         # Response-2000 integration (stub)
├── tests/                     # Test suite (coming soon)
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Testing

```bash
# Run tests (once implemented)
pytest

# Run with coverage
pytest --cov=response_mcp
```

## Contributing

This project demonstrates the "fractional engineering" methodology - AI-augmented structural engineering workflows.

Development progress and methodology will be documented through blog posts and this repository.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Response-2000 by Evan Bentz and Michael Collins
- MCP (Model Context Protocol) by Anthropic
