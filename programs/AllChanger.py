import BaseText2HyperText
import HyperText2LinerText

if __name__ == '__main__':
    BaseText2HyperText.hyper_text_file("../base_files/base_text.txt", "../base_files/hyper_text.txt")
    HyperText2LinerText.convert_text_file("../base_files/hyper_text.txt", "../base_files/liner_text.txt")