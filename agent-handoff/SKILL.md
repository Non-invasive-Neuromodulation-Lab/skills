---
name: agent-handoff
description: Hand the current conversation off to a fresh background agent that picks up the work immediately.
---

Write a handoff summary of the current conversation so a fresh agent can continue the work. Deliver the summary to the fresh session as its first message (or save it to a file and point the next session at it) so it can pick up the work immediately.

Include a "suggested skills" section in the summary, naming which skills the next agent should call the use_skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information, since the summary becomes the agent's prompt.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the summary accordingly.
