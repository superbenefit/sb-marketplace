---
description: Core Agent class API, WebSocket handling, state management, scheduling, and SQL for Cloudflare Agents SDK
globs: ["src/**/*.ts", "*.ts"]
alwaysApply: false
---

# Cloudflare Agents SDK

## Overview

The Agents SDK enables building AI-powered agents that:
- Autonomously perform tasks
- Communicate with clients in real time via WebSockets
- Call AI models
- Persist state
- Schedule tasks
- Run asynchronous workflows
- Browse the web
- Support human-in-the-loop interactions

## Installation

```bash
npm i agents
```

## Agent Class Definition

```typescript
import { Agent } from "agents";

interface Env {
  // Bindings and environment variables
}

interface MyState {
  counter: number;
  messages: Array<{ sender: string; text: string }>;
  lastUpdated: Date | null;
}

export class MyAgent extends Agent<Env, MyState> {
  // Optional initial state
  initialState: MyState = {
    counter: 0,
    messages: [],
    lastUpdated: null
  };

  // Called when agent starts or wakes from hibernation
  async onStart() {
    console.log("Agent started with state:", this.state);
  }

  // Handle HTTP requests
  async onRequest(request: Request): Promise<Response> {
    return new Response("Hello from Agent!");
  }

  // Called when WebSocket connection established
  async onConnect(connection: Connection, ctx: ConnectionContext) {
    // Connections auto-accepted by SDK
    // Access original request: ctx.request
  }

  // Handle WebSocket messages
  async onMessage(connection: Connection, message: WSMessage) {
    connection.send("Received your message");
  }

  // Handle WebSocket errors
  async onError(connection: Connection, error: unknown) {
    console.error("Connection error:", error);
  }

  // Handle WebSocket close
  async onClose(connection: Connection, code: number, reason: string, wasClean: boolean) {
    console.log(`Connection closed: ${code} - ${reason}`);
  }

  // Called when state updated from any source
  onStateUpdate(state: MyState, source: "server" | Connection) {
    console.log("State updated:", state, "Source:", source);
  }
}
```

## State Management

### setState API

```typescript
// Get current state
const current = this.state;

// Update state - persists to storage and notifies connected clients
this.setState({
  ...this.state,
  counter: this.state.counter + 1,
  lastUpdated: new Date()
});
```

### State Synchronization

State automatically syncs between server and connected clients:
- Server updates via `this.setState()` broadcast to all clients
- Client updates via `agent.setState()` sync to server
- `onStateUpdate` callback fires on any change

## SQL API (Embedded SQLite)

Each Agent instance has an embedded SQLite database via `this.sql`:

```typescript
// Create table
this.sql`
  CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at INTEGER
  )
`;

// Insert
this.sql`
  INSERT INTO users (id, name, email, created_at)
  VALUES (${id}, ${name}, ${email}, ${Date.now()})
`;

// Query with type parameter
const users = this.sql<User>`
  SELECT * FROM users WHERE id = ${id}
`;

// Search with wildcards
const results = this.sql<User>`
  SELECT * FROM users
  WHERE name LIKE ${"%" + term + "%"}
  ORDER BY created_at DESC
`;
```

## Scheduling API

Schedule tasks to run in the future:

```typescript
// Schedule in N seconds
const task = await this.schedule(10, "sendReminder", { userId, message });

// Schedule at specific date
const task = await this.schedule(
  new Date("2025-02-01T08:00:00Z"),
  "generateReport",
  { reportType: "daily" }
);

// Schedule with cron (every day at 8 AM)
const task = await this.schedule(
  "0 8 * * *",
  "dailyTask",
  { type: "summary" }
);

// Get schedule by ID
const schedule = await this.getSchedule(taskId);

// Get all schedules
const allSchedules = this.getSchedules();

// Filter schedules
const upcoming = this.getSchedules({
  timeRange: {
    start: new Date(),
    end: new Date(Date.now() + 24 * 60 * 60 * 1000)
  }
});

// Cancel schedule
await this.cancelSchedule(taskId);
```

### Schedule Object Types

```typescript
type Schedule<T> = {
  id: string;
  callback: string;  // Method name to call
  payload: T;
} & (
  | { type: "scheduled"; time: number }
  | { type: "delayed"; time: number; delayInSeconds: number }
  | { type: "cron"; time: number; cron: string }
);
```

## WebSocket API

### Connection Interface

```typescript
interface Connection<State = unknown> {
  id: string;
  state: State;
  setState(state: State): void;
  accept(): void;
  close(code?: number, reason?: string): void;
  send(message: string | ArrayBuffer | ArrayBufferView): void;
}
```

### WebSocket Message Types

```typescript
type WSMessage = string | ArrayBuffer | ArrayBufferView;
```

### Handling WebSocket Messages

```typescript
async onMessage(connection: Connection, message: WSMessage) {
  if (typeof message === "string") {
    const data = JSON.parse(message);

    if (data.type === "update") {
      // Update connection-specific state
      connection.setState({ ...connection.state, lastActive: Date.now() });

      // Update global agent state
      this.setState({ ...this.state, connections: this.state.connections + 1 });

      // Send response
      connection.send(JSON.stringify({ type: "ack", status: "success" }));
    }
  }
}
```

## Calling Agents

### Route-based Addressing

```typescript
import { routeAgentRequest } from "agents";

export default {
  async fetch(request, env) {
    // Routes to /agents/:agent/:name automatically
    return await routeAgentRequest(request, env)
      || Response.json({ msg: "no agent" }, { status: 404 });
  }
};
```

### Named Addressing

```typescript
import { getAgentByName } from "agents";

const agent = await getAgentByName<Env, MyAgent>(env.MyAgent, "user-123");
const response = await agent.fetch(request);

// Call methods directly via RPC
const result = await agent.processTask(data);
```

### Authentication Hooks

```typescript
await routeAgentRequest(request, env, {
  onBeforeConnect: (request) => {
    // Validate WebSocket connections
    // Return Response to reject
  },
  onBeforeRequest: (request) => {
    // Validate HTTP requests
  },
  prefix: "my-prefix"
});
```

## Client APIs

### AgentClient (Browser)

```typescript
import { AgentClient } from "agents/client";

const client = new AgentClient({
  agent: "my-agent",  // Class name in kebab-case
  name: "instance-123"
});

client.onopen = () => console.log("Connected");
client.onmessage = (event) => console.log("Received:", event.data);
client.send(JSON.stringify({ type: "message", text: "Hello" }));
```

### useAgent React Hook

```typescript
import { useAgent } from "agents/react";

function App() {
  const agent = useAgent({
    agent: "my-agent",
    name: "instance-123",
    onMessage: (message) => console.log(message.data),
    onStateUpdate: (state) => setLocalState(state)
  });

  return (
    <button onClick={() => agent.send(JSON.stringify({ action: "click" }))}>
      Send
    </button>
  );
}
```

## Configuration (wrangler.jsonc)

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-agent",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "durable_objects": {
    "bindings": [
      {
        "name": "MyAgent",
        "class_name": "MyAgent"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": ["MyAgent"]  // REQUIRED for state storage
    }
  ],
  "observability": {
    "enabled": true
  }
}
```

## Critical Requirements

1. **new_sqlite_classes**: MUST include Agent class name in migrations
2. **WebSocket Hibernation**: Agents use hibernation API by default (cost-efficient)
3. **Type Parameters**: Always provide `<Env, State>` to Agent class
4. **State Serialization**: State must be JSON-serializable
5. **SQL Tagged Templates**: Always use `this.sql\`...\`` syntax, not string concatenation

## Sources
- https://developers.cloudflare.com/agents/api-reference/
- https://developers.cloudflare.com/agents/concepts/agent-class/
- https://developers.cloudflare.com/agents/concepts/state/
- https://developers.cloudflare.com/agents/concepts/scheduling/
- https://developers.cloudflare.com/agents/concepts/websockets/
- https://developers.cloudflare.com/agents/llms-full.txt
