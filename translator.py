import os
from deep_translator import GoogleTranslator

DIRECTORY = "files/"
TRANSLATED_DIRECTORY = "translated/"
DEST = "fa"


class Translator:
    file_types = []
    dest = ""

    def __init__(self, directory, translated_directory):
        self.directory = directory
        self.translated_directory = translated_directory
        self.dest = input("Please enter translation language (default: fa) : ") or DEST

    def __rename_files(self):
        print("Starting to rename...")
        files = os.listdir(self.directory)
        for file in files:
            if "srt" in file:
                Translator.file_types.append("srt")
                new_name = file.replace("srt", "txt")
            else:
                Translator.file_types.append("vtt")
                new_name = file.replace("vtt", "txt")
            os.rename(f"{self.directory}{file}", f"{self.directory}/{new_name}")

    def __google_translator(self, contents, offset, limit, loop_number, new_file_path):
        translator = GoogleTranslator(source="auto", target=self.dest)
        try:
            result = translator.translate(contents[offset : offset + limit])
        except Exception as e:
            print(e)
            return
        if Translator.file_types[loop_number] == "srt":
            open(new_file_path.replace("txt", "srt"), "a", encoding="utf-8").write(
                result.replace(": ", ":").replace("->", "-->").replace("،", ",")
            )
        else:
            open(new_file_path.replace("txt", "vtt"), "a", encoding="utf-8").write(
                result.replace(": ", ":").replace("->", "-->").replace("،", ",")
            )

    def __save_translated_files(self):
        print("Starting to translate...")
        files = os.listdir(self.directory)
        is_exists = os.path.exists(self.translated_directory)
        if not is_exists:
            os.makedirs(self.translated_directory)

        translated_files = os.listdir(self.translated_directory)
        for file in translated_files:
            os.remove(f"{self.translated_directory}/{file}")

        for file in files:
            file_path = f"{self.directory}{file}"
            new_file_path = f"{self.translated_directory}/{file}"
            opened_file = open(file_path)
            contents = opened_file.read()

            loop_number = 0
            offset = 0
            limit = 4000

            while loop_number <= len(contents) / limit:
                self.__google_translator(
                    contents, offset, limit, loop_number, new_file_path
                )
                offset += limit
                loop_number += 1
        print("Completed!")

    def translate(self):
        self.__rename_files()
        self.__save_translated_files()


translator = Translator(directory=DIRECTORY, translated_directory=TRANSLATED_DIRECTORY)
translator.translate()
