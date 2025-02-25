def convert_text_file(input_file, output_file):
    data = open(input_file, "r", encoding="utf-8").read()
    data = data.split("===メモ===")[0]
    while (data[-1] == "\n"): data = data[:-1]

    re_data = data
    re_data = re_data.replace("\n", "\\n")
    re_data = re_data.replace("\"", "\\\"")
    re_data = re_data.replace("\'", "\\\'")
    re_data = re_data.replace("“", "\\\"")
    re_data = re_data.replace("”", "\\\"")

    temp_data = re_data
    re_data = ""
    b = ""
    for d in temp_data:
        if ((b == " ") and (d == " ")):
            re_data += "\\t"
            b = ""
        elif ((b != " ") and (d == " ")):
            b = " "
        elif ((b == " ") and (d != " ")):
            re_data += b + d
            b = ""
        else:
            re_data += d

    f = open(output_file, "w", encoding="utf-8")
    f.write(re_data)
    f.close()


if __name__ == '__main__':
    convert_text_file("../base_files/hyper_text.txt", "../base_files/liner_text.txt")
