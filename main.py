#!/usr/bin/env python3
"""Copy the front-page image to the output directory.

The image (entry.png) is drawn by draw.py in this repository — a single
newspaper front page for Tuesday 24 November 2026: Nvidia's +31% surge as
Jensen Huang returns as CEO, US sanctions on Iran's shadow banking, the war
spilling into the Baltic, COP31 collapsing in Antalya, and the Banten factory
fire. This program only copies that image, using the standard library, so it
runs with no network and writes identical bytes on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT, "entry.png")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)
assert os.path.getsize(DST) > 0, "copied image is empty"
