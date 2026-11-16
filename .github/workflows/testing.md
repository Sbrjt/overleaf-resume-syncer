# Testing Locally

## Requirements

- [GitHub Local Actions](https://marketplace.visualstudio.com/items?itemName=SanjulaGanepola.github-local-actions)
- [nektos/act](https://github.com/nektos/act)
- Docker

Use Medium size image when prompted: `catthehacker/ubuntu:act-latest` (~500MB)
It's a minimal Ubuntu image, Chrome needs system libraries to run, so run `apt-get install google-chrome-stable` in order to use Selenium.

## Command

```bash
act \
  -W .github/workflows/test.yml \
  --reuse \
  --local-repository "Sbrjt/overleaf-resume-syncer@main=." \
  --var "OVERLEAF_URL=https://www.overleaf.com/read/nsgsskwncdmy#a859ac"
```

Comment out the commit step from `action.yml` while testing.

### What Each Flag Does

| Flag                    | What it does                                                            |
| ----------------------- | ----------------------------------------------------------------------- |
| `--reuse`               | Don't destroy the Docker container between runs                         |
| `--local-repository`    | Maps the GitHub action reference to its local implementation in the cwd |
| `--bind`                | Mounts the container to cwd using a bind mount                          |
| `--action-offline-mode` | Reuse cached actions like `actions/checkout`, `actions/setup-python`    |
