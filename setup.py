import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whitehole", 
    version="0.0.2",
    author="QuantMoon Technologies",
    author_email="contacto@quantmoon.com",
    description="Package for read and backtest data of financial assets in the most storage-efficient way, taking care of performance and store using zarr format files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantmoon/whitehole",
    include_package_data = True,
    packages=setuptools.find_packages(),
    install_requires=["pandas>=0.22.0",
                      "numpy>=1.18.2",
                      "zarr",
                      "xarray>=0.13.0",
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.5',
)