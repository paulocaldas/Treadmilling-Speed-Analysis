import re
from setuptools import setup
 
 
with open("README.md", "rb") as f:
    description = f.read().decode("utf-8")

 
setup(
    name = "analyze_tracks",
    packages = ["analyze_tracks"],
    entry_points = {
        "console_scripts": ['analyze_tracks_cli = analyze_tracks.main_cli:main']
        },
    version = "0.1",
    description = description,
    long_description = description,
    author = "Christoph Sommer",
    author_email = "christoph.sommer@gmail.com",
    )