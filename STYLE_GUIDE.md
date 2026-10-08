# Editorial and Markdown style

## Concept names

Use established spelling and capitalization: Redis, PostgreSQL, GitHub, HTTP, RAG, and MCP. Include long forms or recognized aliases where useful. Keep variants distinct when their guarantees differ, such as sliding-window log and sliding-window counter.

Categories should describe engineering responsibilities rather than individual products. Product-specific concepts belong where their technical behavior is studied. Repeated terms across categories are intentional; repeated terms inside one category are not.

## Markdown

- Use one H1 and a logical heading hierarchy.
- Use sentence case for headings.
- Separate headings, paragraphs, lists, tables, and code fences with blank lines.
- Use relative paths for repository links and descriptive labels for external links.
- Use language identifiers on code fences.
- Keep filenames lowercase with hyphens, except recognized community files such as `README.md`.
- End files with a newline and avoid trailing whitespace.
- Avoid badges without meaningful checks, decorative HTML, inflated expertise claims, and unexplained acronyms when a long form is available.

Generated category pages remain names-only in v0.1.0. Editorial and maintenance documents explain how the repository works; they are not concept tutorials.

## References and freshness

Prefer specifications, official documentation, and original papers. Category reference links are starting points, not a per-term verification claim. Verify version-specific assertions before adding future explanations. Do not put model-version claims into timeless concept names.
