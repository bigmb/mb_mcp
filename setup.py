from setuptools import setup, find_packages
import os

with open("VERSION.txt", "r") as f:
    version = f.read().strip()

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="mb_mcp",
    version=version,
    author="Malav",
    description="Claude MCP (Multimodal Conversational Program) with mb_rag integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bigmb/mb_mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
