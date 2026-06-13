# SuperBenefit Plugin Marketplace

Claude Code plugin marketplace for the SuperBenefit community. Provides development toolkits, platform-specific automation, and social intelligence workflows through the Claude Code plugin system.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [astro-dev](./astro-dev/) | 0.4.0 | Astro/Starlight development toolkit with tiered knowledge loading |
| [cloudflare-dev](./cloudflare-dev/) | 0.1.0 | Cloudflare Workers, Agents SDK, MCP, Vectorize, and Workflows toolkit |
| [project-mgmt](./project-mgmt/) | 0.1.0 | Spec-driven development with persistent markdown planning |
| [hermes-tweet](./hermes-tweet/) | 0.1.6 | Hermes Agent X/Twitter research and automation with opt-in actions |

## Installation

Add the marketplace to your Claude Code settings (global `~/.claude/settings.json` or project `.claude/settings.local.json`):

```json
{
  "extraKnownMarketplaces": {
    "sb-marketplace": {
      "source": {
        "source": "github",
        "repo": "superbenefit/sb-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "astro-dev@sb-marketplace": true,
    "cloudflare-dev@sb-marketplace": true,
    "project-mgmt@sb-marketplace": true,
    "hermes-tweet@sb-marketplace": true
  }
}
```

Enable only the plugins you need. Restart Claude Code after editing settings.

## Plugin Summary

### astro-dev

Astro and Starlight development toolkit with intelligent tiered knowledge loading. Includes a comprehensive knowledge base with 100+ error patterns, implementation guides, and deep-dive references.

**Commands**: `/dev`, `/design`, `/lookup`
**Skills**: astro-coding (implementation patterns), astro-knowledge (API reference)
**MCP**: Astro docs server integration

See [astro-dev/README.md](./astro-dev/README.md) for full documentation.

### cloudflare-dev

Cloudflare developer platform toolkit covering Workers, Agents SDK, MCP servers, Vectorize, Workflows, and all platform bindings. Includes 8 audited reference files and 3 specialized agents.

**Commands**: `/cf-dev`, `/validate`, `/deploy-check`, `/test-mcp`
**Agents**: cf-validator, cloudflare-helper, docs-writer
**Skills**: cloudflare-knowledge (8 reference files)
**MCP**: Cloudflare docs server integration

See [cloudflare-dev/README.md](./cloudflare-dev/README.md) for full documentation.

### project-mgmt

Spec-driven development with persistent markdown planning. Uses the filesystem as persistent memory with plan.md, spec.md, findings.md, and progress.md in `.project/{issue#}/` directories.

**Skills**: project-mgmt (6-phase workflow with progressive disclosure)
**Agents**: pm-bookkeeper (background file updates, Haiku)

See [project-mgmt/README.md](./project-mgmt/README.md) for full documentation.

### hermes-tweet

Hermes Agent X/Twitter plugin for social research, timeline review, tweet analysis, and explicitly gated action workflows through Xquik.

**Skills**: hermes-tweet (read-first workflow guide)
**Runtime**: Native Hermes Agent plugin
**Actions**: Require explicit `HERMES_TWEET_ENABLE_ACTIONS=true`

See [hermes-tweet/README.md](./hermes-tweet/README.md) for full documentation.

## Contributing

Contributions are welcome from the SuperBenefit community and beyond.

- **Astro knowledge**: Update files in `astro-dev/knowledge-base/`
- **Cloudflare knowledge**: Update files in `cloudflare-dev/skills/cloudflare-knowledge/references/`
- **Plugin manifests**: `<plugin>/.claude-plugin/plugin.json`
- **Marketplace manifest**: `.claude-plugin/marketplace.json`

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## Support

- **Issues**: [GitHub Issues](https://github.com/superbenefit/sb-marketplace/issues)
- **Email**: rathermercurial@protonmail.com
- **Community**: [SuperBenefit](https://superbenefit.org) (info@superbenefit.org)

## License

CC0 1.0 Universal - Public Domain Dedication

Created by rathermercurial.eth for the SuperBenefit community.
