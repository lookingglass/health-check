#!/usr/bin/env python3
# Docker-like naming system
import random

left=["deep", "silent", "huge", "distant", "frozen", "snowy", "vibrant", "beautiful", "awesome"]
right=["peak", "forest", "hill", "river", "ocean", "desert", "taiga"]


l=random.choice(left)
r=random.choice(right)

print(f"{l}_{r}")