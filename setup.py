import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylgrum", # Replace with your own username
    version="0.0.1",
    author="Joshua R. Heling",
    author_email="jrh-pypi@netfluvia.org",
    description="A library for modeling and playing the card game Gin Rummy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrheling/pylgrum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment"
    ],
    python_requires='>=3.6',
)