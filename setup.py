import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Spending-tracker-OTA",
    version="0.0.1",
    author="Markus",
    author_email="ruutmies@gitmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruutimies/programmable-web-2019",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
