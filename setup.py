import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rhygen",
    version="0.1.0",
    author="Jakim",
    description="A simple rhythm score generator using abjad package and lilypond",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="GNU General Public License v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.8',
    py_modules=["rhygen"],
    package_dir={'':'quicksample/src'},
)