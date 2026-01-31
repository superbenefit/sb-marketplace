---
description: "Authentication patterns and deployment workflows for Cloudflare Workers"
globs: ["src/**/*.ts", "wrangler.jsonc", ".github/**"]
alwaysApply: false
---

# Authentication & Deployment for Cloudflare Workers

## workers-oauth-provider Library

The `workers-oauth-provider` package implements a full OAuth 2.1 server on Cloudflare Workers. It is the standard way to add authentication to MCP servers and other Worker-based APIs.

### Installation

```bash
npm install workers-oauth-provider
```

### OAuthProvider Class

The `OAuthProvider` wraps your Worker, intercepting OAuth routes and forwarding API requests to your handler.

```typescript
import { OAuthProvider } from "workers-oauth-provider";
import { McpHandler } from "./mcp-handler";
import { AuthHandler } from "./auth-handler";

export default new OAuthProvider({
  apiRoute: "/mcp",                           // Route prefix for your API/MCP handler
  apiHandler: McpHandler,                      // Worker handling API requests (receives authenticated requests)
  defaultHandler: AuthHandler,                 // Worker handling all non-API routes (login, callback, consent)
  authorizeEndpoint: "/authorize",             // OAuth authorization endpoint
  tokenEndpoint: "/token",                     // OAuth token exchange endpoint
  clientRegistrationEndpoint: "/register",     // Dynamic client registration (RFC 7591)
});
```

### OAuthProvider Configuration Reference

| Property | Type | Description |
|----------|------|-------------|
| `apiRoute` | `string` | Path prefix routed to `apiHandler` (e.g., `/mcp`) |
| `apiHandler` | `ExportedHandler` | Worker/DO that handles authenticated API requests |
| `defaultHandler` | `ExportedHandler` | Worker handling OAuth UI routes (authorize, callback) |
| `authorizeEndpoint` | `string` | Path for authorization requests (`/authorize`) |
| `tokenEndpoint` | `string` | Path for token exchange (`/token`) |
| `clientRegistrationEndpoint` | `string` | Path for dynamic client registration (`/register`) |

> **CRITICAL**: The `apiHandler` receives requests only after OAuth validation. The `defaultHandler` receives everything else -- use it for login pages, consent screens, and OAuth callbacks.

### OAUTH_KV Binding (Required)

The OAuthProvider stores tokens, authorization codes, and client registrations in a KV namespace. The binding **must** be named `OAUTH_KV`.

```jsonc
// wrangler.jsonc
{
  "name": "my-authenticated-server",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "kv_namespaces": [
    {
      "binding": "OAUTH_KV",
      "id": "<your-kv-namespace-id>"
    }
  ]
}
```

Create the namespace:
```bash
npx wrangler kv namespace create OAUTH_KV
# Copy the output id into wrangler.jsonc
```

> **CRITICAL**: Without the `OAUTH_KV` binding, OAuthProvider will throw at runtime. The binding name is not configurable.

## MCP Authentication Patterns (3 Options)

### Option 1: Self-Handled OAuth

Full control over user authentication. You implement login UI, credential verification, and token issuance entirely within your Worker.

```typescript
// src/auth-handler.ts
import { Hono } from "hono";
import { OAuthHelpers } from "workers-oauth-provider";

const app = new Hono<{ Bindings: Env }>();

app.get("/authorize", async (c) => {
  const oauthReqInfo = await c.env.OAUTH_PROVIDER.parseAuthRequest(c.req.raw);
  // Render login form or redirect to consent page
  return c.html(`
    <form method="POST" action="/authorize">
      <input type="hidden" name="oauthReqInfo" value='${JSON.stringify(oauthReqInfo)}' />
      <input name="email" type="email" required />
      <input name="password" type="password" required />
      <button type="submit">Login</button>
    </form>
  `);
});

app.post("/authorize", async (c) => {
  const body = await c.req.parseBody();
  const user = await verifyCredentials(body.email, body.password);
  if (!user) return c.text("Unauthorized", 401);

  // Complete OAuth flow - issues authorization code
  return OAuthHelpers.completeAuthorization(c.env.OAUTH_PROVIDER, {
    request: c.req.raw,
    userId: user.id,
    metadata: { email: user.email, role: user.role },
    scope: oauthReqInfo.scope,
    props: { userId: user.id, email: user.email },
  });
});

export const AuthHandler = app;
```

### Option 2: Third-Party OAuth (GitHub, Google)

Redirect users to an external identity provider, then exchange the callback code.

```typescript
// src/auth-handler.ts -- GitHub OAuth example
import { OAuthHelpers } from "workers-oauth-provider";

export const AuthHandler = {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/authorize") {
      // Store OAuth request info, redirect to GitHub
      const oauthReqInfo = await env.OAUTH_PROVIDER.parseAuthRequest(request);
      await env.OAUTH_KV.put(`pending:${state}`, JSON.stringify(oauthReqInfo), { expirationTtl: 600 });

      const githubAuthUrl = new URL("https://github.com/login/oauth/authorize");
      githubAuthUrl.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
      githubAuthUrl.searchParams.set("redirect_uri", `${url.origin}/callback`);
      githubAuthUrl.searchParams.set("state", state);
      githubAuthUrl.searchParams.set("scope", "read:user user:email");
      return Response.redirect(githubAuthUrl.toString());
    }

    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      const state = url.searchParams.get("state");

      // Exchange code with GitHub
      const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code,
        }),
      });
      const { access_token } = await tokenRes.json();

      // Fetch user info from GitHub
      const userRes = await fetch("https://api.github.com/user", {
        headers: { Authorization: `Bearer ${access_token}`, "User-Agent": "CF-Worker" },
      });
      const ghUser = await userRes.json();

      // Complete the OAuth flow
      const oauthReqInfo = JSON.parse(await env.OAUTH_KV.get(`pending:${state}`));
      return OAuthHelpers.completeAuthorization(env.OAUTH_PROVIDER, {
        request,
        userId: ghUser.id.toString(),
        metadata: { login: ghUser.login, avatar: ghUser.avatar_url },
        scope: oauthReqInfo.scope,
        props: { githubId: ghUser.id, login: ghUser.login },
      });
    }

    return new Response("Not found", { status: 404 });
  },
};
```

### Option 3: Bring-Your-Own Auth (Stytch, Auth0, WorkOS)

Integrate an existing auth provider SDK. The pattern is the same as third-party OAuth, but you use the provider's SDK for token exchange and user lookup.

```typescript
// Example with Auth0
import { OAuthHelpers } from "workers-oauth-provider";

// In /authorize: redirect to Auth0 universal login
const auth0Url = `https://${env.AUTH0_DOMAIN}/authorize?` +
  `client_id=${env.AUTH0_CLIENT_ID}&` +
  `redirect_uri=${url.origin}/callback&` +
  `response_type=code&scope=openid profile email&state=${state}`;

// In /callback: exchange code and get user info
const tokenRes = await fetch(`https://${env.AUTH0_DOMAIN}/oauth/token`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    grant_type: "authorization_code",
    client_id: env.AUTH0_CLIENT_ID,
    client_secret: env.AUTH0_CLIENT_SECRET,
    code,
    redirect_uri: `${url.origin}/callback`,
  }),
});
```

## getMcpAuthContext()

Access authenticated user identity inside MCP tool handlers. Returns the `props` object passed during `completeAuthorization`.

```typescript
import { getMcpAuthContext } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "auth-server", version: "1.0.0" });

server.tool(
  "get_user_data",
  "Fetch data for the authenticated user",
  { filter: z.string().optional() },
  async ({ filter }) => {
    const authContext = getMcpAuthContext();
    if (!authContext) {
      return { content: [{ type: "text", text: "Authentication required" }], isError: true };
    }

    // authContext contains props from completeAuthorization
    const { userId, email, role } = authContext;
    const data = await fetchUserData(userId, filter);

    return { content: [{ type: "text", text: JSON.stringify(data) }] };
  }
);
```

> **CRITICAL**: `getMcpAuthContext()` uses AsyncLocalStorage internally. It only works inside tool handler callbacks when the request was routed through `OAuthProvider`. Returns `null` for unauthenticated requests.

## Workers Builds (CI/CD)

Workers Builds is Cloudflare's built-in CI/CD system. Connect a GitHub or GitLab repository and Cloudflare automatically builds and deploys on push.

### Enabling Workers Builds

1. Go to **Workers & Pages > Your Worker > Settings > Builds**
2. Connect your GitHub or GitLab repository
3. Configure build settings

### Build Configuration in wrangler.jsonc

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-01",
  // Build configuration
  "build": {
    "command": "npm run build",        // Build command
    "cwd": "packages/worker",         // Working directory (monorepo support)
    "watch_dir": "src"                 // Directory to watch for changes
  }
}
```

### Branch Control

Configure which branches trigger deployments:

| Setting | Description |
|---------|-------------|
| **Production branch** | Branch that deploys to production (e.g., `main`) |
| **Preview branches** | Branches that deploy to preview environments |
| **Branch includes** | Glob patterns for branches to build (e.g., `feature/*`) |
| **Branch excludes** | Glob patterns for branches to skip |

### Build Caching

Workers Builds caches `node_modules` and build artifacts between builds. To optimize:
- Use a lockfile (`package-lock.json`, `pnpm-lock.yaml`)
- Build output is cached automatically
- Cache is invalidated when lockfile changes

### Watch Paths (Monorepo Support)

For monorepos, configure watch paths so builds only trigger when relevant files change:

```jsonc
// wrangler.jsonc for a monorepo package
{
  "name": "api-worker",
  "main": "src/index.ts",
  "build": {
    "command": "npm run build",
    "cwd": "packages/api",
    "watch_dir": "packages/api/src"
  }
}
```

### Environment Variables in Builds

Available during the build process:

| Variable | Description |
|----------|-------------|
| `CF_PAGES_BRANCH` | Git branch being built |
| `CF_PAGES_COMMIT_SHA` | Full commit SHA |
| `CF_PAGES_URL` | URL of the deployment |
| `WORKERS_CI` | Set to `true` during Workers Builds |

Set custom build environment variables in the Cloudflare dashboard under **Settings > Builds > Environment variables**, or in wrangler.jsonc:

```jsonc
{
  "vars": {
    "API_VERSION": "v2",
    "NODE_ENV": "production"
  }
}
```

## External CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy Worker
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Deploy to Cloudflare Workers
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          # Optional: specify wrangler version
          # wranglerVersion: "3"
          # Optional: specify environment
          # environment: "production"
          # Optional: custom deploy command
          # command: "deploy --minify"
```

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:
  image: node:20
  stage: deploy
  only:
    - main
  before_script:
    - npm ci
  script:
    - npx wrangler deploy
  variables:
    CLOUDFLARE_API_TOKEN: $CLOUDFLARE_API_TOKEN
    CLOUDFLARE_ACCOUNT_ID: $CLOUDFLARE_ACCOUNT_ID
```

### Creating an API Token

1. Go to **Cloudflare Dashboard > My Profile > API Tokens**
2. Click **Create Token**
3. Use the **Edit Cloudflare Workers** template (or create custom)
4. Required permissions: `Account > Cloudflare Workers > Edit`
5. Store as `CLOUDFLARE_API_TOKEN` in your CI secrets

> **CRITICAL**: Never commit API tokens to your repository. Always use CI/CD secrets or environment variables.

## Secrets Management

### wrangler secret put (Production)

```bash
# Set a secret interactively (prompts for value)
npx wrangler secret put SECRET_NAME

# Set from a value
echo "secret-value" | npx wrangler secret put SECRET_NAME

# Set for a specific environment
npx wrangler secret put SECRET_NAME --env production

# List all secrets (names only, values hidden)
npx wrangler secret list

# Delete a secret
npx wrangler secret delete SECRET_NAME
```

### Bulk Secrets

```bash
# Set multiple secrets from a JSON file
npx wrangler secret bulk secrets.json

# secrets.json format:
# { "API_KEY": "value1", "DB_PASSWORD": "value2" }
```

### .dev.vars (Local Development)

For local development with `wrangler dev`, create a `.dev.vars` file in your project root:

```bash
# .dev.vars - NOT committed to git
SECRET_API_KEY=sk-dev-1234567890
DATABASE_URL=postgresql://localhost:5432/mydb
GITHUB_CLIENT_SECRET=ghp_xxxxxxxxxxxx
AUTH0_CLIENT_SECRET=xxxxxxxxxxxxxxxx
```

> **CRITICAL**: Add `.dev.vars` to `.gitignore`. This file is only used by `wrangler dev` and should never be committed.

### Accessing Secrets in Code

Secrets are accessed the same way as environment variables through the `env` parameter:

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Secrets and vars accessed identically
    const apiKey = env.SECRET_API_KEY;
    const dbUrl = env.DATABASE_URL;
    return new Response("OK");
  },
};

interface Env {
  SECRET_API_KEY: string;
  DATABASE_URL: string;
}
```

### Secrets vs Vars

| Feature | Secrets (`wrangler secret`) | Vars (`wrangler.jsonc vars`) |
|---------|---------------------------|------------------------------|
| Encrypted at rest | Yes | No |
| Visible in dashboard | Hidden | Visible |
| In version control | Never | Yes (non-sensitive only) |
| Set via | CLI or API | Config file or dashboard |
| Use for | API keys, tokens, passwords | Feature flags, public config |

## Deploy Buttons

Deploy Buttons let users deploy a Worker directly from a URL. Cloudflare reads the `wrangler.jsonc` to automatically provision required resources (KV, D1, R2, etc.).

### Creating a Deploy Button

```markdown
[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/your-org/your-repo)
```

### How It Works

1. User clicks the deploy button
2. Cloudflare forks the repository to the user's GitHub
3. Reads `wrangler.jsonc` to determine required resources
4. Automatically provisions: KV namespaces, D1 databases, R2 buckets, Durable Objects, etc.
5. Sets up Workers Builds for automatic deployments
6. Deploys the Worker

### Supported Auto-Provisioned Resources

From `wrangler.jsonc`, deploy buttons automatically create:
- **KV namespaces** (`kv_namespaces`)
- **D1 databases** (`d1_databases`)
- **R2 buckets** (`r2_buckets`)
- **Durable Objects** (`durable_objects`)
- **Queues** (`queues`)
- **Vectorize indexes** (`vectorize`)
- **AI bindings** (`ai`)

### Deploy Button for MCP Servers

Common pattern for deploying authenticated MCP servers:

```jsonc
// wrangler.jsonc -- deploy button will auto-provision OAUTH_KV
{
  "name": "my-mcp-server",
  "main": "src/index.ts",
  "compatibility_date": "2025-03-07",
  "compatibility_flags": ["nodejs_compat"],
  "kv_namespaces": [
    { "binding": "OAUTH_KV", "id": "" }
  ],
  "durable_objects": {
    "bindings": [
      { "name": "MCP_AGENT", "class_name": "MyMcpAgent" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["MyMcpAgent"] }
  ]
}
```

> **NOTE**: The `id` field for KV can be empty in the template -- the deploy button process creates the namespace and fills in the ID.

## Sources

- https://developers.cloudflare.com/agents/third-party-packages/workers-oauth-provider/
- https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- https://developers.cloudflare.com/agents/tutorials/build-a-remote-mcp-server/
- https://developers.cloudflare.com/agents/model-context-protocol/
- https://developers.cloudflare.com/workers/ci-cd/builds/
- https://developers.cloudflare.com/workers/ci-cd/builds/build-caching/
- https://developers.cloudflare.com/workers/ci-cd/builds/build-watch-paths/
- https://developers.cloudflare.com/workers/ci-cd/external-cicd/
- https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/
- https://developers.cloudflare.com/workers/ci-cd/external-cicd/gitlab-ci/
- https://developers.cloudflare.com/workers/configuration/secrets/
- https://developers.cloudflare.com/workers/platform/deploy-buttons/
- https://github.com/cloudflare/workers-oauth-provider
