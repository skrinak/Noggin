# ContextEng

Context engineering templates and configurations for optimizing AI-powered code writing tools.

## Purpose

This repository provides templates and configuration files designed to optimize the experience of context engineering with code writing tools such as **Claude Code** and **Kiro**. These templates help establish clear guidelines, project structure conventions, and best practices for AI assistants working on your codebase.

The most precious resource in any context engineering project is memory. In order to optimize memory usage that speeds code delivery the use of the /clear command is essential. At any moment in your development process, you must be able to type/clear followed by the instruction to read the four following files: README.md, CLAUDE.md, TASKS.md, and .env. By well, maintaining these poor files, it is possible to create superb overall architectures, develop development, guidelines, and themes, and importantly to zero in on specific debugging and narrow product feature requests.

## What's Included

- **CLAUDE.md** - Comprehensive project instructions template for Claude Code
- **claude-template.md** - Starter template for creating project-specific instructions
- **settings.json** - Example configuration settings
- **env.example** - Environment variable template
- **2025-10-14 - UV Setup.md** - UV package manager setup guide

## Getting Started

1. Copy the relevant template files to your project
2. Customize `CLAUDE.md` with your project-specific details
3. Replace placeholder text (YOUR_APP, DATA_SOURCE_1, etc.) with your actual values
4. Configure settings according to your development workflow

## Benefits

- Consistent AI assistant behavior across team members
- Reduced need for repetitive instructions
- Better code quality through enforced standards
- Faster onboarding for AI tools in complex projects
- Clear architectural and development guidelines

## Memory Management Best Practices

### Core Principles

Memory (context window) is the most precious resource in context engineering. Effective memory management can improve AI coding performance by up to 39% according to [Anthropic's research on context management](https://www.anthropic.com/news/context-management).

### Essential Commands for Memory Optimization

**`/clear`** - Use frequently between tasks to reset the context window. This should become muscle memory executed every few minutes during development sessions.

**`/context`** - Inspect token usage and optimize MCP tools and custom agents for peak performance.

**`/compact`** - Summarizes the current coding session to make it more concise (note: can take a minute or more to execute).

**`/resume`** - Jump between previous chats for strategic context switching.

### File-Based Memory System

**Project Memory Files** (CLAUDE.md):
- Should contain project-specific guidelines needed in every coding session
- Keep lean as they consume context window space at the start of each session
- Follow the cascaded system approach recommended in [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)

**Ad-Hoc Documentation** (docs/ folder):
- Place information only needed occasionally in separate documentation files
- Reference using `@docs/filename.md` to save tokens by not loading unnecessary content
- Implement "just in time" context loading for complex data analysis

### Context Engineering Strategies

**Four Pillars of Context Engineering**:
1. **Writing Context** - Create persistent information stores
2. **Selecting Context** - Pull relevant information at the right time
3. **Compressing Context** - Manage token bloat effectively
4. **Isolating Context** - Structure information for effective task performance

**Best Practices**:
- Chop tasks into smaller chunks and use `/clear` after each completion
- Use subagents to verify details or investigate questions early in conversations
- Maintain examples folder with patterns for the AI to follow
- Document context at the end of each working session
- Select only the most relevant code snippets for the AI model
- Preserve project structure and hierarchy when importing code

### Advanced Features (2025)

**Context Editing**: Automatically clears stale tool calls and results when approaching token limits, reducing token consumption by up to 84% in long-running tasks. [Learn more](https://www.anthropic.com/news/context-management)

**Memory Tool**: Enables Claude to store and consult information outside the context window through a file-based system, allowing agents to build knowledge bases over time and maintain project state across sessions.

**Context Awareness**: Claude Sonnet 4.5 and Haiku 4.5 can track their remaining context window ("token budget") throughout conversations, enabling more effective context management.

## Cloud Development & AWS Integration

### AWS AI Coding Tools

**[Amazon Q Developer](https://aws.amazon.com/q/developer/)** - AWS's primary AI coding assistant with industry-leading code acceptance rates (37-60% in production environments). Supports Python, Java, JavaScript, TypeScript, C#, Go, Rust, PHP, Ruby, Kotlin, C, C++, shell scripting, SQL, Scala, JSON, YAML, and HCL.

**[AWS MCP Servers](https://aws.amazon.com/blogs/machine-learning/introducing-aws-mcp-servers-for-code-assistants-part-1/)** - Suite of specialized Model Context Protocol servers that bring AWS best practices directly to your development workflow.

### AWS Best Practices for AI-Assisted Development

- **Infrastructure as Code (IaC)**: Use AI assistants to automate IaC translation, reducing manual effort and minimizing errors. [AWS IaC Translation Guide](https://aws.amazon.com/blogs/compute/infrastructure-as-code-translation-for-serverless-using-ai-code-assistants/)
- **Security First**: Scan code for vulnerabilities, exposed credentials, and log injection with AI-powered security analysis
- **CI/CD Integration**: Auto-generate tests, prevent builds from breaking downstream contracts, and surface failures before production
- **Compliance**: Follow [FedRAMP and DoD CC SRG standards](https://aws.amazon.com/blogs/publicsector/building-an-ai-coding-assistant-on-aws-a-guide-for-federal-agencies/) for federal and highly regulated environments

## Key Resources & Influencers

### Official Documentation

- [Anthropic Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Context Windows Guide](https://docs.claude.com/en/docs/build-with-claude/context-windows)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [AWS Amazon Q Developer](https://aws.amazon.com/q/developer/)

### Community Leaders & Resources

**[Cole Medin](https://github.com/coleam00)** - Context engineering advocate and AI educator
- Creator of ["Context Engineering 101: The Simple Strategy to 100× AI Coding"](https://github.com/coleam00/context-engineering-intro)
- Founder of Dynamous AI community with Context Engineering Hub
- Focuses on Product Requirements Prompts (PRPs) and practical implementation strategies
- [LinkedIn](https://www.linkedin.com/in/cole-medin-727752184/) | [GitHub](https://github.com/coleam00)

### Additional Learning Resources

- [Practical Context Engineering for Vibe Coding](https://abvijaykumar.medium.com/practical-context-engineering-for-vibe-coding-with-claude-code-6aac4ee77f81)
- [Claude Code Memory Management Tips](https://www.geeky-gadgets.com/claude-code-memory-management-tips/)
- [Context Engineering: A Guide With Examples](https://www.datacamp.com/blog/context-engineering) (DataCamp)
- [16x Prompt - AI Coding Context Management](https://prompt.16x.engineer/blog/ai-coding-context-management)
- [Google Cloud: Five Best Practices for AI Coding Assistants](https://cloud.google.com/blog/topics/developers-practitioners/five-best-practices-for-using-ai-coding-assistants)

## Contributing

Feel free to submit issues or pull requests to improve these templates.
