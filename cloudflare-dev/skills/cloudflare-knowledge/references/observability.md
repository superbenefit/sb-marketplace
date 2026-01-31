---
description: "Monitoring, logging, tracing, and analytics for Cloudflare Workers"
globs: ["src/**/*.ts", "wrangler.jsonc"]
alwaysApply: false
---

# Workers Observability

## CRITICAL: Enable Observability in wrangler.jsonc

**REQUIRED for Agents SDK projects and recommended for all Workers.**

```jsonc
// wrangler.jsonc
{
  "observability": {
    "enabled": true  // Enables Workers Logs, Traces, real-time logs
  }
}
```

Without this setting, `console.log()` output and trace data are NOT persisted.

## Workers Logs (Dashboard)

When `observability.enabled` is `true`, `console.log()` output is captured in the dashboard (**Workers & Pages > worker > Logs**). Retained 72 hours (free), longer on paid plans. Use structured JSON for filterability:

```typescript
console.log(JSON.stringify({
  level: "info",
  message: "Request received",
  method: request.method,
  url: request.url,
  timestamp: Date.now()
}));
```

## Real-Time Logs (wrangler tail)

```bash
npx wrangler tail                       # Stream live logs
npx wrangler tail --status error        # Filter errors only
npx wrangler tail --method POST         # Filter by HTTP method
npx wrangler tail --search "keyword"    # Filter by string match
npx wrangler tail --ip 203.0.113.1      # Filter by IP
npx wrangler tail --format json         # JSON output (pipe to jq)
npx wrangler tail --env staging         # Specific environment
```

## Tail Workers

Receive log data from a producer Worker for custom filtering, routing, or alerting.

```jsonc
// wrangler.jsonc (producer Worker)
{
  "tail_consumers": [{ "service": "my-tail-worker" }]
}
```

```typescript
// tail-worker/src/index.ts
export default {
  async tail(events: TraceItem[], env: Env): Promise<void> {
    for (const event of events) {
      if (event.outcome !== "ok" || event.exceptions.length > 0) {
        await env.ALERT_QUEUE.send({
          worker: event.scriptName,
          outcome: event.outcome,
          exceptions: event.exceptions,
          timestamp: event.eventTimestamp
        });
      }
      // Archive all logs to R2
      await env.LOG_BUCKET.put(
        `logs/${event.scriptName}/${Date.now()}.json`,
        JSON.stringify(event)
      );
    }
  }
};
```

Each `TraceItem` contains: `scriptName`, `event` (request/response), `logs[]` (level, message, timestamp), `exceptions[]`, `outcome` ("ok"|"exception"|"exceededCpu"|"exceededMemory"), `eventTimestamp`.

## Logpush

Push logs in batches to R2, S3, Azure Blob, GCS, Datadog, Splunk, Sumo Logic. Configure via dashboard or API:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/logpush/jobs" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "workers-logs-to-r2",
    "output_options": {
      "field_names": ["Event", "EventTimestampMs", "Outcome", "Logs", "ScriptName"]
    },
    "destination_conf": "r2://{bucket-name}/workers-logs/{date}?account-id={account_id}",
    "dataset": "workers_trace_events",
    "enabled": true
  }'
```

## Traces (Beta)

Automatic distributed tracing with OpenTelemetry-compatible spans. Requires `observability.enabled: true`.

### Auto-Instrumented Spans

| Operation | Span Name | Key Attributes |
|-----------|-----------|----------------|
| Incoming request | `fetch handler` | `http.method`, `http.url`, `http.status_code` |
| Outgoing `fetch()` | `fetch` | `http.method`, `http.url`, `http.status_code` |
| KV read/write | `KV GET`/`KV PUT` | `cloudflare.kv.key`, `cloudflare.kv.namespace_id` |
| R2 get/put | `R2 GET`/`R2 PUT` | `cloudflare.r2.key`, `cloudflare.r2.bucket_name` |
| D1 query | `D1 query` | `cloudflare.d1.query`, `cloudflare.d1.database_id` |
| Durable Object | `DO fetch` | `cloudflare.do.class_name`, `cloudflare.do.id` |
| Queue send | `Queue send` | `cloudflare.queue.name` |
| AI inference | `AI run` | `cloudflare.ai.model` |
| Vectorize | `Vectorize query` | `cloudflare.vectorize.index_name` |

### Custom Spans

```typescript
import { trace } from "cloudflare:workers";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    return trace("process-request", async (span) => {
      span.setAttribute("custom.user_id", "user-123");

      const data = await trace("fetch-data", async () => {
        return env.KV.get("my-key", "json");
      });

      return Response.json(await trace("transform", () => processData(data)));
    });
  }
};
```

## OpenTelemetry Export

Export traces via dashboard (**Workers & Pages > worker > Traces > Configure export**). Provide OTLP endpoint URL + auth headers.

| Provider | Endpoint |
|----------|----------|
| Honeycomb | `https://api.honeycomb.io` |
| Grafana Cloud | `https://otlp-gateway-{region}.grafana.net/otlp` |
| Axiom | `https://api.axiom.co` |
| Sentry | Sentry OTLP endpoint |
| Custom | Any OTLP-compatible endpoint |

## Analytics Engine

Unlimited-cardinality analytics. No sampling, no pre-aggregation. Write raw data points, query with SQL.

### Configuration

```jsonc
// wrangler.jsonc
{
  "analytics_engine_datasets": [
    { "binding": "ANALYTICS", "dataset": "my_app_events" }
  ]
}
```

### Writing Data Points

```typescript
// writeDataPoint: blobs (strings), doubles (numbers), indexes (grouping)
env.ANALYTICS.writeDataPoint({
  indexes: [url.pathname],                    // 1 index max (primary key)
  blobs: [request.method, userAgent, host],   // Up to 20 (blob1-blob20)
  doubles: [Date.now(), contentLength]         // Up to 20 (double1-double20)
});
```

| Field | Type | Max | SQL Columns |
|-------|------|-----|-------------|
| `indexes` | `string[]` | 1 | `index1` |
| `blobs` | `string[]` | 20 | `blob1`-`blob20` |
| `doubles` | `number[]` | 20 | `double1`-`double20` |
| (auto) | timestamp | 1 | `timestamp` |

### SQL Query API

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine/sql" \
  -H "Authorization: Bearer {api_token}" \
  -d "SELECT index1 AS path, blob1 AS method, COUNT() AS requests,
      SUM(double2) AS total_bytes
    FROM my_app_events
    WHERE timestamp > NOW() - INTERVAL '24' HOUR
    GROUP BY path, method ORDER BY requests DESC LIMIT 100"
```

**SQL functions**: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`, `QUANTILE()`, `IF()`, `intDiv()`, `toDateTime()`, `NOW()`, `INTERVAL`, `GROUP BY`, `ORDER BY`, `LIMIT`, `HAVING`, `FORMAT JSON`.

```typescript
// Query from a Worker
async function queryAnalytics(env: Env, sql: string) {
  const res = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/analytics_engine/sql`,
    { method: "POST", headers: { Authorization: `Bearer ${env.CF_API_TOKEN}` }, body: sql }
  );
  return res.json();
}
```

## Built-In Dashboard Metrics

Available without configuration in the Workers dashboard:

| Metric | Description |
|--------|-------------|
| Requests | Total count, success/error breakdown |
| Errors | Error rate, 4xx/5xx split |
| CPU Time | Wall time and CPU time per invocation |
| Duration | p50, p75, p99 percentiles |
| Data Transfer | Bytes in/out |
| Subrequests | Outbound fetch() count |
| Cron Triggers | Scheduled invocation metrics |

## DevTools (wrangler dev)

```bash
npx wrangler dev --inspect    # Attach Chrome DevTools
```

Capabilities: breakpoints, CPU profiling, memory inspection, interactive console, network request inspection.

## Quick Reference

| Need | Solution |
|------|----------|
| See live logs | `npx wrangler tail` |
| Persist console.log | `observability: { enabled: true }` in wrangler.jsonc |
| Custom log routing | Tail Workers (`tail_consumers`) |
| Bulk log export | Logpush to R2/S3/external |
| Distributed tracing | Traces (auto-instrumented) |
| Custom trace spans | `import { trace } from "cloudflare:workers"` |
| Export to Honeycomb/Grafana | OTLP export in dashboard |
| Custom analytics | Analytics Engine `writeDataPoint` + SQL |
| Debug locally | `wrangler dev --inspect` |

## Sources

- https://developers.cloudflare.com/workers/observability/
- https://developers.cloudflare.com/workers/observability/logs/workers-logs/
- https://developers.cloudflare.com/workers/observability/logs/tail-workers/
- https://developers.cloudflare.com/workers/observability/logs/logpush/
- https://developers.cloudflare.com/workers/observability/traces/
- https://developers.cloudflare.com/workers/observability/dev-tools/
- https://developers.cloudflare.com/analytics/analytics-engine/
- https://developers.cloudflare.com/analytics/analytics-engine/sql-api/
- https://developers.cloudflare.com/workers/wrangler/commands/#tail
