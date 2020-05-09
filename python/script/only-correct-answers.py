# ~~~~parameters~~~~~
# the src file with answer
src = '/home/vistajin/Desktop/test-aws-saa-with-answer.txt'
# the key to the one you want to search
key = 'DynamoDB'


def remove_blank_line(s):
    return "".join([s for s in s.splitlines(True) if s.strip()]).strip()


with open(src, 'r', encoding='UTF-8') as f:
    all_content = f.read()
    questions = str(all_content).split("Question ")
    del(questions[0])
    match = 0
    for q in questions:
        question = remove_blank_line(q.split("A.")[0])
        a = q.split("Answer: ")[1].split("\n")[0].strip()
        print("=============================")
        print(question)
        match = match + 1
        for n in range(0, len(a)):
            answer = a[n:n+1] + ". " + remove_blank_line(q.split(a[n:n+1] + ".")[1].split(chr(ord(a[n:n+1]) + 1) + ".")[0])
            print(answer)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Match: {%d}" % match)

