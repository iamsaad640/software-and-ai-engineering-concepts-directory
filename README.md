# Software & AI Engineering Concepts

Find the concepts behind reliable software and LLM applications.

Browse **45 categories** covering databases, distributed systems, architecture, prompts, RAG, agent loops, and technical leadership. Use the directory to spot gaps in your knowledge, prepare for interviews, or plan what to study next.

**[Browse the directory](docs/README.md)** · **[Find a term A–Z](docs/glossary.md)**

## Pick a starting point

| What you’re working on | Start here |
| --- | --- |
| APIs under heavy traffic | [Rate limiting](docs/software/rate-limiting.md), [caching](docs/software/caching.md), [performance](docs/software/performance.md) |
| Data that stays correct | [Transactions](docs/software/transactions.md), [distributed systems](docs/software/distributed-systems.md), [Redis and distributed KV stores](docs/software/distributed-key-value-stores.md) |
| LLMs that use your knowledge base | [Knowledge bases](docs/ai/knowledge-bases.md), [retrieval and RAG](docs/ai/rag-and-retrieval.md), [context engineering](docs/ai/context-engineering.md) |
| Agents that take actions | [Tools and MCP](docs/ai/tools-and-mcp.md), [agent loops](docs/ai/loop-engineering.md), [action safety](docs/ai/action-safety.md) |
| AI applications in production | [Evaluation](docs/ai/evaluation.md), [observability](docs/ai/observability.md), [security](docs/ai/security.md) |
| Architecture and team decisions | [Technical strategy](docs/principal/technical-strategy.md), [organizational engineering](docs/principal/organizational-engineering.md) |

## What’s inside

- **Software engineering:** fundamentals, system design, storage, networking, security, testing, and operations.
- **LLM applications:** prompts, context, retrieval, tools, memory, orchestration, and evaluations.
- **Architecture and technical leadership:** tradeoffs, ownership, migrations, and engineering strategy.

The directory currently lists concept names, with reference links for each category. Choose a topic relevant to your work and use its terms as a study checklist. The AI section focuses on building applications with LLMs.

## Suggest a missing concept

Found a gap or a confusing name? [Open an issue](https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory/issues/new/choose) or [send a pull request](CONTRIBUTING.md).

## Run the searchable docs locally

Requires Python 3.11 or newer, with no extra packages.

```bash
python3 scripts/build.py --site
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000` to search concepts and filter by topic. See [the contribution guide](CONTRIBUTING.md) for validation commands and [the maintenance guide](docs/maintaining.md) for publishing.

[Changelog](CHANGELOG.md) · [Releases](https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory/releases) · [MIT license](LICENSE)
