from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nuc_led",
    description="A python API for control of the front LEDs of Intel NUC7i[x]BN and NUC6CAY NUCs.",
    version="0.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TomAFrench/intel_nuc_led_python_api",
    author="Tom French",
    author_email="tom@tomfren.ch",
    license="Apache 2",
    packages=["nuc_led"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
)
