"""Package configuration."""
from setuptools import setup

setup(
    name="vinyl_scraper",
    version="0.1",
    packages=["vinyl_scraper"],
    package_dir={"": "src"},
    install_requires=["pytest==7.1.3", "black==22.10.0", "beautifulsoup4", "requests"],
)
