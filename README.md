![logo_website](https://user-images.githubusercontent.com/49825286/90585259-06971800-e19a-11ea-88e2-c4866aa8caaf.png)
<br />
Whitehole is a zarr-format-based-tool that allows individuals or small teams interested in processing financial information to make investment decisions.


## What do I need to know to start?
<br />

Whitehole was thought to fill the gap between the techniques used by the industry and some retail quantitative investors. Thus, the first step to think about is that there is a huge amount of data that is necessary to process for different purposes, specially for **ticks** market data instead of **candlebars**. That's why we need a format to store all the data in less storage space. In that sense, [Quantmoon Technologies](https://www.quantmoon.com/) provides [tick data using Zarr format](https://www.quantmoon.com/tickdata). [Zarr](https://github.com/zarr-developers/zarr-python) allows to chunk this tick data and store it in binary structure with metadata as labels.

Whithole use this light data files to upload and read it in Python environments, such as Jupyter, Spyder, PyCharm and more. The idea behind this is to get useful data arrays to work efficiently through any required process. So, [xarray](https://github.com/pydata/xarray) is the main library useful for hold the data and work with it. 

As an additional features, Whitehole allows to use [numpy](https://github.com/numpy/numpy/blob/master/README.md) and [pandas](https://github.com/pandas-dev/pandas) to work with the data for different purposes, specially when the processing has to be done just once in the workflow.

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
