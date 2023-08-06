import os
from typing import overload

BASEDIR = os.path.join("bot", "messages", "templates")


class MessageTemplate:

    __basedir = BASEDIR
    ext = "txt"

    def __init__(self, filename: str) -> None:
        name = filename.split(".")[0]
        self.name = name
        self.text = self.__init_content()

    def __init_content(self) -> str:
        with open(self.path, "r") as file:
            return file.read()

    def __repr__(self) -> str:
        return f"MessageTemplate<{self.name}>"

    def update_content(self, text: str) -> None:
        with open(self.path, "w") as file:
            file.write(text)

        self.text = text

    @property
    def path(self) -> str:
        return os.path.join(self.__basedir, f"{self.name}.{self.ext}")


class MessageTemplatesDict(dict):

    ext = "txt"

    def __init__(self) -> None:
        self.BASEDIR = BASEDIR
        self.__init_message_templates()

    def __init_message_templates(self):
        for filename in os.listdir(BASEDIR):
            mt = MessageTemplate(filename)
            self[mt.name] = mt

    def __create_template_file(self, filename: str) -> MessageTemplate:
        with open(os.path.join(self.BASEDIR, f"{filename}.{self.ext}"), "w") as file:
            file.write(f"This is new file for \"{filename}\" handler ")
        return MessageTemplate(filename)

    def __delete_template_file(self, filename):
        os.remove(os.path.join(self.BASEDIR, filename))

    def get(self, __key: str) -> MessageTemplate:
        __val = super().get(__key)
        if __val:
            return __val
        return self.__create_template_file(__key)

    def __getitem__(self, __key: str) -> str:
        return self.get(__key).text

    def pop(self, __key: str):
        super().pop(__key)
        self.__delete_template_file(__key)
