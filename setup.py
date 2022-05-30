import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="APU",
    version="1.0.0",
    author="Thomas QUEMARD (RCD)",
    author_email="thomas.t.quemard.external@airbus.com",
    description="Airbus Python Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gheprivate.intra.corp/QDNP/apu",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
    ),
)