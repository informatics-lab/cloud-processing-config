import iris
import functools
import numpy as np

max_val = 255 # maximum data value (i.e. 8 bit uint)

thredds_server = "http://ec2-52-16-245-62.eu-west-1.compute.amazonaws.com:8080/thredds/dodsC/testLab/"
img_data_server = "http://ec2-52-16-246-202.eu-west-1.compute.amazonaws.com:9000/molab-3dwx-ds/media/"
vid_dest = "http://ec2-52-16-246-202.eu-west-1.compute.amazonaws.com:9000/molab-3dwx-ds/media/"

topog_file = "http://ec2-52-16-245-62.eu-west-1.compute.amazonaws.com:8080/thredds/dodsC/testLab/global_dem.nc"

sea_level = 3 # minimum altitude number


def saturateClouds(c, min_val=None, max_val=None):
    c.data -= min_val
    c.data /= (max_val-min_val)
    c.data[c.data<=0.0] = 0.0
    c.data[c.data>=1.0] = 1.0

    return c

def binarySaturateClouds(c, cutoff):
    c.data[c.data<cutoff] = 0.0
    c.data[c.data>cutoff] = 1.0

    return c

def degrib_cb(c, f, n):
    levc = c.coord("level")
    levcdim, = c.coord_dims(levc)
    newc = iris.coords.DimCoord(levc.points, "height", long_name="level_height", units="m")
    c.remove_coord(levc)
    c.add_dim_coord(newc, levcdim) 

    c.coord("time").rename("forecast_time")
    frtc = iris.coords.AuxCoord.from_coord(c.coord("forecast_time")[0])
    frtc.rename("forecast_reference_time")
    c.add_aux_coord(frtc)

    return c

def latlon2Dto1D_cb(c, f, n):
    latc = c.coord("latitude")
    newlatc = iris.coords.DimCoord(np.mean(latc.points, 1),
                                    standard_name="latitude", units="degrees")
    lonc = c.coord("longitude")
    newlonc = iris.coords.DimCoord(np.mean(lonc.points, 0),
                                    standard_name="longitude", units="degrees")

    c.remove_coord("latitude")
    c.remove_coord("longitude")
    c.remove_coord("x-coordinate in Cartesian system")
    c.remove_coord("y-coordinate in Cartesian system")

    c.add_dim_coord(newlatc, c.ndim-2)
    c.add_dim_coord(newlonc, c.ndim-1)

    return c

def ukv_cb(c, f, n):
    c = latlon2Dto1D_cb(c, f, n)
    c = degrib_cb(c, f, n)

    return c

# profiles are namespaces which contain setting for different analysis types
profiles = {

"UKV2EGRR_LR": {"data_constraint": iris.Constraint(coord_values={"height": lambda v: v.point < 5e3}),
                "extent": [-13.62, 6.406, 47.924, 60.866],
                "regrid_shape": [200, 200, 20],
                "proc_fn": None,
                "load_call_back": ukv_cb,
                "video_ending": "ogv",
                "ffmpeg_args_template": ["ffmpeg", "-r", "20", "-i", "FILES_IN",
                                     "-r", "20", "-c:v", "libtheora", "FILE_OUT"]
                },
                
"UKV2EGRR_HR": {"data_constraint": iris.Constraint(coord_values={"height": lambda v: v.point < 5e3}),
                "extent": [-13.62, 6.406, 47.924, 60.866],
                "regrid_shape": [400, 400, 35],
                "proc_fn": None,
                "load_call_back": ukv_cb,
                "video_ending": "ogv",
                "ffmpeg_args_template": ["ffmpeg", "-r", "20", "-i", "FILES_IN",
                                     "-r", "20", "-c:v", "libtheora", "FILE_OUT"]
                }

}