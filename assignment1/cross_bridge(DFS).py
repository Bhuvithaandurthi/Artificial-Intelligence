times = {
    "Amogh": 5,
    "Ameya": 10,
    "Grandmother": 20,
    "Grandfather": 25
}

initial_state = ({"Amogh", "Ameya", "Grandmother", "Grandfather"}, set(), "left", 0)
visited = {}
gpath = []

def dfs(state, path):
    global gpath
    left, right, umbrella_side, time_passed = state

    if len(right) == 4:
        if time_passed <= 60:
            if not gpath or time_passed < gpath[-1]:
                gpath = path + [f" Finished in {time_passed} minutes"]
        return

    config = (frozenset(left), frozenset(right), umbrella_side)
    
    if config in visited and visited[config] <= time_passed:
        return
    visited[config] = time_passed

    if umbrella_side == "left":
        people = list(left)
        for i in range(len(people)):
            for j in range(i, len(people)):
                p1, p2 = people[i], people[j]
                time = max(times[p1], times[p2])
                if time_passed + time > 60:
                    continue
                new_left = left - {p1, p2}
                new_right = right | {p1, p2}
                new_state = (new_left, new_right, "right", time_passed + time)
                des = f"{p1} and {p2} cross in {time} min"
                dfs(new_state, path + [des])
    else:
        for p in right:
            time = times[p]
            if time_passed + time > 60:
                continue
            new_left = left | {p}
            new_right = right - {p}
            new_state = (new_left, new_right, "left", time_passed + time)
            des = f"{p} returns in ({time} min)"
            dfs(new_state, path + [des])

dfs(initial_state, [])
if gpath:
    print("\n".join(gpath))
else:
    print(" No solution found within 60 minutes.")
