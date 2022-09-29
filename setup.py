from distutils.core import setup

# get long description for display within PyPi
with open("README.md", "r") as fh:
    long_description = fh.read()

# do the settings for PyPi
setup(
    name='freeplane-io',
    version='0.5.2',
    py_modules=['freeplane'],
    author='nnako',
    author_email='nnako@web.de',
    url="https://github.com/nnako/freeplane-python-io",
    description='provide create, read, update and delete of freeplane nodes via file access',
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "html2text ~= 2020.1.16",
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        ]
)
