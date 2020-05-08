# ~~~~parameters~~~~~
# the src file with answer
test_file = '/home/vistajin/Desktop/test-001.txt'


flag = False
with open(test_file, 'r', encoding='UTF-8') as f:
    all_content = f.readlines()
    for line in all_content:
        if line.startswith("*Question"):
            flag = True
            print("===================================")
            line = line.replace("*", "")
        elif line.find("Answer: ") != -1:
            if flag:
                print("Answer: ")
            flag = False
        if flag:
            print(line.strip())

