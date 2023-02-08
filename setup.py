import setuptools

setuptools.setup(
    name='package',
    author='Julia Bartczak',
    package.dir={"":"src"},
    packages=setuptools.find_packages(where="./src"),
    install_requires=["pandas", "regex", "argparse"]
)
