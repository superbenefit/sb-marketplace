---
description: MCP (Model Context Protocol) server and client integration with Cloudflare Workers, including createMcpHandler, OAuth authentication, and transport options
globs: ["src/**/*.ts", "src/server/**"]
alwaysApply: false
---

# MCP Integration with Cloudflare

## Overview

MCP (Model Context Protocol) is an open standard connecting AI systems with external applications - a standardized way to connect AI agents to services.

### Terminology
- **MCP Hosts**: AI assistants (Claude, Cursor) that use external capabilities
- **MCP Clients**: Embedded in hosts, connect to MCP servers
- **MCP Servers**: Expose tools, prompts, and resources

## Recommended: createMcpHandler (Stateless)

The recommended pattern for building MCP servers on Cloudflare. Runs as a standard Worker without Durable Objects overhead.

```typescript
import { createMcpHandler } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0"
});

// Register tools
server.tool(
  "search_docs",
  "Search the documentation",
  {
    query: z.string().describe("Search query"),
    limit: z.number().optional().describe("Max results")
  },
  async ({ query, limit = 10 }) => {
    const results = await performSearch(query, limit);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }]
    };
  }
);

// Export handler - createMcpHandler returns a fetch handler function
// Routes to /mcp by default
export default {
  fetch: (request: Request, env: Env, ctx: ExecutionContext) => {
    return createMcpHandler(server)(request, env, ctx);
  }
};
```

### Configuration for Stateless MCP

```jsonc
// wrangler.jsonc - NO durable_objects or migrations needed
{
  "name": "my-mcp-server",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "observability": { "enabled": true }
}
```

## Stateful MCP (Agent + createMcpHandler)

When you need per-user state, WebSocket connections, or scheduling alongside MCP, use `createMcpHandler` with a `WorkerTransport` inside an Agent class. This persists session state in Durable Object storage.

```typescript
import { Agent } from "agents";
import { createMcpHandler, WorkerTransport, type TransportState } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const STATE_KEY = "mcp-transport-state";

interface Env {
  VECTORIZE: VectorizeIndex;
  AI: Ai;
}

export class StatefulMcpAgent extends Agent<Env> {
  server = new McpServer({
    name: "stateful-mcp",
    version: "1.0.0"
  });

  // WorkerTransport with persistent storage for session state
  transport = new WorkerTransport({
    sessionIdGenerator: () => this.name,
    storage: {
      get: () => this.ctx.storage.kv.get<TransportState>(STATE_KEY),
      set: (state: TransportState) => { this.ctx.storage.kv.put(STATE_KEY, state); },
    },
  });

  async onStart() {
    // Register tools that access agent state and bindings
    this.server.tool(
      "search_knowledge",
      "Search the knowledge base",
      { query: z.string() },
      async ({ query }) => {
        const embedding = await this.env.AI.run("@cf/baai/bge-small-en-v1.5", { text: query });
        const results = await this.env.VECTORIZE.query(embedding.data[0], {
          topK: 10,
          returnMetadata: "all"
        });

        return {
          content: [{ type: "text", text: JSON.stringify(results.matches, null, 2) }]
        };
      }
    );
  }

  async onRequest(request: Request): Promise<Response> {
    // Route MCP requests through the handler with persistent transport
    return createMcpHandler(this.server, {
      transport: this.transport,
    })(request, this.env, {});
  }
}
```

## Legacy: McpAgent (SSE Compatibility Only)

Use `McpAgent` only when you need backward-compatible SSE transport. For new servers, prefer `createMcpHandler`.

```typescript
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

interface Props {
  userId: string;
  accessLevel: string;
}

export class LegacyMCP extends McpAgent<Env, State, Props> {
  // Server as CLASS PROPERTY
  server = new McpServer({
    name: "legacy-server",
    version: "1.0.0"
  });

  // Register tools in init()
  async init() {
    this.server.tool(
      "search",
      "Search content",
      { query: z.string() },
      async ({ query }) => {
        return { content: [{ type: "text", text: "result" }] };
      }
    );
  }
}
```

### McpAgent Critical Requirements
1. **Server as class property**: `server = new McpServer({...})`
2. **Tools in init()**: Register all tools in the `init()` method
3. **migrations block**: Include `new_sqlite_classes` for state
4. **Props for auth**: Access user identity via `this.props`

## OAuth Authentication (workers-oauth-provider)

```typescript
import { OAuthProvider } from "workers-oauth-provider";
import { MyMcpServer } from "./server";

// Auth handler for your authentication flow
const AuthHandler = {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);

    if (url.pathname === "/authorize") {
      // Redirect to your auth provider (GitHub, Google, etc.)
      return new Response("Authorize endpoint");
    }

    if (url.pathname === "/callback") {
      // Handle auth callback, exchange code for token
      return new Response("Callback endpoint");
    }

    return new Response("Not found", { status: 404 });
  }
};

export default new OAuthProvider({
  apiRoute: "/mcp",
  apiHandler: MyMcpServer,       // Your MCP agent or handler
  defaultHandler: AuthHandler,    // Handles auth routes
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/token",
  clientRegistrationEndpoint: "/register"
});
```

### OAuth KV Binding (Required)

```jsonc
// wrangler.jsonc
{
  "kv_namespaces": [{
    "binding": "OAUTH_KV",
    "id": "your-kv-namespace-id"
  }]
}
```

### Accessing Auth Context in Tools

```typescript
import { getMcpAuthContext } from "agents/mcp";

server.tool(
  "protected_action",
  "Action requiring authentication",
  { data: z.string() },
  async ({ data }) => {
    const authContext = getMcpAuthContext();
    // authContext contains user identity from OAuth flow
    if (!authContext) {
      return { content: [{ type: "text", text: "Unauthorized" }], isError: true };
    }
    // Proceed with authenticated action
    return { content: [{ type: "text", text: `Processed for ${authContext.userId}` }] };
  }
);
```

### OAuth Patterns (3 Options)

1. **Self-handled OAuth**: Full control using `workers-oauth-provider`
2. **Third-party OAuth** (GitHub, Google): Redirect to external IdP, exchange tokens
3. **Bring-your-own auth** (Stytch, Auth0, WorkOS): Integrate existing auth provider

## MCP Client (Connecting TO Other Servers)

Agents can connect to remote MCP servers:

```typescript
import { Agent } from "agents";

export class MyAgent extends Agent<Env> {
  async onStart() {
    const { id, authUrl } = await this.addMcpServer(
      "slack-mcp",                    // Server name
      "https://mcp.slack.com/sse",    // Server URL
      "https://my-agent.workers.dev/callback",  // OAuth callback
      "/agents"                        // Agents prefix
    );

    if (authUrl) {
      this.setState({ pendingAuth: { serverId: id, authUrl } });
    }
  }

  async onMessage(connection: Connection, message: WSMessage) {
    const servers = this.getMcpServers();
    // Use tools from connected servers
  }
}
```

## Transport: Streamable HTTP

MCP servers on Cloudflare use Streamable HTTP transport:
- Default route: `/mcp` (configurable)
- Supports SSE streaming for responses
- WebSocket Hibernation for efficiency (with McpAgent)
- Request/response multiplexing

## Tool Response Format

```typescript
// Success response
return {
  content: [
    { type: "text", text: "Result here" },
    { type: "image", data: base64Data, mimeType: "image/png" }
  ]
};

// Error response
return {
  content: [{ type: "text", text: "Error message" }],
  isError: true
};
```

## Best Practices

### Tool Design
- Don't wrap entire API schemas - build tools for specific user goals
- Fewer well-designed tools > many granular ones
- Detailed parameter descriptions help agents use tools correctly

### Scoped Permissions
- Deploy focused MCP servers with narrow permissions
- Easier to audit and manage access
- Reduces over-privileged access risk

### Testing
```bash
# Test locally with MCP Inspector
npx @modelcontextprotocol/inspector

# Connect to: http://localhost:8787/mcp (default route)
```

## Migration: McpAgent → createMcpHandler

If migrating from `McpAgent` to `createMcpHandler`:

1. Move tool registrations from `init()` to top-level `server.tool()` calls
2. Remove `McpAgent` class wrapper
3. Export `createMcpHandler(server)` as default
4. Remove `durable_objects` and `migrations` from wrangler.jsonc (if MCP was the only DO)
5. Replace `this.env` bindings with Worker env parameter access
6. Replace `this.props` auth checks with `getMcpAuthContext()`

## Sources
- https://developers.cloudflare.com/agents/model-context-protocol/
- https://developers.cloudflare.com/agents/tutorials/build-a-remote-mcp-server/
- https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- https://developers.cloudflare.com/agents/third-party-packages/workers-oauth-provider/
- https://modelcontextprotocol.io/
