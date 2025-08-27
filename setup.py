from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mortgage-rate-agent",
    version="1.0.0",
    author="Claude Code Assistant",
    author_email="developer@example.com",
    description="AI-powered social media content generator for mortgage loan officers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mortgage-rate-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mortgage-agent=src.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.yaml", "data/*.json"],
    },
)