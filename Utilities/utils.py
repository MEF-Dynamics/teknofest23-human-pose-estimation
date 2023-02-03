from    pygrabber.dshow_graph   import  FilterGraph
from    PIL                     import  Image
import  json

def get_available_cameras() -> dict:
    """
    Method, that returns the cameras that are available on the computer.
    @Params
        None
    @Returns
        available_cameras : dict - Available cameras.
    """
    devices = FilterGraph().get_input_devices()

    available_cameras = {}

    for device_index, device_name in enumerate(devices):
        available_cameras[device_index] = device_name

    return available_cameras

def get_gif_frame_count(gif_file_path:str) -> int:
    """
    Method, that returns the number of frames in a gif file.
    @Params
        gif_file_path : str - (Required) The path to the gif file.
    @Returns
        number_of_frames : int - The number of frames in the gif file.
    """
    with Image.open(gif_file_path) as gif_file:
        number_of_frames = 0
        while True:
            try:
                gif_file.seek(number_of_frames)
                number_of_frames += 1
            except EOFError:
                break

    return number_of_frames

def read_config(config_file_path:str) -> dict:
    """
    Method, that reads the config file and returns the config file as a dictionary.
    @Params
        config_file_path : str - (Required) The path to the config file.
    @Returns
        config_file : dict - The config file as a dictionary.
    """
    config_file = {}

    with open(config_file_path, "r") as config_file:
        config_file = json.load(config_file)

    return config_file