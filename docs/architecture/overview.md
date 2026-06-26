# Architecture générale

```mermaid
graph TD
    Book[book/] --> Notebooks[notebooks/]
    Book --> Docs[docs/]
    MiniFramework[mini_framework/] --> Examples[examples/]
    Platform[ai_platform/] --> Examples
    Tests[tests/] --> MiniFramework
    Tests --> Platform
```
