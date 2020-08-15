import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whitehole", 
    version="0.0.6",
    author="QuantMoon Technologies",
    author_email="contacto@quantmoon.com",
    description="Package for read and backtest data of financial assets in the most storage-efficient way, taking care of performance and store using zarr format files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantmoon/whitehole",
    packages=setuptools.find_packages(),
    install_requires=['pandas','numpy','csv','re','xarray','datetime','dateutil'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.5',
)