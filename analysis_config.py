import iris
import functools

max_val = 255 # maximum data value (i.e. 8 bit uint)

thredds_server = "http://ec2-52-16-245-62.eu-west-1.compute.amazonaws.com:8080/thredds/dodsC/testLab/"
img_data_server = "http://ec2-52-16-246-202.eu-west-1.compute.amazonaws.com:9000/molab-3dwx-ds/media/"
vid_dest = "http://ec2-52-16-246-202.eu-west-1.compute.amazonaws.com:9000/molab-3dwx-ds/media/"

topog_file = "/Users/niall/Data/ukv/ukv_orog.pp"

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

# profiles are namespaces which contain setting for different analysis types
profiles = {

"UKV2EGRR_LR": {"data_constraint": iris.Constraint(model_level_number=lambda v: v.point < 60),
                "extent": [-13.62, 6.406, 47.924, 60.866],
                "regrid_shape": [200, 200, 20],
                "proc_fn": None,
                "video_ending": "ogv",
                "ffmpeg_args_template": ["ffmpeg", "-r", "20", "-i", "FILES_IN",
                                     "-r", "20", "-c:v", "libtheora", "FILE_OUT"]
                }
                
"UKV2EGRR_HR": {"data_constraint": iris.Constraint(model_level_number=lambda v: v.point < 60),
                "extent": [-13.62, 6.406, 47.924, 60.866],
                "regrid_shape": [400, 400, 35],
                "proc_fn": None,
                "video_ending": "ogv",
                "ffmpeg_args_template": ["ffmpeg", "-r", "20", "-i", "FILES_IN",
                                     "-r", "20", "-c:v", "libtheora", "FILE_OUT"]
                }

}