import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# TODO: Extract version number from git tag

setuptools.setup(
    name="vagrancyCtrl",
    version="0.0.1",
    author="Clemens Rabe",
    author_email="clemens.rabe@clemensrabe.de",
    description="Management of vagrant boxes stored in a vagrancy server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seeraven/vagrancyCtrl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
