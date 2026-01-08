from setuptools import setup, find_packages

setup(
    name="dfe-nfse",
    version="0.1.0",
    description="Biblioteca para baixar NFSe do Ambiente Nacional (ADN)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="David Silva",
    author_email="david.emery.silva@gmail.com",
    url="https://github.com/DaavidSiilva/dfe-nfse",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "cryptography",
    ],
)
