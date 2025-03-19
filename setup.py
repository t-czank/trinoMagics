from setuptools import setup, find_packages

setup(
    name="trinoMagics",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "IPython>=7.0",
        "trino>=0.331.0",
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [],
    },
)
