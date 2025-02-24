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


def llm_recognition(node=None):
    global feedback_msg
    action_client = ActionClient(node, ChatLlmRecognition, "/ollama_action")
    if not action_client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error("Action server not available!")
        rclpy.shutdown()
        return

    send_msg = ChatLlmRecognition.Goal()
    send_msg.room_name = "GPSR"
    # send_msg.model_name = "llama3.2"
    # send_msg.model_name = "llama3.2-vision"
    # send_msg.model_name = "llama3"
    # send_msg.model_name = "deepseek-llm"
    send_msg.model_name = "phi4"

    funcs = selection()

    print("Imperative Statement : ", end="")
    imperative_statement = str(input())

    print("Past Transitions")
    past_transitions = ""
    while True:
        print(" ".join(list(funcs.keys())) + " : ", end="")
        functions = str(input())
        if (functions == ""):
            break
        val = ""
        if (funcs[functions]):
            if (type(funcs[functions]) == list):
                print(" ".join(funcs[functions]) + " : ", end="")
            else:
                print(funcs[functions] + " : ", end="")
            val = str(input())
        print(functions + "\'s Results (option:SUCCESS,FAILED) : ", end="")
        res = str(input())
        past_transitions += "\n- " + functions + "(" + val + ") -> " + res

    send_msg.request = "Imperative Statement : " + imperative_statement + "\nPast Transitions :" + past_transitions
    print("=============================\033[36m")
    print(send_msg.request + "\033[0m")
    print("=============================")
    
    send_msg.is_stack = False
    send_msg.image = []

    # ゴールを送信してフィードバックと結果を処理
    future = action_client.send_goal_async(
        send_msg, feedback_callback=feedback_callback
    )
    rclpy.spin_until_future_complete(node, future)

    # ゴール送信の結果を取得
    goal_handle = future.result()

    wip_result = ""
    while not feedback_msg.end_flag:
        rclpy.spin_once(node)

        # if ((len(wip_result) != len(feedback_msg.wip_result))):
        #     wip_result = feedback_msg.wip_result
        #     print("\n------------------FEEDBACK--------------------")     # こちらはFeedbackとして黄色で出力されます．おそらく未完成の文が順に出力されているでしょう
        #     print("\033[33m", wip_result, "\033[0m")
        #     print("----------------------------------------------")

    # 結果の取得
    result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, result_future)
    result = result_future.result().result

    # 結果の出力
    print("\n------------------RESULT--------------------")     # こちらは最終的な出力が緑色で出力されます．
    print("Result: \033[92m",result.result)
    print("\t\t\t\t\t\033[0m(Elapsed Time: ", result.elapsed_time, ")")  # 返答までにかかった時間も出力されます
    print("--------------------------------------------")


def main():
    # rclpyの初期化
    rclpy.init()

    # ノードの作成
    node = Node("test_ollama_ros_llm")

    while rclpy.ok():
        llm_recognition(node)   # ノードをmain関数に継承する
        print("===")

    rclpy.spin(node)



if __name__ == "__main__":
    main()
