from setuptools import setup, find_packages

setup(
    name="infinite_games",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "aiohttp",
        "bittensor",
    ],
) 