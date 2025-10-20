# Contributing to sb-marketplace

Thank you for your interest in contributing to the SuperBenefit Astro Dev Marketplace! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Report Issues
Found a bug or have a feature request?
- Check [existing issues](https://github.com/superbenefit/sb-marketplace/issues) first
- Create a new issue with a clear title and description
- Include steps to reproduce for bugs
- Suggest use cases for feature requests

### 2. Improve Documentation
- Fix typos or unclear explanations
- Add examples or clarify instructions
- Update documentation for new features
- Improve the knowledge base content

### 3. Enhance Knowledge Base
The knowledge base is critical for plugin functionality:

**Location**: `astro-dev/knowledge-base/`

**Areas to improve**:
- **error-catalog.md** - Add new error patterns and solutions
- **astro-patterns.md** - Document implementation patterns and best practices
- **starlight-guide.md** - Expand Starlight-specific guidance
- **integrations.md** - Add integration examples and patterns
- **content-knowledge/** - Detailed reference materials

**Guidelines**:
- Index errors by symptom (what developers see)
- Provide clear, working examples
- Keep patterns current with latest Astro versions
- Test all code examples before submitting

### 4. Improve Skills and Agents
**Skills** (`astro-dev/skills/`):
- Add new coding patterns to astro-coding
- Enhance API references in astro-knowledge
- Improve selective loading efficiency

**Agents** (`astro-dev/agents/`):
- Refine orchestration logic
- Improve task analysis algorithms
- Enhance validation checks
- Add specialized agents for specific tasks

### 5. Create New Commands
Add new slash commands to `astro-dev/commands/`:
- Follow existing command structure
- Update plugin.json manifest
- Document the command in README files

## Development Guidelines

### Code Quality
- Follow existing code style and patterns
- Test changes thoroughly before submitting
- Ensure all examples are functional
- Keep documentation up to date with code changes

### The 5 Critical Rules
All code examples must follow Astro's critical rules:
1. Include file extensions in imports
2. Use `astro:` module prefix (not `astro/`)
3. Use `class` not `className` in .astro files
4. Async code only in frontmatter, not templates
5. Use `SECRET_*` for server-side, `PUBLIC_*` for client

### Commit Messages
- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused and atomic

### Documentation
- Update all relevant documentation for changes
- Include examples where appropriate
- Keep language clear and concise
- Update version information if needed

## Pull Request Process

1. **Fork and Branch**
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/your-feature`)

2. **Make Changes**
   - Follow the guidelines above
   - Test your changes
   - Update documentation

3. **Submit PR**
   - Push to your fork
   - Open a pull request to main branch
   - Provide clear description of changes
   - Reference related issues

4. **Review Process**
   - Maintainers will review your PR
   - Address any feedback or requested changes
   - Once approved, PR will be merged

## Project Structure

```
sb-marketplace/
├── .claude-plugin/          # Marketplace configuration
│   └── marketplace.json
├── astro-dev/               # Main plugin
│   ├── .claude-plugin/      # Plugin configuration
│   ├── agents/              # Specialized agents
│   ├── commands/            # Slash commands
│   ├── skills/              # Capability providers
│   ├── knowledge-base/      # Reference materials
│   └── hooks/               # Hook configurations
├── README.md                # User documentation
├── CHANGELOG.md             # Version history
└── claude.md                # AI assistant context
```

## Community Standards

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Assume good intentions

### Getting Help
- **Issues**: Technical problems or bugs
- **Discussions**: Questions and ideas
- **Email**: rathermercurial@protonmail.com
- **SuperBenefit**: info@superbenefit.org

## License

By contributing to sb-marketplace, you agree that your contributions will be licensed under the CC0 1.0 Universal (Public Domain Dedication) license.

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for significant contributions
- GitHub contributors page
- Project documentation where appropriate

## Questions?

Don't hesitate to ask questions! Open an issue labeled "question" or reach out via email.

---

**Thank you for contributing to sb-marketplace!**

Your contributions help make Astro/Starlight development better for everyone.
