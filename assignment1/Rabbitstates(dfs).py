class RabbitState:
    def __init__(self, state, path=None):
        self.state = state
        self.path = path or [state]

    def is_goal(self):
        return self.state == ['R', 'R', 'R', ' ', 'L', 'L', 'L']

    def generate_moves(self):
        moves = []
        s = self.state
        for i in range(len(s)):
            if s[i] == 'L':
                # Move right by 1
                if i + 1 < len(s) and s[i + 1] == ' ':
                    new_state = s.copy()
                    new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
                    moves.append(RabbitState(new_state, self.path + [new_state]))
                # Jump right over L
                if i + 2 < len(s) and s[i + 1] == 'R' and s[i + 2] == ' ':
                    new_state = s.copy()
                    new_state[i], new_state[i + 2] = new_state[i + 2], new_state[i]
                    moves.append(RabbitState(new_state, self.path + [new_state]))

            elif s[i] == 'R':
                # Move left by 1
                if i - 1 >= 0 and s[i - 1] == ' ':
                    new_state = s.copy()
                    new_state[i], new_state[i - 1] = new_state[i - 1], new_state[i]
                    moves.append(RabbitState(new_state, self.path + [new_state]))
                # Jump left over R
                if i - 2 >= 0 and s[i - 1] == 'L' and s[i - 2] == ' ':
                    new_state = s.copy()
                    new_state[i], new_state[i - 2] = new_state[i - 2], new_state[i]
                    moves.append(RabbitState(new_state, self.path + [new_state]))
        return moves

def dfs(state, visited):
    state_tuple = tuple(state.state)
    if state_tuple in visited:
        return None
    visited.add(state_tuple)

    if state.is_goal():
        return state.path

    for move in state.generate_moves():
        result = dfs(move, visited)
        if result:
            return result
    return None

# Initial state: 3 Ls, empty, 3 Rs
initial_state = ['L', 'L', 'L', ' ', 'R', 'R', 'R']
start = RabbitState(initial_state)
visited = set()

# Run DFS
solution = dfs(start, visited)

# Print the solution path
if solution:
    print("✅ DFS Solution Path:")
    for step in solution:
        print(''.join(step))
else:
    print("❌ No solution found.")
