"""
Script for importing Xarray binary blobs into a PostgreSQL
database of X, Y, and binary data fields for faster searching of
values than scraping all of the
"""

import xarray as xr
import dask
import numpy as np
import psycopg2
import pickle
import multiprocessing as mp
import dot_data


def do_work(xy):
    conn = psycopg2.connect("dbname='precip' user='precip' password='w@terdropl3ts'")
    cur = conn.cursor()
    data = dot_data.get_percentile_data(xy[1], xy[0])
    pickled_data = pickle.dumps(data, protocol=-1)
    cur.execute(
        "INSERT INTO precip_data (x, y, data) VALUES (%s,%s,%s)",
        (xy[1], xy[0], pickled_data),
    )
    conn.commit()
    cur.close()
    conn.close()
    return


def insert_data():

    coords = xr.open_dataset(
        "/usr/local/data/combined/pcpt_NCAR-CCSM4_sum_wrf_6h_2020-2049_combined.nc"
    )
    with mp.Pool(processes=36) as pool:
        for x in coords.xc.values:
            args = [(y, x) for y in coords.yc.values]
            pool.map(do_work, args)
    return


if __name__ == "__main__":
    # Run insert data to start computing each X & Y coordinate into a 5D
    # representation of the data accessible by the X & Y value at a given
    # point in the EPSG:3338 map projection.
    insert_data()
