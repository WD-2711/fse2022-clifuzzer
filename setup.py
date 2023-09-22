import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CLIFuzzer",
    version="0.0.1",
    author="Abhilash Gupta",
    author_email="abhilash0272@gmail.com",
    description="Tool to generate invocation grammars of CLI utilities and then grammar fuzz them.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clifuzzer/fse2022-clifuzzer",
    install_requires=[
        'fuzzingbook',
        'markdown',
        'graphviz'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Testing"
    ],
    python_requires='>=3.6',
    # 在 src 目录下查找所有的 python 包，并返回给 packages
    package_dir={'':'src'},
    packages=setuptools.find_packages()
)