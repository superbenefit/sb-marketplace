---
description: Cloudflare Workflows for durable execution with automatic retries, state persistence, waitForEvent, and long-running tasks
globs: ["src/sync/**", "src/workflows/**", "*.ts"]
alwaysApply: false
---

# Cloudflare Workflows

## Overview

Workflows provide durable execution - applications that:
- Execute reliably with automatic retries
- Persist state automatically
- Survive infrastructure failures
- Run for minutes, hours, days, or weeks

## Key Concepts

| Term | Definition |
|------|------------|
| **Durable Execution** | Programming model for reliable, resumable execution |
| **Step** | Self-contained, individually retriable unit of work |
| **Workflow Instance** | Single execution of a Workflow with unique ID |
| **Event** | Trigger with optional payload data |

## Workflow Definition

```typescript
import {
  WorkflowEntrypoint,
  WorkflowStep,
  WorkflowEvent
} from "cloudflare:workers";
import { NonRetryableError } from "cloudflare:workflows";

interface Env {
  MY_WORKFLOW: Workflow;
  R2: R2Bucket;
}

interface SyncParams {
  source: string;
  triggerType: "webhook" | "manual";
}

export class ContentSyncWorkflow extends WorkflowEntrypoint<Env, SyncParams> {
  async run(event: WorkflowEvent<SyncParams>, step: WorkflowStep) {
    const { source } = event.payload;

    // Step 1: Fetch content
    const files = await step.do("fetch-content", async () => {
      const response = await fetch(source);
      return response.json();
    });

    // Step 2: Process each file (with retry config)
    for (const file of files) {
      await step.do(
        `process-${file.name}`,
        {
          retries: {
            limit: 3,
            delay: "10 seconds",
            backoff: "exponential"
          },
          timeout: "5 minutes"
        },
        async () => {
          await this.env.R2.put(`content/${file.path}`, file.content);
        }
      );

      // Rate limit between files
      await step.sleep("rate-limit", "500 milliseconds");
    }

    return {
      success: true,
      filesProcessed: files.length,
      timestamp: new Date().toISOString()
    };
  }
}
```

## Step Configuration

```typescript
interface WorkflowStepConfig {
  retries?: {
    limit: number;           // Max retry attempts
    delay: string;           // Initial delay ("5 seconds", "1 minute")
    backoff?: "constant" | "linear" | "exponential";
  };
  timeout?: string;          // Max duration ("15 minutes", "1 hour")
}

// With full config
await step.do(
  "risky-operation",
  {
    retries: {
      limit: 5,
      delay: "5 seconds",
      backoff: "exponential"  // 5s, 10s, 20s, 40s, 80s
    },
    timeout: "10 minutes"
  },
  async () => {
    // Work that may fail
  }
);
```

## Waiting for External Events (step.waitForEvent)

Pause a workflow until an external event is received. Ideal for human-in-the-loop approvals, webhook callbacks, or cross-workflow coordination.

```typescript
export class ApprovalWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    // Step 1: Submit for review
    const submission = await step.do("submit-for-review", async () => {
      // Create review request, notify reviewers
      return { reviewId: "review-123" };
    });

    // Step 2: Wait for approval event
    const approval = await step.waitForEvent<{ approved: boolean; reviewer: string }>(
      "wait-for-approval",
      {
        type: "approval-response",  // Event type to match
        timeout: "7 days"           // Max wait time
      }
    );

    // Step 3: Act on the result
    if (approval.payload.approved) {
      await step.do("deploy", async () => {
        // Proceed with deployment
      });
    } else {
      await step.do("notify-rejection", async () => {
        // Handle rejection
      });
    }
  }
}
```

### Sending Events to a Waiting Workflow

```typescript
// From a Worker or Agent
const instance = await env.MY_WORKFLOW.get(instanceId);

await instance.sendEvent({
  type: "approval-response",
  payload: {
    approved: true,
    reviewer: "user@example.com"
  }
});
```

### waitForEvent Config

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `string` | Event type to match (only letters, digits, `-`, `_` - no `.`) |
| `timeout` | `string` | Max wait duration (`"5 minutes"`, `"7 days"`). Default: 24 hours. Range: 1 second to 365 days. |

**Important**: When `waitForEvent` times out, the Workflow throws an error and the instance **fails**. Wrap in `try/catch` if you want the Workflow to continue on timeout.

## Sleeping

```typescript
// Delay strings
await step.sleep("delay-name", "30 seconds");
await step.sleep("delay-name", "5 minutes");
await step.sleep("delay-name", "2 hours");
await step.sleep("delay-name", "1 day");

// Sleep until specific time
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
await step.sleepUntil("wait-until-tomorrow", tomorrow);
```

## Error Handling

### Catch and Continue

```typescript
try {
  await step.do("might-fail", async () => {
    // Risky operation
  });
} catch (error) {
  console.log(`Step failed: ${error.message}`);

  await step.do("cleanup", async () => {
    // Recovery logic
  });
}

// Workflow continues execution
await step.do("next-step", async () => {
  // Continue working
});
```

### Force Failure (No Retry)

```typescript
import { NonRetryableError } from "cloudflare:workflows";

await step.do("validate-input", async () => {
  if (!event.payload.required_field) {
    throw new NonRetryableError("Missing required_field");
  }
});
```

## Triggering Workflows

### From a Worker

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const data = await request.json();

    const instance = await env.MY_WORKFLOW.create({
      id: crypto.randomUUID(),
      params: {
        source: data.source,
        triggerType: "manual"
      }
    });

    return Response.json({
      instanceId: instance.id,
      status: await instance.status()
    });
  }
};
```

### Check Instance Status

```typescript
const instance = await env.MY_WORKFLOW.get(instanceId);
const status = await instance.status();
// {
//   status: "running" | "complete" | "errored" | "queued",
//   output?: any,
//   error?: string
// }
```

### Webhook Trigger

```typescript
export default {
  async fetch(request: Request, env: Env) {
    if (request.method === "POST" &&
        new URL(request.url).pathname === "/webhook") {

      const payload = await request.json();

      // Idempotent: use webhook delivery ID
      const instanceId = `webhook-${payload.delivery_id}`;

      const instance = await env.MY_WORKFLOW.create({
        id: instanceId,
        params: payload
      });

      return Response.json({ instanceId: instance.id });
    }
  }
};
```

## Configuration (wrangler.jsonc)

```jsonc
{
  "name": "my-workflows",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "workflows": [{
    "name": "content-sync",
    "binding": "MY_WORKFLOW",
    "class_name": "ContentSyncWorkflow"
  }],
  "r2_buckets": [{
    "binding": "R2",
    "bucket_name": "my-content"
  }],
  "observability": {
    "enabled": true
  }
}
```

## Rules of Workflows (CRITICAL)

### 1. Always Await Steps

```typescript
// ✅ CORRECT
await step.do("name", async () => { ... });
await step.sleep("delay", "5 seconds");

// ❌ WRONG - step not awaited
step.do("name", async () => { ... });
```

### 2. Steps Must Be Idempotent

Steps may retry - ensure operations are safe to repeat:

```typescript
// ✅ CORRECT - idempotent upsert
await step.do("store-data", async () => {
  await env.R2.put(key, data);  // Overwrites if exists
});

// ❌ RISKY - may duplicate
await step.do("append-data", async () => {
  const existing = await env.R2.get(key);
  await env.R2.put(key, existing + data);  // Duplicates on retry
});
```

### 3. Return Serializable Data

```typescript
// ✅ CORRECT - serializable
await step.do("get-data", async () => {
  return { id: 123, name: "test" };
});

// ❌ WRONG - functions not serializable
await step.do("get-data", async () => {
  return { process: () => {} };
});
```

### 4. No Side Effects Outside Steps

```typescript
// ❌ WRONG - side effect outside step
console.log("Starting workflow");  // May log multiple times

// ✅ CORRECT - side effects inside steps
await step.do("log-start", async () => {
  console.log("Starting workflow");
});
```

### 5. Access Bindings via this.env

```typescript
// ✅ CORRECT
await step.do("use-binding", async () => {
  await this.env.R2.put(key, data);
});

// ❌ WRONG - closure over env
const r2 = env.R2;  // Don't capture in closure
await step.do("use-binding", async () => {
  await r2.put(key, data);  // May not work after hibernation
});
```

## Calling Workflows from Agents

```typescript
import { Agent } from "agents";

export class SyncAgent extends Agent<Env> {
  async triggerSync(source: string) {
    const instance = await this.env.MY_WORKFLOW.create({
      id: `sync-${Date.now()}`,
      params: { source, triggerType: "manual" }
    });

    await this.schedule(60, "checkStatus", { instanceId: instance.id });
    return instance.id;
  }

  async checkStatus(data: { instanceId: string }) {
    const instance = await this.env.MY_WORKFLOW.get(data.instanceId);
    const status = await instance.status();

    if (status.status === "running") {
      await this.schedule(60, "checkStatus", data);
    } else {
      this.setState({
        ...this.state,
        lastSync: { instanceId: data.instanceId, ...status }
      });
    }
  }
}
```

## Python Workflows SDK (Beta)

A Python SDK for Workflows is available (beta, requires `compatibility_date >= "2025-08-01"`). See the Cloudflare docs for Python-specific syntax including `step.do` with `depends` parameter for DAG-style step dependencies.

## Best Practices

1. **Unique Instance IDs**: Use deterministic IDs for idempotency
2. **Granular Steps**: Break work into small, retriable units
3. **Error Boundaries**: Wrap risky operations in try-catch
4. **Reasonable Timeouts**: Set appropriate timeouts per step
5. **Rate Limiting**: Use `step.sleep()` between API calls
6. **Status Tracking**: Poll `instance.status()` for monitoring
7. **waitForEvent for approvals**: Use instead of polling for human-in-the-loop

## Sources
- https://developers.cloudflare.com/workflows/
- https://developers.cloudflare.com/workflows/build/events-and-parameters/
- https://developers.cloudflare.com/workflows/build/sleeping-and-retrying/
- https://developers.cloudflare.com/workflows/build/trigger-workflows/
- https://developers.cloudflare.com/workflows/build/wait-for-event/
