# Contributing

## Development workflow

Changes must not be committed directly to `main`.

Use the following workflow for every change, including small documentation updates:

1. Create a focused branch from the current `main` branch.
2. Make the intended changes on that branch.
3. Validate the affected ontology, SHACL, examples, documentation, or tooling.
4. Commit the changes with a concise and descriptive commit message.
5. Open a pull request targeting `main`.
6. Merge the pull request automatically after the applicable checks have passed.

Squash merging is preferred so that each pull request results in one coherent commit on `main`.

The `main` branch should remain usable and represent the current accepted state of the project.

Post-merge review may be used when explicitly agreed, but the branch and pull-request workflow still applies.

## Documentation convention

SMO adopts the shared [Semantic Knowledge Engineering Semantic Markdown convention](https://github.com/GerhardBalz/semantic-knowledge-engineering/blob/main/conventions/semantic-markdown.md):

- use ordered Markdown lists when order or procedure is part of the meaning;
- use unordered Markdown lists for non-sequential collections;
- reserve fenced blocks for code, commands, literal syntax, identifiers, diagrams, aligned specimens, or output where preformatted layout carries meaning.

Do not mechanically convert semantic identifier blocks, repository trees, command examples, or other literal/preformatted specimens into lists merely because they contain multiple lines.

This convention was promoted to SKE after review feedback from @TallTed on `perma-id/w3id.org#6530`; ESKA #72 was the first cross-repository adoption case.

## Branch naming

Use short, descriptive branch names, for example:

```text
feature/add-model-versioning
docs/clarify-capability-terminology
fix/projection-shape
```

Automation-created branches may use:

```text
agent/<change-description>
```

## Pull requests

A pull request should explain:

- what changed;
- why the change is needed;
- which files or concepts are affected;
- how the change was validated.

Small changes may be merged automatically after validation when post-merge review has been agreed.
