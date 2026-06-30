---
title: CPU GameEngine written from scratch (in Rust)
keywords: [Computer Graphics, Rust, Vision, Game Engine]
description: I wanted to see how difficult it would be to write an CPU equivalent of OpenGL. So here it is ! A 3D world renderer written from scratch in Rust, without any vision library such as OpenGL or Vulkan. To be able to render thousands of polygons efficiently on the CPU, I implemented binary space partitioning.
priority: 80
featuredImage: images/engine.png
github: https://github.com/arthurBricq/GameEngine
start_date: 2024-02-19
end_date: 2024-02-19
---

# Custom Game Engine framework

I the quest for a new project, I have decided to program a Doom game. When I explored the several options in Rust to write OpenGL or Vulkan bindings, I was slightly disappointed. I though it would a great idea to try and **write a custom game engine**. Since it is quite a challenging piece of work, I limited myself to a **CPU engine** (no hardware acceleration).

- Display any number of 3D polygons on a 2D buffer of pixels
- Each polygon can be associated a texture
- Pixel color is determined using the closest's polygon texture
- Binary space partitioning is implemented to determine which polygon it is.
