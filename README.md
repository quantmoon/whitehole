# WHITEHOLE: 
![alt text](http://url/to/img.png)

<br />
Whitehole is a zarr-format-based-tool that allows individuals or small teams interested in processing financial information to make investment decisions.


## What do I need to start?
<br />

As Whitehole was thought in a way of lowering some enter barriers to the finacial world, the first step to think about is the huge amount of data that is necessary to process for some purposes, specially if is required to use some features as **ticks** instead of **candlebars**. That's why we need a format to store all the data in less storage space. To accomplish that, Whitehole use the [zarr format](https://github.com/zarr-developers/zarr-python) to store the data in binary with metadata understand it. 

Also is necesarry a parallel procesing of this format to focus not only solve the problem of storage, but also improve the performance of the process. That's why we need to use the [xarray](https://github.com/pydata/xarray)

For general purposes, we use [numpy](https://github.com/numpy/numpy/blob/master/README.md) and [pandas](https://github.com/pandas-dev/pandas) to work with the data specially when the processing has to be done just once in the workflow.

Whitehole is fully developed in Windows.


## Features:
<br />

* Decryptor: because of zarr store data in binary, with this class is possible to transform it in a more human-comprenhensive way.
* Whitehole is thought to have different features, the processing of the information will be realized in future versions.

## How do I get it?
<br />

Whitehole can be installed from PyPI using pip:
```
pip install whitehole
```


## Quick Start
<br />

To have a better understanding of the features, please check the notebooks on the 'notebook' folder
