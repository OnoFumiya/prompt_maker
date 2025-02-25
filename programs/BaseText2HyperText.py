import os
import datetime
import calendar

dt_now = datetime.datetime.now()
month_name = (["January","February","March","April","May","June","July","August","September", "October","November","December"])[dt_now.month-1]
weekday_name = calendar.day_name[datetime.date.today().weekday()]


replace_txt = {
    "DATE"        : str(weekday_name) + ", " + month_name + " " + str(dt_now.day) + ", " + str(dt_now.year),
    "ROBOT_NAME"  : "SOBIT PRO",
    "HOST_NAME"   : "Tom",
}




def hyper_text_file(input_file, output_file):
    data = open(input_file, "r", encoding="utf-8").read()
    data = data.split("===メモ===")[0]
    while (data[-1] == "\n"): data = data[:-1]

    re_data = data
    for k in os.listdir("../import_files"):
        file_data = open("../import_files/" + k, "r", encoding="utf-8").read()
        file_data = file_data.split("===メモ===")[0]

        while (file_data[-1] == "\n"): file_data = file_data[:-1]

        if ("${file=" + k + "}$" in re_data): print("===\n\033[33m" + str(k) + "\033[0m\n ↓ \n\033[35m" + str(file_data) + "\033[0m")
        re_data = re_data.replace("${file=" + k + "}$", file_data)

    for k in replace_txt.keys():
        if ("${value=" + k + "}$" in re_data): print("===\n\033[33m" + str(k) + "\033[0m --> \033[35m" + str(replace_txt[k]) + "\033[0m")
        re_data = re_data.replace("${value=" + k + "}$", replace_txt[k])

    print("===")

    f = open(output_file, "w", encoding="utf-8")
    f.write(re_data)
    f.close()

if __name__ == '__main__':
    hyper_text_file("../base_files/base_text.txt", "../base_files/hyper_text.txt")
