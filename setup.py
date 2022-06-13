from setuptools import find_packages, setup

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstream-dao",
    version="0.0.5",
    packages=find_packages(),
    install_requires=["eth-brownie", "tqdm"],
    extras_require={
        "dev": [
            "black",
            "moonworm >= 0.1.9",
        ],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    description="Command line interface to the Moonstream DAO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Moonstream",
    author_email="engineering@moonstream.to",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    url="https://github.com/bugout-dev/dao",
    entry_points={
        "console_scripts": [
            "dao=dao.cli:main",
        ]
    },
    include_package_data=True,
)
