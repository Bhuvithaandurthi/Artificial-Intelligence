from collections import deque

class RabbitLeap:
    def __init__(self, state, path=[]):
        self.state = state
        self.path = path + [state]

    def goaltest(self):
        return self.state == ['L', 'L', 'L', '_', 'R', 'R', 'R']

    def move_gen(self):
        moves = []
        for i in range(len(self.state)):
            if self.state[i] == 'R':             #rabbits on right
                if i + 1 < len(self.state) and self.state[i + 1] == '_':
                    new_state = self.state.copy()
                    new_state[i], new_state[i + 1] = '_', 'R'
                    moves.append(RabbitLeap(new_state, self.path))
                if i + 2 < len(self.state) and self.state[i + 1] == 'L' and self.state[i + 2] == '_':
                    new_state = self.state.copy()
                    new_state[i], new_state[i + 2] = '_', 'R'
                    moves.append(RabbitLeap(new_state, self.path))

        
            elif self.state[i] == 'L':       #rabbits on left
                if i - 1 >= 0 and self.state[i - 1] == '_':
                    new_state = self.state.copy()
                    new_state[i], new_state[i - 1] = '_', 'L'
                    moves.append(RabbitLeap(new_state, self.path))
                # Jump over one R into empty space
                if i - 2 >= 0 and self.state[i - 1] == 'R' and self.state[i - 2] == '_':
                    new_state = self.state.copy()
                    new_state[i], new_state[i - 2] = '_', 'L'
                    moves.append(RabbitLeap(new_state, self.path))
        return moves

def rabbit_leap():
    initial_state = ['R', 'R', 'R', '_', 'L', 'L', 'L']
    start = RabbitLeap(initial_state)

    queue = deque([start])
    visited = set()

    while queue:
        current = queue.popleft()
        state_tuple = tuple(current.state)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if current.goaltest():
            print(" Path:")
            for step in current.path:
                print(''.join(step))
            return

        for move in current.move_gen():
            queue.append(move)

    print(" No solution found.")
rabbit_leap()
