# Personal Site Generator

A minimal personal webpage creator that you can fully customize, written in python.

I use this code to generate my personal website, [arthurbricq.com](https://arthurbricq.com).

## Layout

- `generator/` — the engine (library code), with no personal data.
- `generate_site.py` — thin CLI that wires the engine to your inputs.
- `data/` — content source of truth (markdown, images, resume).
- `templates/` — HTML/CSS presentation.

The generated site is hosted in a separate repo,
[`personal-site`](https://github.com/arthurBricq/personal-site), which is served
by GitHub Pages. That repo holds **only build output** — never edit it by hand.

## Setup

```console
pip install -r requirements.txt
```

## Usage

```console
python3 generate_site.py [--data ./data] [--templates ./templates] [--output ./outsite] [--name "Arthur Bricq"]
```

The build is **clean**: the output directory is wiped first (so deleted pages or
images never linger), while `.git` and `CNAME` are preserved.

### Local preview

```console
python3 generate_site.py        # builds into ./outsite (gitignored)
```

### Deploy

Build straight into the hosting repo and push — no copy step:

```console
python3 generate_site.py --output ../arthurbricq
cd ../arthurbricq
git add -A
git commit -m "rebuild site"
git push
```

`CNAME` is a deploy artifact of the hosting repo: it stays there and is left
untouched by the build.
