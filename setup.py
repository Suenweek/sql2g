import os
from setuptools import setup
from codecs import open


HERE = os.path.abspath(os.path.dirname(__file__))


def read(filename, encoding="utf-8"):
    path = os.path.join(HERE, filename)
    with open(path, encoding=encoding) as f:
        return f.read()


setup(
    name="sql2g",
    version="0.0.1",
    author="Suenweek",
    author_email="suenweek@protonmail.com",
    description="CLI utility that queries SQL database and posts results to "
                "Graphite via StatsD.",
    license="MIT",
    url="https://github.com/Suenweek/sql2g",
    install_requires=[
        "click",
        "psycopg2",
        "PyYAML",
        "statsd"
    ],
    package_dir={"": "src"},
    py_modules=["sql2g"],
    long_description=read("README.md"),
    entry_points={
        "console_scripts": [
            "sql2g=sql2g:main"
        ]
    }
)
