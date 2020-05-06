import random


# ~~~~parameters~~~~~
# the src file with answer
src = '/home/vistajin/Desktop/test-aws-saa-with-answer.txt'
# Update the question_num as the no. of questions you want to gen
question_num = 60


def remove_blank_line(s):
    return "".join([s for s in s.splitlines(True) if s.strip()]).strip()


with open(src, 'r', encoding='UTF-8') as f:
    all_content = f.read()
    questions = str(all_content).split("Question ")
    del(questions[0])
    for num in range(0, question_num):
        index = random.randint(0, len(questions))
        q = questions[index]
        question = remove_blank_line(q.split("Answer: ")[0])
        print("=========================%d=============================" % (num + 1))
        print("Question " + question)
        print("Answer: ")
        del (questions[index])

