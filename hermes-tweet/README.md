# Hermes Tweet

Hermes Tweet is a native Hermes Agent plugin for X/Twitter research,
monitoring, timeline review, tweet analysis, and explicitly gated action
workflows through Xquik.

## Install

Add the marketplace, then install the plugin:

```json
{
  "enabledPlugins": {
    "hermes-tweet@sb-marketplace": true
  }
}
```

For the upstream Hermes Agent runtime, install and enable Hermes Tweet directly:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Hermes prompts for `XQUIK_API_KEY` during interactive install. In
non-interactive sessions, set `XQUIK_API_KEY` in the process environment or
`~/.hermes/.env` before running read tools.

## Capabilities

- Search tweets, profiles, timelines, and tweet context.
- Use read-first workflows for social research and monitoring.
- Keep write actions disabled unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Review the upstream guide before production use:
  <https://github.com/Xquik-dev/hermes-tweet#readme>.
