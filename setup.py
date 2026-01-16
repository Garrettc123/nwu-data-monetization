"""Setup configuration for NWU Data Monetization Engine."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nwu-data-monetization",
    version="0.1.0",
    author="AUTOHELIX Quantum Systems",
    author_email="contact@autohelix.ai",
    description="Transform data into revenue with liquidity bonds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Garrettc123/nwu-data-monetization",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dateutil>=2.8.2",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "sqlalchemy>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
        ],
    },
)
