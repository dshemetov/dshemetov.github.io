---
# Generated from the Obsidian vault by scripts/vault_export.py. Edit the note there.
title: Rust and MistQL
date: 2025-10-17T20:57:50-07:00
tags: []
draft: false
slug: mistql
---

I made a [Rust port of MistQL](https://github.com/evinism/mistql/pull/194), a query language for JSON-like data structures. I learned a lot about what goes into a program that runs a language: lexers, parsers, grammars, runtimes, and general language design. This was also my first serious project with Rust. I made a [follow-up improvement](https://github.com/evinism/mistql/pull/212) that focused on memory management, which taught me a lot about Rust lifetimes, and, in particular, it taught me that JSON-like structures are very tough to represent in Rust. I'm not sure if I will get the motivation to write an in-depth post.
