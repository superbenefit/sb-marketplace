---
name: hermes-tweet
description: >
  Guide Hermes Agent users through safe X/Twitter research, monitoring, and
  opt-in action workflows with Hermes Tweet.
---

# Hermes Tweet

Use this skill when a user wants Hermes Agent support for X/Twitter research,
social listening, tweet analysis, profile context, timeline review, or
approval-gated X/Twitter actions through Hermes Tweet.

## Workflow

1. Confirm the user wants the Hermes Agent plugin for X/Twitter workflows.
2. Prefer read-first tasks such as search, profile context, timeline review,
   monitoring, and tweet analysis.
3. Point upstream runtime installs to:
   `hermes plugins install Xquik-dev/hermes-tweet --enable`.
4. Tell the user to set `XQUIK_API_KEY` through Hermes' interactive prompt, the
   process environment, or `~/.hermes/.env`. Never ask them to paste secrets
   into chat.
5. Treat write actions as opt-in only. They require
   `HERMES_TWEET_ENABLE_ACTIONS=true` in addition to `XQUIK_API_KEY`.
6. Use the upstream guide for current install and safety details:
   <https://github.com/Xquik-dev/hermes-tweet#readme>.
