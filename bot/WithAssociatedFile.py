import os
import typing

from PathFile import Paths
from utils.KOSTYAWrapper import KostyaWrapper


def WithAssociatedFile(cls: typing.Any) -> "Wrapper":
    @KostyaWrapper
    class Wrapper(cls):
        def __init__(self, *args: typing.Any) -> None:
            self.__associated_file_path = None
            self.create_associated_file_if_not_exists()

        def create_associated_file_if_not_exists(self) -> None:
            self.__associated_file_path = os.path.join(Paths.BotGeneratedFolder, self.get_id() + ".py")
            if not os.path.exists(self.__associated_file_path):
                with open(self.__associated_file_path, "w") as file:
                    file.write(self.get_template_body())

        def get_associated_file(self) -> str:
            return self.__associated_file_path

        def set_associated_file(self, name: str) -> None:
            self.__associated_file_path = name

    return Wrapper
