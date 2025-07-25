from collections import deque
times = {
    "Amogh": 5,
    "Ameya": 10,
    "Grandmother": 20,
    "Grandfather": 25
}

initial_state = ({"Amogh", "Ameya", "Grandmother", "Grandfather"}, set(), "left", 0)   #initially all are on left side
queue = deque()                                       #used deque rather than list ,operations like append,pop are faster on deque
queue.append((initial_state, []))      
visited = set()
while queue:
    (left, right, umbrella_side, time_passed), path = queue.popleft()
    if len(right) == 4 and time_passed <= 60:
        print("all crossed in",time_passed , "minutes")
        for step in path:
            print(step)
        break
    config = (frozenset(left), frozenset(right), umbrella_side)
    if config in visited:
        continue
    visited.add(config)

    if umbrella_side == "left":                      # Send 2 people from left to right
        people = list(left)
        for i in range(len(people)):
            for j in range(i, len(people)):
                p1, p2 = people[i], people[j]
                time = max(times[p1], times[p2])
                if time_passed + time > 60:
                    continue
                new_left = left - {p1, p2}
                new_right = right | {p1, p2}
                des = f"{p1} and {p2} cross in {time} min"
                new_state = (new_left, new_right, "right", time_passed+time)
                queue.append((new_state, path + [des]))
    else:                                       # Send 1 person from right to left
        for p in right:
            time = times[p]
            if time_passed + time > 60:
                continue
            new_left = left | {p}
            new_right = right - {p}
            des = f"{p} returns  in {time} min"
            new_state = (new_left, new_right, "left", time_passed+time)
            queue.append((new_state, path + [des]))
