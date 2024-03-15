from flask import Flask, request, render_template
import re
import json


def usage():
    return (f"first arg is the mandatory letter.  second arg is the other 6 letters")


class Word:
    def __init__(self, value):
        self.value = value.strip()
        self.is_pangram = False


class Hive:
    def __init__(self, center_letter, ans_letters):
        self.center_letter = center_letter
        self.ans_letters = ans_letters

    def solve(self):
        f = open("/usr/share/dict/words", "r")

        included_letters = self.center_letter + self.ans_letters

        def get_excluded_letters():
            excluded_letters = ''
            for c in list(map(chr, range(ord('a'), ord('z') + 1))):
                if not re.search(f"[{included_letters}]", c):
                    excluded_letters += c
            return excluded_letters

        def is_pangram(w):
            return len(set(w.strip())) == len(set(included_letters.strip()))

        words = []
        excluded_letters = get_excluded_letters()

        for w in f:
            w = w.strip()
            if len(w) >= 4 \
                    and re.search('^[a-z]+$', w) \
                    and re.search(self.center_letter, w) \
                    and not re.search(f"[{excluded_letters}]", w):
                w = Word(w)
                if is_pangram(w.value):
                    w.is_pangram = True
                words.append(w)
        return {'words': words}


app = Flask(__name__)


@app.route('/solve', methods=['GET'])
def solve():
    center_letter = request.args['center']
    other_letters = request.args['others']

    errors = []
    if center_letter is None:
        errors.append("center_letter is missing")
    if other_letters is None:
        errors.append("other_letters is missing")
    if len(other_letters) == 1:
        errors.append("other_letters size should be greater than 1")
    if len(center_letter) != 1:
        errors.append("center_letter size should be 1")

    if len(errors) > 0:
        return {'usage': usage(), 'errors': errors}
    else:
        hive = Hive(center_letter, other_letters)
        solution = hive.solve()
        return render_template('solution.html', solution=solution)


@app.route('/')
def home():
    return render_template('solver.html')


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
