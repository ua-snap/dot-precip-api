"""
For a given pair of X and Y coordinates,
return an xarray.DataArray of all the
precipitation frequency available from
the NC files.
"""

import os
import xarray as xr
import numpy as np
import psycopg2

DATADIR = os.getenv("DATADIR", default="/usr/local/data/undiff/")

DURATIONS = [
    "60m",
    "2h",
    "3h",
    "6h",
    "12h",
    "24h",
    "2d",
    "3d",
    "4d",
    "7d",
    "10d",
    "20d",
    "30d",
    "45d",
    "60d",
]
DATASETS = ["GFDL-CM3", "NCAR-CCSM4"]
TIMESLICES = [("2020", "2049"), ("2050", "2079"), ("2080", "2099")]
VARIABLES = ["pf_upper", "pf", "pf_lower"]
INTERVALS = [2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 200.0, 500.0, 1000.0]


def get_percentile_data(xcoord, ycoord):

    x = float(xcoord)
    y = float(ycoord)

    all_zeros = np.zeros(
        [len(DATASETS), len(DURATIONS), len(TIMESLICES), len(VARIABLES), len(INTERVALS)]
    )

    returned_data = xr.DataArray(
        data=all_zeros,
        coords=[
            DATASETS,
            DURATIONS,
            [f"{i[0]}-{i[1]}" for i in TIMESLICES],
            VARIABLES,
            INTERVALS,
        ],
        dims=["gcm", "duration", "timerange", "variable", "interval"],
    )

    for dataset in DATASETS:
        for duration in DURATIONS:
            for ts in TIMESLICES:
                ts_str = f"{ts[0]}-{ts[1]}"
                ds = xr.open_dataset(
                    os.path.join(
                        DATADIR,
                        f"pcpt_{dataset}_sum_wrf_{duration}_{ts_str}_undiff.nc",
                    )
                )
                for var in VARIABLES:
                    returned_data.loc[
                        dict(
                            gcm=dataset,
                            duration=duration,
                            timerange=ts_str,
                            variable=var,
                        )
                    ] = ds.sel(xc=[x], yc=[y], method="nearest")[var].values[..., 0, 0]

    return returned_data


if __name__ == "__main__":
    # Test data to confirm things are working
    # get_percentile_data(-2173040, 882215)
    get_percentile_data(-117682.86362522288, 1963676.5978819495)
