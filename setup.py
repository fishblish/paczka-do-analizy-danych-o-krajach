import setuptools

setuptools.setup(
    name='package',
    author='Julia Bartczak',
    packages=setuptools.find_packages(),
    install_requires=["pandas", "regex", "argparse"]
)
