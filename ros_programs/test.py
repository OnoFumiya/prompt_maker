for i in range(10): 
    for j in range(10): print("\033[" + str(i) + str(j) + "m\\033[" + str(i) + str(j) + "m\033[0m ", end="")
    print()