---
title: Chess Engine in Rust
keywords: [Chess, Rust]
description: A fully functional Chess Engine written completely from scratch in Rust
priority: 1
featuredImage: images/chess_engine.png
github: https://github.com/arthurBricq/chess_rust
start_date: 2023-04-02
end_date: 2025-08-09
---

# Chess Engine in Rust

I wanted to learn Rust, and I had loved to write my first chess engine (in C++). So this is my attempt to do it in Rust. It was surprisingly easier than C++.

With this engine, I choose a memory efficient representation of a chess-board: 7 integers are sufficient to represent a full chess position (including the special rules for castling and for en-passant). Using such a low-memory approach, it's extremely cheap to perform deep copies of chess games and therefore have a simple chess solver.
