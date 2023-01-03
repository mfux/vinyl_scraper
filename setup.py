"""Package configuration."""
from setuptools import setup

setup(
    name="vinyl_scraper",
    description="convert music blog into local music collection",
    url="https://github.com/mfux/vinyl_scraper",
    author="mfpypi",
    author_email="mfpypi@elektronmail.de",
    license="MIT",
    version="0.1",
    zip_safe=False,
    packages=["vinyl_scraper"],
    package_dir={"": "src"},
    install_requires=[
        "pytest==7.1.3",
        "black==22.10.0",
        "beautifulsoup4",
        "requests",
        "youtube_dl",
        "eyed3",
        "lxml",
    ],
    entry_points={
        "console_scripts": ["vinyl-scrap=vinyl_scraper.app:main"],
    },
)
