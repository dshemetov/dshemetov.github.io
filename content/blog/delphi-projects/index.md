---
# Generated from the Obsidian vault by scripts/vault_export.py. Edit the note there.
date: 2023-11-13T22:51:13-07:00
slug: delphi-projects
aliases:
  - /delphi-projects/
title: Recent Delphi Projects
---
> Test quote block.
> - Source Name, "Here".

A large portion of my work at Delphi has involved producing R packages for epidemiological data processing and forecasting. This includes:

- [epidatr](https://github.com/cmu-delphi/epidatr/) - a package for downloading and processing epidemiological data.
- [epiprocess](https://github.com/cmu-delphi/epiprocess/) - a package for processing epidemiological data.
- [epipredict](https://github.com/cmu-delphi/epipredict/) - a package for building forecasting models on epidata.

I used these to build data pipelines (in Python and in R) that flowed into forecasting models. I worked with a research team to design and implement our forecasting models. We read through [Forecasting: Principles and Practice](https://otexts.com/fpp3/) and [Advanced R](https://adv-r.hadley.nz/) recently, as a reading group.

I have also built web apps with Django and FastAPI to [Epidata API - Swagger UI](https://delphi.cmu.edu/epidata/v5/docs). I have peered into the depths of data engineering to serve a 2TB versioned dataset in Postgres (and scoped potential migration to a datalake using DuckDB). Might do some technical writeups on this soon.
