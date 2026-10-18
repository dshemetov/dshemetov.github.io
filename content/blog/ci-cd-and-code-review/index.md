---
# Generated from the Obsidian vault by scripts/vault_export.py. Edit the note there.
title: CI/CD and Code Review
date: 2026-10-18T14:00:00-07:00
tags:
  - software
draft: false
slug: ci-cd
---

> Now, review runs continuously, more like spellcheck while you write. Most changes have been reviewed and fixed by Claude at least once before a human is asked to look. This catches most routine mistakes, and saves team attention for higher-level questions and scrutiny.
> - [Anthropic's recent post on code review](https://claude.dev/blog/solving-code-review-at-anthropic)

As we move through big shifts in software dev practices, it's grounding to get historical context and realize that much of what we do is more recent than we thought. In the 90s/00s, it wasn't that uncommon for small teams to just push to trunk directly (as long as the build/test times were fast):

> Some teams will choose to commit/push straight to the trunk. Most likely it is because they are a small team with each team member knowing what the others are up to. Their build is probably fast and relatively exhaustive, and they may well seldom experience a build breakage. If the build does break (post integration into trunk/main) then they most likely ‘revert’ the commit straight away, possibly locking the trunk for a short period of time while that is performed. If the team is really small (say three or four), in which case the team might allow someone to fix the build quickly and commit that in order to get the build green again.
> - [trunk-based development](https://trunkbaseddevelopment.com/committing-straight-to-the-trunk/)

[Steve Yegge's experiments](https://yegge.ai/essays/the-shape-of-things-to-come/) with running an MMO come to mind - it's not only a question of whether human review can keep up, but can your CI/CD keep up? Github is certainly feeling the strain of having to run CI/CD on every change. If the pace of change keeps increasing, I can see CI/CD running in a `git bisect`-like mode, only in response to a suspected problem, rather than on every commit.
