# System Design Write-Up Brief (shared by all writer agents)

You are writing ONE markdown file per system design question into
`/Users/shahdevs/.kiro/crew/workspace/system-design-pdf/questions/NN-slug.md`
(NN = two-digit order given in your task). Nothing else. Do not touch other files.

## Audience and tone

- A mid-level engineer preparing for a system design interview.
- VERY easy to understand. Short sentences. Plain words. Explain every term the first time it appears.
- Prefer concrete numbers over hand-waving. Show the arithmetic.
- Use code snippets (Python, SQL, JSON, pseudo-config) wherever a snippet makes an idea clearer. Fence them with a language tag.
- Use ASCII diagrams in fenced ```text blocks for architecture. Keep them under 80 columns.
- Use markdown tables for comparisons (option A vs B, trade-offs).
- Target length: Easy 1800-2500 words, Medium 2500-3500 words, Hard 3500-4500 words.

## Research (required)

Use web search on the question first. Good sources: hellointerview.com (the question list comes from there), highscalability, engineering blogs of the real company, AWS/GCP architecture docs, systemdesign primers on GitHub. Paraphrase; never copy more than a sentence. Put a `## Sources` section at the end with 3-8 links as `- [title](url)`.

## MANDATORY structure (use these exact H2 headings, in this order)

```
# NN. <Question name>  (<Easy|Medium|Hard>)

> One-paragraph plain-English description of what the product does and what the interviewer is really testing.

## 1. Functional requirements
Numbered list. Core (must have) first, then "Below the line" (out of scope, say why).

## 2. Non-functional requirements
Numbered list. Each one must be SPECIFIC and QUANTIFIED where possible
(e.g. "p99 redirect latency < 200 ms", "99.99% availability for reads",
"consistency: eventual for X, strong for Y"). Call out the CAP choice and why.

## 3. Back-of-the-envelope estimates
Table: assumption -> number. Then derive QPS (read and write), storage per year,
bandwidth. Show the math as a code block.

## 4. Core entities
Bulleted list of the 4-8 nouns, each with one line of what it is and its key fields.
Then a small schema snippet (SQL or JSON) for the 2-3 most important ones.

## 5. API design
Each endpoint as:
  `METHOD /path` -- one-line purpose
  request body / params (JSON), response (JSON), status codes, auth note.
Cover every core functional requirement with at least one endpoint.

## 6. High-level design
ASCII diagram of the whole system. Then walk through each core functional
requirement end to end as a numbered "request flow" (client -> ... -> response).
This is where you answer the "How will users do X?" questions one at a time,
each under an H3 like `### How will users shorten a URL?`

## 7. Deep dives
One H3 per hard problem, phrased as the interviewer would ask it, e.g.
`### How can we ensure redirects are fast?`
`### How does the system scale to 10k reads/sec?`
For each: the problem, 2-3 options in a comparison table, the recommended
option, and a code snippet or diagram that shows the mechanism. Aim for 4-6 deep dives
(Easy: 3-4, Medium: 4-5, Hard: 5-6). Always include at least one on scaling,
one on the key consistency/correctness problem, and one on failure handling.

## 8. Final architecture
Updated ASCII diagram including everything from the deep dives, plus a
"component -> job -> technology example" table.

## 9. Common mistakes and interviewer follow-ups
Bulleted. 5-8 items. Each: the mistake, why it hurts, what to say instead.

## 10. One-page cheat sheet
A compact table or list a reader can review in 60 seconds before the interview:
key numbers, key decisions, key technologies.

## Sources
```

## Formatting rules

- H1 only once (the title). H2 for the 10 sections + Sources. H3 inside.
- No HTML. No emoji. No em dashes (use commas or a plain hyphen).
- Tables must have a header row and `|---|` separator.
- Code fences always get a language: ```python ```sql ```json ```text ```yaml ```bash
- Keep ASCII diagrams <= 80 columns wide so they fit a PDF page.
- Do not write "as an AI" or refer to this brief. Write as the author of a study guide.

## Done condition

The file exists at the exact path, passes a quick self-check (all 11 H2 headings present, in order,
at least 3 code fences, at least 2 tables, Sources section with >= 3 links), and you report
the path plus word count in one line.
