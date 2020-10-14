import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="okapi-python-connector",
    version="v2020.09.03",
    author="Jonas Radtke",
    author_email="jonas@okapiorbits.space",
    description="Package to connect to OKAPI Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OKAPIOrbits/OkapiPythonConnector",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'time'.
        'json'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
