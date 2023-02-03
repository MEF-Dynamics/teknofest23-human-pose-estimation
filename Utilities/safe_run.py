import  shutil
import  json
import  os

def safe_start() -> None:
    """
    Method to check program structure and create folders if not exists.
    @Params:
        None
    @Returns:
        None
    """
    PROGRAM_STRUCTURE_CHECK_LIST = ["Assets/GUI", "GUI", "Resources", "Utilities"]
    # Check these folders in PROGRAM_STRUCTURE_CHECK_LIST. Raise error if not exists.
    for path in PROGRAM_STRUCTURE_CHECK_LIST :
        if not os.path.exists(path) :
            raise FileNotFoundError("Program structure does not match, please reinstall the program. Missing: " + path)

    # check config file in "Resources/Config/config.json"
    CONFIG_FILE_PATH = "Resources/Config/config.json"
    if not os.path.exists(CONFIG_FILE_PATH) :
        raise FileNotFoundError("Config file does not exist, please create config file :", CONFIG_FILE_PATH, "{\"POSTGRE_PASSWORD\":\"password\"}")
    else :
        try :
            with open(CONFIG_FILE_PATH, "r") as file :
                configs = json.load(file)

            POSTGRE_PASSWORD = configs["POSTGRE_PASSWORD"]
        except :
            with open(CONFIG_FILE_PATH, "w") as file :
                json.dump({}, file, indent=4)
            raise FileNotFoundError("Config file is corrupted, please check config file :", CONFIG_FILE_PATH,  "{\"POSTGRE_PASSWORD\":\"password\"}")

def safe_stop() -> None:
    """
    Method to check program structure and delete folders if exists.
    @Params:
        None
    @Returns:
        None
    """
    PROGRAM_POST_CACHE_CHECK_LIST = ["GUI", "Utilities"]
    # Check python cache folders in PROGRAM_POST_CACHE_CHECK_LIST. Delete if exists.
    for path in PROGRAM_POST_CACHE_CHECK_LIST :
        if os.path.exists(os.path.join(path, "__pycache__")) :
            shutil.rmtree(os.path.join(path, "__pycache__"))