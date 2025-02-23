import datetime
import calendar

dt_now = datetime.datetime.now()
month_name = (["January","February","March","April","May","June","July","August","September", "October","November","December"])[dt_now.month-1]
weekday_name = calendar.day_name[datetime.date.today().weekday()]



replace_txt = {
    "DATE"        : str(weekday_name) + ", " + month_name + " " + str(dt_now.day) + ", " + str(dt_now.year),
    "ROBOT_NAME"  : "SOBIT PRO",
}




def hyper_text_file(input_file, output_file):
    print("===")
    data = open(input_file, "r", encoding="utf-8").read()
    data = data.split("===メモ===")[0]

    while True:
        if (data[-1] == "\n"):
            data = data[:-1]
        else:
            break
    
    re_data = data
    for k in replace_txt.keys():
        re_data = re_data.replace("${value=" + k + "}$", replace_txt[k])
        print("\033[33m" + str(k) + "\033[0m --> \033[35m" + str(replace_txt[k]) + "\033[0m")

    find_file = re_data.split("${file=")
    file_names = []
    file_tabs = []
    for i in range(len(find_file)-1):
        file_name = ""
        file_tab = ""
        for s in find_file[i+1]:
            if (s == "}"):
                break
            else:
                file_name += s
        for n in range(len(find_file[i])//2):
            if (find_file[i][len(find_file[i])-1-(2*n+1)] != " "):
                break
            if ((find_file[i][len(find_file[i])-1-(2*n+1)] == " ") and (find_file[i][len(find_file[i])-1-(2*n)] == " ")):
                file_tab += "  "
        file_names += [file_name]
        file_tabs += [file_tab]

    for file_name in file_names:
        file_data = open("../import_files/" + file_name, "r", encoding="utf-8").read()
        file_data = file_data.split("===メモ===")[0]

        while True:
            if (file_data[-1] == "\n"):
                file_data = file_data[:-1]
            else:
                break

        re_data = re_data.replace("${file=" + file_name + "}$", file_data)
        print("===\n\033[33m" + str(file_name) + "\033[0m\n ↓ \n\033[35m" + str(file_data) + "\033[0m")

    print("===")
    f = open(output_file, "w", encoding="utf-8")
    f.write(re_data)
    f.close()

if __name__ == '__main__':
    hyper_text_file("../base_files/base_text.txt", "../base_files/hyper_text.txt")
