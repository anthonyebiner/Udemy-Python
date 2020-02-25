import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="udemy-python",
    version="0.0.1",
    author="Anthony Ebiner",
    author_email="anthonyebiner@gmail.com",
    description="A python wrapper for the Udemy Instructor API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthonyebiner/Python-Udemy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
