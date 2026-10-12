# VanDrishti documentation

Use this page as the starting point for the M4 Intelligence module.

| Document | Read this when you need to understand |
| --- | --- |
| [M4 module map](m4-module-map.md) | The purpose of each M4 folder, file, test, and execution step. |
| [M4 integration guide](m4-integration.md) | The M1 -> M4 -> M5 API flow, JSON contracts, and module boundaries. |
| [Contribution guide](../CONTRIBUTING.md) | Branch names, pull requests, checks, and merge rules. |

## Quick navigation

```text
M1 evidence payload
        |
        v
M4 API -> Fact Packet -> Report Generator -> Numeric Guard -> XAI -> Review Queue
        |
        v
M5 dashboard
```

The authoritative shared data formats are in `../contracts/`. Do not change a contract without coordinating with the module that produces or consumes it.
