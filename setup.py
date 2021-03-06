import os
from setuptools import setup, find_packages
from codecs import open


HERE = os.path.abspath(os.path.dirname(__file__))


def read(filename, encoding="utf-8"):
    path = os.path.join(HERE, filename)
    with open(path, encoding=encoding) as f:
        return f.read()


setup(
    name="sql2statsd",
    version="1.2.5",
    author="Suenweek",
    author_email="roman.novatorov@gmail.com",
    description="CLI utility that queries SQL database and posts results to StatsD.",
    license="MIT",
    url="https://github.com/Suenweek/sql2statsd",
    install_requires=[
        "click",
        "psycopg2",
        "PyYAML",
        "statsd"
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    long_description=read("README.md"),
    entry_points={
        "console_scripts": [
            "sql2statsd=sql2statsd.cli:main"
        ]
    }
)
