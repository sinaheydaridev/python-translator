from googletrans import Translator as GoogleTranslator
import os

DIRECTORY = 'files/'
TRANSLATED_DIRECTORY = 'translated/'
DEST = 'fa'


class Translator:
    file_type = []
    dest = ""

    def __init__(self, directory, translated_directory):
        self.directory = directory
        self.translated_directory = translated_directory

    def get_dest(self):
        dest = input("Please enter translation language  (default: fa) : ") or DEST
        Translator.dest = dest
        return dest

    # Renamed file
    def file_rename(self):
        print("Start to rename...")
        files = os.listdir(self.directory)
        # Change file type
        for file in files:
            if 'srt' in file:
                Translator.file_type.append('srt')
                new_name = file.replace('srt', 'txt')
            else:
                Translator.file_type.append('vtt')
                new_name = file.replace('vtt', 'txt')
            print(file)
            os.rename(f'{self.directory}{file}', f'{self.directory}/{new_name}')

    # Translate file
    def file_translate(self):
        print("Start to translate...")
        files = os.listdir(self.directory)
        is_exists = os.path.exists(self.translated_directory)
        if not is_exists:
            os.makedirs(self.translated_directory)
        translated_files = os.listdir(self.translated_directory)
        for file in translated_files:
            os.remove(f'{self.translated_directory}/{file}')
        for file in files:
            # Paths
            file_path = f'{self.directory}/{file}'
            new_file_path = f'{self.translated_directory}/{file}'
            f = open(file_path)
            contents = f.read()
            # Numbers
            n = 0
            offset = 0
            limit = 4000
            # File translate
            while n <= len(contents) / limit:
                # Translate
                translator = GoogleTranslator()
                try:
                    result = translator.translate(
                    contents[offset:offset+limit], dest=self.dest)
                except Exception as e:
                    print(e)
                    return
                # Save text translated
                if Translator.file_type[0] == 'srt':
                    open(new_file_path.replace('txt', 'srt'), 'a', encoding='utf-8').write(
                        result.text.replace(': ', ':').replace('->', '-->').replace('،', ','))
                else:
                    open(new_file_path.replace('txt', 'vtt'), 'a', encoding='utf-8').write(result.text.replace(
                        ': ', ':').replace('->', '-->').replace('،', ',').replace('وب سایت', 'WEBVTT'))
                offset += limit
                n += 1

translator = Translator(directory=DIRECTORY, translated_directory=TRANSLATED_DIRECTORY)
translator.get_dest()
translator.file_rename()
translator.file_translate()
