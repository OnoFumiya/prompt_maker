import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from sobits_interfaces.action import ChatLlmRecognition
import os


def selection():
    data = open("../import_files/function_list.txt", "r", encoding="utf-8").read()
    data = data.split("===メモ===")[0]
    data = data.replace("  - ", "@@@@")

    datas = data.split("\n- ")[1:]

    func_list = []
    arg_lists = []
    for d in datas:
        func_list += [d.split("(")[0]]
        if (d.replace("- ", "").split("(")[0] + "()" in d):
            arg_lists += [False]
        else:
            d = d.replace("@@@@", "").replace("\n", " ").replace(",", "").replace(".", "").replace("\"", "").replace("\'", "").replace("“", "").replace("”", "")
            for s in d.split(" "):
                if (os.path.isfile("../import_files/" + s + ".txt")):
                    break
            if (os.path.isfile("../import_files/" + s + ".txt")):
                value = open("../import_files/" + s + ".txt", "r", encoding="utf-8").read()
                value_list = []
                for v in value.split("\n"):
                    if ("- " in v):
                        value_list += [v.replace("- ", "")]
                arg_lists += [value_list]
            else:
                arg_lists += ["Custom Value"]

    dictional = {}
    for i in range(len(func_list)):
        dictional[func_list[i]] = arg_lists[i]

    return dictional


feedback_msg = ChatLlmRecognition.Feedback()
def feedback_callback(msg):
    global feedback_msg
    feedback_msg = msg.feedback


def llm_recognition(node, cont):
    global feedback_msg
    action_client = ActionClient(node, ChatLlmRecognition, "/ollama_action")
    if not action_client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error("Action server not available!")
        rclpy.shutdown()
        return

    send_msg = ChatLlmRecognition.Goal()
    send_msg.room_name = "GPSR_NEW"
    # send_msg.model_name = "llama3.2"
    # send_msg.model_name = "llama3.2-vision"
    # send_msg.model_name = "llama3"
    # send_msg.model_name = "minicpm-v"
    # send_msg.model_name = "deepseek-r1"
    # send_msg.model_name = "deepseek-llm"
    send_msg.model_name = "phi4"

    ###################################################################
    print("\n-------------------------------\n\nLast Result : " + cont + " -> \n\n\n\n\n\n\n\n\n", end="")
    print("")
    print("\033[10F\033[" + str(len(cont) + 18) + "C", end="")
    last_result = str(input())
    send_msg.request = "Last Result : " + cont + " -> " + last_result
    ###################################################################

    print("\033[2F=============================\033[36m")
    print(send_msg.request + "\033[0m")
    print("=============================")
    
    send_msg.is_stack = True
    send_msg.image = []

    future = action_client.send_goal_async(send_msg, feedback_callback=feedback_callback)
    rclpy.spin_until_future_complete(node, future)
    goal_handle = future.result()

    wip_result = ""
    print("\n------------------FEEDBACK--------------------\n\033[K\n----------------------------------------------\n\n\n\n")
    while not feedback_msg.end_flag:
        rclpy.spin_once(node)
        if ((len(wip_result) != len(feedback_msg.wip_result))):     # こちらはFeedbackとして黄色で出力されます．未完成の文が出力される
            wip_result = feedback_msg.wip_result
            print("\033[7F\033[K" + "------------------FEEDBACK--------------------")
            print("\033[K\033[93m" + wip_result + "\033[0m")
            print("\033[K" + "----------------------------------------------\n\n\n\n")


    # 結果の取得
    result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, result_future)
    result = result_future.result().result
    feedback_msg.end_flag = False
    feedback_msg.wip_result = ""

    # 結果の出力
    print("\033[7F\033[K" + "------------------RESULT--------------------\n\033[K\033[92m" + result.result + "\033[0m")
    print("\033[K" + "----------------------------------------------")
    print("\t\t\t\t\t\033[0m(Elapsed Time: ", result.elapsed_time, ")")  # 返答までにかかった時間も出力されます
    return result.result


def main():
    # rclpyの初期化
    rclpy.init()

    # ノードの作成
    node = Node("test_ollama_ros_llm")
    cont = "End()"
    while rclpy.ok():
        cont = llm_recognition(node, cont)   # ノードをmain関数に継承する
        print("===")

    rclpy.spin(node)



if __name__ == "__main__":
    main()