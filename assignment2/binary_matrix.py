
import heapq         #we needs priority queue to store nodes based on f value
import math

class FindPath:
    def __init__(self, grid):
        self.grid = grid                 
        self.n = len(grid)                
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),(0, 1),
                           (1, -1),(1, 0), (1, 1)]

    def is_valid(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and self.grid[x][y] == 0
   
    def heuristic(self, x, y):               #here we are considering euclidean distance from current node to goal as heuristic 
        goal_x, goal_y = self.n - 1, self.n - 1  
        return math.sqrt((x - goal_x) ** 2 + (y - goal_y) ** 2)
    #Best First search

    def best_first_search(self):
        if self.grid[0][0] == 1 or self.grid[self.n - 1][self.n - 1] == 1:
            return -1, []              #i.e no path is exists
        pq = []                      # priority queue 
      
        heapq.heappush(pq, (self.heuristic(0, 0), (0, 0)))         
        parent = {(0, 0): None}    #used while reconstructing the path
        visited = set()
        while pq:  
            _, (x, y) = heapq.heappop(pq)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) == (self.n - 1, self.n - 1):
                return self.reconstruct_path(parent, (x, y))

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny) and (nx, ny) not in visited:
                    parent[(nx, ny)] = (x, y)  # remember how we reached (nx, ny)
                    heapq.heappush(pq, (self.heuristic(nx, ny), (nx, ny)))
        return -1, []

   # A* Search 
    def a_star_search(self):
      
        if self.grid[0][0] == 1 or self.grid[self.n - 1][self.n - 1] == 1:
            return -1, []
        pq = []  # priority queue (min-heap)
        heapq.heappush(pq, (self.heuristic(0, 0), 0, (0, 0)))
        parent = {(0, 0): None}   
        g_score = {(0, 0): 0}     
        visited = set()          
        while pq:
            f, g, (x, y) = heapq.heappop(pq)  
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) == (self.n - 1, self.n - 1):  
                return self.reconstruct_path(parent, (x, y))
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny):
                    new_g = g + 1 
                    if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                        g_score[(nx, ny)] = new_g
                        f_score = new_g + self.heuristic(nx, ny)   #f(n)=g(n)+h(n) is  heuristic
                        parent[(nx, ny)] = (x, y)
                        heapq.heappush(pq, (f_score, new_g, (nx, ny)))

        return -1, []
    def reconstruct_path(self, parent, end):
        path = []              
        while end is not None: 
            path.append(end)
            end = parent[end]  
        path.reverse()           
        return len(path), path
    
if __name__ == "__main__":
   grids = [
    [[0, 1],
     [1, 0]],

    [[0, 0, 0],
     [1, 1, 0],
     [1, 1, 0]],

    [[1, 0, 0],
     [1, 1, 0],
     [1, 1, 0]],

]
   for grid in grids:
        print("for the binary matrix grid:", grid)
        pf =FindPath(grid)
        path_length, path_bfs = pf.best_first_search()
        print("Best First Search:Path length:", path_length, "Path:", path_bfs)
        path_len, path_astar = pf.a_star_search()
        print("A* Search :Path length:", path_len, "Path:", path_astar)

        print()

