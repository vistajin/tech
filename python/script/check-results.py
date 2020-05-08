import random


# ~~~~parameters~~~~~
# the file with answer
answer_file = '/home/vistajin/Desktop/test-aws-saa-with-answer.txt'
# the file you test
# test_file = '/home/vistajin/Desktop/wrong-answered-001.txt'
test_file = '/home/vistajin/Desktop/test-002.txt'
# test_file = '/home/vistajin/Desktop/test-001.txt'


def remove_blank_line(s):
    return "".join([s for s in s.splitlines(True) if s.strip()]).strip()


answer_dic = {}
with open(answer_file, 'r', encoding='UTF-8') as f:
    all_content = f.read()
    questions = str(all_content).split("Question ")
    del(questions[0])
    for q in questions:
        question = int(remove_blank_line(q.split("A.")[0]).split("\n")[0].split(" ")[0])
        # print(question)
        a = q.split("Answer: ")[1].split("\n")[0].strip()
        answer_dic[question] = a
# print(answer_dic)


with open(test_file, 'r', encoding='UTF-8') as f:
    all_content = f.read()
    questions = str(all_content).split("Question ")
    del (questions[0])
    correct = 0
    total = 0
    for q in questions:
        question = remove_blank_line(q.split("A.")[0])
        question_key = int(question.split("\n")[0].strip())
        a = q.split("Answer: ")[1].split("\n")[0].strip()
        if a == "":
            break
        total = total + 1
        if a == answer_dic[question_key]:
            correct = correct + 1
            print(str(total) + ". Correct for: " + str(question_key))
        else:
            print(str(total) + ". Wrong for: " + str(question_key) + ", answer: " + answer_dic[question_key] + ", yours: " + a)
            # print(str(total) + ". Wrong for: " + str(question_key))

    print("=========================================")
    print("Your score: %.2f " % (correct / total * 100))