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
    '*' : lambda a, b: a * b,
    '/' : lambda a, b: a / b,
    '+' : lambda a, b: a + b,
    '-' : lambda a, b: a - b
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
            print(self.__str__())
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
        ret_str = ''
        for op in self.ops:
            ret_str += str(str(int(op[0])) + ' ' + str(op[1]) + ' ' + str(int(op[2])) + ' = ' + str(int(op[3])) + '\n')
        return ret_str
        


def solve_numbers(target, numbers=None, histories=None):
    if histories:
        all_solved = True
        for i in range(len(histories)):
            if not histories[i][0].solved and len(histories[i][1]) > 0:
                all_solved = False
                new_histories = []
                hist = histories[i][0]
                numbers = histories[i][1]
                for j in range(len(numbers)):
                    outside_numbers = numbers[0:j] + numbers[j+1:]
                    for oper in ops.keys():
                        new_history = hist.op(oper, numbers[j])
                        if new_history != None:
                            new_histories.append((new_history, outside_numbers))
                histories = histories[0:i] + new_histories + histories[i+1:]
        if all_solved:
            return [history[0] for history in histories if history[0].solved]
        else:
            return solve_numbers(target, histories=histories)
    elif not histories and numbers:
        histories = []
        for i in range(len(numbers)):
            outside_numbers = numbers[0:i] + numbers[i+1:]
            histories.append((History(numbers[i], target), outside_numbers))
        histories = solve_numbers(target, histories=histories)
        return histories


def solve_iteratively(target, numbers):
    '''
    Iteratively append diverging histories (path through all permutations of operators and value orders)
    to a stack. Returns results much faster than recursive iteration above and doesn't hit any limits.
    '''
    solutions = []
    histories = []
    ## Setup History Stack
    for i in range(len(numbers)):
        histories.append((History(numbers[i], target), numbers[0:i] + numbers[i+1:]))
    while histories:
        history_tup = histories.pop()
        history = history_tup[0]
        numbers = history_tup[1]
        for i in range(len(numbers)):
            for op in ops.keys():
                new_history = history.op(op, numbers[i])
                if new_history:
                    if new_history.solved:
                        solutions.append(new_history)
                    else:
                        histories.append((new_history, numbers[0:i] + numbers[i+1:]))
    return solutions

if __name__ == '__main__':
    in_targ = 265
    in_nums = [5, 2, 10, 100, 50, 8]
    # solutions = solve_numbers(in_targ, numbers=in_nums)
    solution  = solve_iteratively(in_targ, in_nums)
    code.interact(local=locals())