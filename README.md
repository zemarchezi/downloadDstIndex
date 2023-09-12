# Disturbance Storm-Time index Downloader

Download one year of Data from Kyoto repository and store in a DataFrame Format.

## Requirements

Python 3.8+
### Installation: 

```
conda create -n yourenvname python=x.x anaconda
conda activate yourenvname

pip install dstdownloader
```


## Simple use

```python
from dstdownloader.downloadDst import downloadDst

dst = downloadDst(2020)
```

