import os

from PathFile import Paths
from utils.KOSTYAWrapper import KostyaWrapper


def WithAssociatedFile(cls):
    @KostyaWrapper
    class Wrapper(cls):
        def __init__(self, *args):
            self.__associated_file_path = None
            self.create_associated_file()

        def create_associated_file(self):
            self.__associated_file_path = os.path.join(Paths.BotGeneratedFolder, self.get_id() + '.py')
            with open(self.__associated_file_path, 'w') as file:
                pass

        def get_associated_file(self):
            return self.__associated_file_path

    return Wrapper
