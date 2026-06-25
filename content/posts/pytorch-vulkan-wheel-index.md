---
title: "PyTorch Vulkan wheel index"
description: "PEP 503 static wheel index served from GitHub Pages."
tags: ["python", "pytorch", "vulkan", "wheels"]
---

Wheel index URL:

```text
https://parksnoopyinc.github.io/index/whl/vulkan/
```

Use as primary index:

```text
--index-url https://parksnoopyinc.github.io/index/whl/vulkan/
torch
```

Or in `pyproject.toml` with installer-specific config that supports custom indexes.

This path is a static PEP 503 simple repository under `static/index/whl/vulkan/`. Hugo still owns normal pages like `/` and article slugs; only `/index/whl/vulkan/` is reserved for wheels.

Add wheel files under `static/index/whl/vulkan/_wheels/`, then run:

```sh
python3 scripts/build-wheel-index.py
```

The script writes normalized project pages such as `/index/whl/vulkan/torch/` and root project links at `/index/whl/vulkan/`.
