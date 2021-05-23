import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pandas_to_snowflake",
    version="1.0.0",
    description="Bulk loading pandas dataframe to snowflake table",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nit567esh/pandas_to_snowflake",
    author="Nitesh Kumar",
    author_email="nit567esh@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pandas_to_snowflake"],
    include_package_data=True,
    install_requires=["pandas", "snowflake.connector"],
    entry_points={
        "console_scripts": [
            "realpython=pandas_to_snowflake.pandas_to_snowflake:pandas_to_snowflake",
        ]
    },
)