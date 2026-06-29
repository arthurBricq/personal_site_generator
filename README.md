# Personal Site Generator

A minimal personal webpage creator that you can fully customize, written in python.

I use this code to generate my personal website, [arthurbricq.com](https://arthurbricq.com).

## Repos

This repo is the **source of truth**: the generator code and the `data/` it consumes.

The generated site is hosted in a separate repo,
[`personal-site`](https://github.com/arthurBricq/personal-site), which is served
by GitHub Pages. That repo holds **only build output** — never edit it by hand.

## To build and deploy

```console
# 1. Generate the site (writes into ./outsite, which is gitignored here)
python3 generate_site.py

# 2. Copy the build into the hosting repo and push it
cp -R outsite/. ../arthurbricq/
cd ../arthurbricq
git add -A
git commit -m "rebuild site"
git push
```

GitHub Pages on the `personal-site` repo then serves the new content at
arthurbricq.com (the `CNAME` file lives in `outsite/` and is copied along with
the rest).
