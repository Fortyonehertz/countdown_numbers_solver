import code
import sys

sys.setrecursionlimit(1500)
def mult(a, b):
    return a * b

def div(a, b):
    return a / b

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = {
    'mult' : mult,
    'div' : div,
    'add' : add,
    'sub' : sub
}

class History:
    def __init__(self, val, target, ops=None):
        if ops:
            self.ops = ops
        else:
            self.ops = []
        if val == target:
            self.solved = True
            print('SOLVED!')
            print(self.ops)
        else:
            self.solved = False
        self.current_val = val
        self.target = target
    def op(self, op, val):
        new_val = ops[op](self.current_val, val)
        if (not type(new_val) == int and not float.is_integer(new_val)) or new_val < 0:
            return None
        new_ops = self.ops + [(self.current_val, op, val, new_val)]
        return History(new_val, self.target, new_ops)
    def __str__(self):
        return str(self.ops)

def summarise(history):


def solve_numbers(target, numbers=None, histories=None):
    if histories:
        all_solved = True

        for i in range(len(histories)):
            if not histories[i][0].solved and len(histories[i][1]) > 0:
                # print('History: ', histories[i][0])
                # print('Len outside: ', len(histories[i][1]))
                all_solved = False
                new_histories = []
                hist = histories[i][0]
                numbers = histories[i][1]
                for j in range(len(numbers)):
                    outside_numbers = numbers[0:j] + numbers[j+1:]
                    for oper in ops.keys():
                        # print('Oper: ', oper)
                        # print('Number: ', numbers[i])
                        # print('Outside: ', outside_numbers)
                        new_history = hist.op(oper, numbers[j])
                        if new_history != None:
                            new_histories.append((new_history, outside_numbers))
                
                histories = histories[0:i] + new_histories + histories[i+1:]
        if all_solved:
            return [history[0] for history in histories if history[0].solved]
        else:
            return solve_numbers(target, histories=histories)
    elif not histories and numbers:
        # print('Setup called!')
        histories = []
        for i in range(len(numbers)):
            outside_numbers = numbers[0:i] + numbers[i+1:]
            histories.append((History(numbers[i], target), outside_numbers))
        histories = solve_numbers(target, histories=histories)
        return histories

if __name__ == '__main__':
    in_targ = 265
    in_nums = [5, 2, 10, 100, 50, 8]
    solutions = solve_numbers(in_targ, numbers=in_nums)
    code.interact(local=locals())