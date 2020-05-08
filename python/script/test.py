
q = 'Question 297'
options = {}
answer = 'Answer: '
find_q = False
with open('/home/vistajin/Desktop/test-aws-saa-with-answer.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        line = str(line).strip()
        if line == "": continue
        if line.find(q) != -1:
            find_q = True
            continue
        if find_q and line.find("Question") != -1:
            break
        if find_q:
            print(line)
