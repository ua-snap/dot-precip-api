# GCM Generated Precipitation Data API

## Purpose

This provides the ability for a Flask API to request data from all NetCDF files located in a particular directory given an X-coordinate and a Y-coordinate in the [EPSG:3338](https://epsg.io/3338) projection coordinates. This returned data is in a [Pickle](http://xarray.pydata.org/en/stable/io.html#:~:text=open_dataset(store)-,Pickle,%5B22%5D%3A%20pkl%20%3D%20pickle.) formatted [xarray.DataArray](http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html) which can be un-Pickled on the client side for access to collected data in a usable format.

## Structure

* `api.py` contains the main Flask API app.
* `dot_data.py` contains the code to pull all of the data for a particular X and Y coordinate.

## Production

* TBD - Probably using NodeJS Forever API to keep script running permanently from host system.