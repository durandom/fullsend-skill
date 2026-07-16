# help

Point users to canonical Fullsend documentation without restating it.

## Usage

```text
/fullsend help [topic]
```

## Procedure

1. Use the orientation report to distinguish a question about this checkout
   from a general Fullsend question.
2. For checkout-specific questions, summarize only locally observed facts and
   link the relevant upstream reference for background.
3. For general questions, choose the narrowest canonical page below.

| Topic | Canonical documentation |
|---|---|
| User workflow, labels, slash commands | [Bugfix workflow](https://github.com/fullsend-ai/fullsend/blob/main/docs/guides/user/bugfix-workflow.md) |
| Running an installed agent locally | [Running agents locally](https://github.com/fullsend-ai/fullsend/blob/main/docs/guides/user/running-agents-locally.md) |
| Agent catalog and behavior | [Agent documentation](https://github.com/fullsend-ai/fullsend/tree/main/docs/agents) |
| Getting started or installation | [Getting started](https://github.com/fullsend-ai/fullsend/tree/main/docs/guides/getting-started) |
| Administration and configuration | [Guide index](https://github.com/fullsend-ai/fullsend/tree/main/docs/guides) |

Do not copy guide sections into the response. Give a short answer based on the
installation when possible, then link the canonical page for the full procedure.

## Report

Include:

- the answer specific to the current checkout, if observable;
- the canonical link;
- any uncertainty caused by an unreadable remote configuration source.
