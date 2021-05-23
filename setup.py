from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pandas_to_snowflake',
    version='2.0.1',
    author="Nitesh Kumar",
    author_email="nit567esh@gmail.com",
    description="Bulk loading pandas dataframe to snowflake table",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nit567esh/pandas_to_snowflake",
    packages=['pandas_to_snowflake'],
    install_requires=["pandas"]
)