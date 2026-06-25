# ParkSnoopy Blog

Hugo + Blowfish GitHub Pages site.

## Wheel Index

PEP 503 index: `https://parksnoopyinc.github.io/index/whl/vulkan/`

Add wheels to `static/index/whl/vulkan/_wheels/`, then rebuild:

```sh
uv run --script scripts/build-wheel-index.py
```

GitHub Actions builds the wheel index with `uv`, builds Hugo, then deploys Pages.
