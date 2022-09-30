# importing the required libraries
from pyautogui import screenshot
from time import time, strftime, localtime
from os import path, makedirs


class FileManagerClass:

    def __init__(self):
        self.directory = "./data/screenshot_folder"

        self.create_directory(self.directory)

    def get_directory(self):
        return self.directory

    def get_session_instance(self):
        return self.directory + "/instance_" + strftime("%b_%d_%H_%M_%S", localtime(time()))

    ####################  STATIC METHODS  ####################
    @staticmethod
    def create_directory(target_path: str = ""):
        try:
            # Create Data Folder first
            if not path.exists(target_path):
                makedirs(target_path)
        except Exception as e:
            print("Error in Directory creation:", e)

    @staticmethod
    def save_txt_file(file_name: str = "", mode: str = "a", content: list = None):
        if content is None:
            content = []

        with open(file_name, mode) as output_file:
            for line in content:
                output_file.write(line)
