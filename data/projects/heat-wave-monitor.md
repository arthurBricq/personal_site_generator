---
title: Heat Wave Monitor
keywords: [ Web App, Climate, Data Viz ]
description: A static web app to explore the heat-wave history of any location on Earth, from ~85 years of ERA5 daily temperatures fetched client-side. Detects heat-wave episodes against percentile thresholds of the 1991-2020 climate and renders them as interactive SVG charts.
priority: 98
start_date: 2026-08-24
end_date: 2026-08-24
---

# Heat Wave Monitor

A static website to explore the heat-wave history of any location on Earth,
inspired by ARPAL Liguria's analysis of extreme heat waves.

Pick a city and the app fetches ~85 years of daily temperatures (ERA5
reanalysis via the free Open-Meteo Historical Weather API), detects heat-wave
episodes client-side, and renders them: one bubble per episode (height = peak
intensity, size = severity), a per-year timeline of when in the summer each
episode happened, warming stripes, annual temperature anomaly, and hot days
per year.

Episodes are detected against calendar-day percentile thresholds of the
1991-2020 climate, following ARPAL's regional thermal indicator by default,
with a TX90 model and a fully custom model also available. The view is
mirrored in the URL, so any state is shareable as a link.

Built with Vite + React + TypeScript; charts are hand-rolled SVG. No backend.

Live at [arthurbricq.com/heat-wave-monitor](https://arthurbricq.com/heat-wave-monitor/).
