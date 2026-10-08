# Software & AI Engineering Concepts Directory

A directory of advanced software and applied LLM engineering concepts for senior and principal engineers.

**Start here:** [Browse categories](docs/README.md) · [Alphabetical index](docs/glossary.md) · [Contribute](CONTRIBUTING.md)

## Scope

- **Software engineering:** algorithms, runtimes, concurrency, architecture, APIs, databases, distributed systems, Redis, security, delivery, and operations.
- **Applied LLM engineering:** prompts, context, knowledge bases, RAG, tools, MCP, agent loops, orchestration, memory, evaluations, and production applications.
- **Principal engineering:** technical strategy, organizational engineering, and applied AI judgment.

The first release lists concept names. It does not include concept explanations, tutorials, classical machine learning, or model training. Inclusion is a study prompt, not a claim that every role requires every specialization. Emerging umbrella terms such as “loop engineering” are distinguished from established mechanisms.

## Browse

| Track | Directory |
| --- | --- |
| Software engineering | [Software categories](docs/README.md#software-engineering) |
| Applied LLM engineering | [LLM application categories](docs/README.md#applied-llm-engineering) |
| Principal engineering | [Strategy and leadership](docs/README.md#principal-engineering) |
| All concepts | [Alphabetical index](docs/glossary.md) |

The static documentation includes text search, track filtering, category navigation, and a downloadable catalog. Its intended GitHub Pages address is `https://iamsaad640.github.io/software-and-ai-engineering-concepts-directory/`; publication depends on Pages being enabled for the repository.

## Maintain the directory

`catalog/directory.json` is the source of truth. Markdown and static documentation are generated from the same catalog.

```bash
python3 scripts/build.py --site
python3 scripts/check.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. Python 3.11 or newer is sufficient; the build has no third-party dependencies.

Do not edit generated category pages or the alphabetical index directly. See [contribution guidance](CONTRIBUTING.md), [editorial style](STYLE_GUIDE.md), and [repository lifecycle](docs/maintaining.md).

## Releases

[Changelog](CHANGELOG.md) · [Release history](https://github.com/iamsaad640/software-and-ai-engineering-concepts-directory/releases)

The release workflow uses `VERSION`, creates an annotated `vMAJOR.MINOR.PATCH` tag, and publishes the catalog and static site archive. Existing tags are never moved. The Pages workflow publishes validated content from `main` independently of release creation.

## License

[MIT](LICENSE). Third-party reference resources retain their own licenses.
