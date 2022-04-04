import os
from setuptools import setup, find_packages

_dir = os.path.abspath(os.path.dirname(__file__))
_readme_path = os.path.join(_dir, "README.md")

with open(_readme_path, "r") as rm:
    README = rm.read()

setup(
    name="pypocket",
    version="0.1",
    description="Python Client SDK for Pocket Network.",
    author="blockjoe",
    author_email="joe@pokt.network",
    license="MIT",
    packages=find_packages(),
    url="https://github.com/pokt-foundation/pypocket",
    keywords="pocket network sdk rpc",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests>=2.27.1",
        "pydantic>=1.9.0",
        "PyNaCl>=1.5.0",
        "pycryptodome>=3.14.1",
        "tabulate>=0.8.9",
    ],
    extras_require={"async": ["aiohttp[speedups]>=3.8.1"]},
    tests_require=["pytest", "python-dotenv"],
    setup_requires=["black", "sphinx"],
)
