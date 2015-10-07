"""
Specify the names of the profiles (defined in the image service config.py)
which define the typ on analysis to perform. Can be a function of variable
and model.

"""

runnames = {"umqvaa": {
                "model": "UKV",
                "variables": ["cloud_volume_fraction_in_atmosphere_layer", "air_temperature"],
                "profile": "UKV2EGRR",
                "nframes": 36
                }
            }