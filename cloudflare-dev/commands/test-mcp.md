---
name: test-mcp
description: Test an MCP server locally using the MCP Inspector
---

# Test MCP Server

Test the MCP server implementation using the MCP Inspector.

## Steps

1. **Start the dev server**:
   ```bash
   npm run dev
   ```

2. **Launch MCP Inspector** (in a new terminal):
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. **Connect to the MCP endpoint**:
   - Default URL: `http://localhost:8787/mcp`
   - If using custom port/path from `$ARGUMENTS`, connect to that instead

4. **Verify tool discovery**:
   - List all available tools
   - Confirm each tool has a description and parameter schema
   - Check that tool names match expectations

5. **Test each tool**:
   - Invoke with valid parameters and verify responses
   - Invoke with edge cases (empty strings, missing optional params)
   - Verify error responses include `isError: true`

6. **Test authentication** (if OAuth configured):
   - Verify unauthenticated requests are rejected
   - Test the OAuth flow end-to-end
   - Verify `getMcpAuthContext()` returns user identity

7. **Report results**:
   - List all tools tested with pass/fail status
   - Note any unexpected behaviors or errors
   - Suggest fixes for any failures

## Usage

```
/test-mcp $ARGUMENTS
```

`$ARGUMENTS` optionally specifies the endpoint. Examples:
- `/test-mcp` - Test at default `http://localhost:8787/mcp`
- `/test-mcp http://localhost:8788/mcp` - Custom port
- `/test-mcp /sse` - Test SSE endpoint (legacy)
