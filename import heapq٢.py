import heapq
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# دالة لإنشاء متاهة بحجم معين مع نسبة مئوية للعوائق، وضمان وجود مسار مفتوح
def generate_maze(size, obstacle_prob=0.3):
    while True:
        maze = [[0 if random.random() > obstacle_prob else 1 for _ in range(size)] for _ in range(size)]
        maze[0][0] = 0  # نقطة البداية
        maze[size-1][size-1] = 0  # نقطة الهدف
        if is_solvable(maze, size):
            return maze

# التحقق مما إذا كانت المتاهة قابلة للحل
def is_solvable(maze, size):
    from collections import deque
    queue = deque([(0, 0)])
    visited = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) == (size-1, size-1):
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False

# دالة حساب مسافة مانهاتن بين نقطتين

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# دالة حساب المسافة الإقليدية بين نقطتين
def euclidean_distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

# خوارزمية البحث A*
def a_star_search(maze, heuristic):
    rows, cols = len(maze), len(maze[0])
    start, goal = (0, 0), (rows - 1, cols - 1)
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    nodes_expanded = 0
    start_time = time.time()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        nodes_expanded += 1
        
        if current == goal:
            return nodes_expanded, g_score[current], time.time() - start_time
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return nodes_expanded, float('inf'), time.time() - start_time

# خوارزمية البحث Greedy Best-First Search
def greedy_best_first_search(maze, heuristic):
    rows, cols = len(maze), len(maze[0])
    start, goal = (0, 0), (rows - 1, cols - 1)
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {}
    visited = set([start])
    nodes_expanded = 0
    start_time = time.time()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        nodes_expanded += 1
        
        if current == goal:
            path_cost = 0
            while current in came_from:
                path_cost += 1
                current = came_from[current]
            return nodes_expanded, path_cost, time.time() - start_time
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))
    
    return nodes_expanded, float('inf'), time.time() - start_time

mazes = {30: generate_maze(30), 35: generate_maze(35), 40: generate_maze(40)}
heuristics = {'Manhattan': manhattan_distance, 'Euclidean': euclidean_distance}
algorithms = {'A*': a_star_search, 'Greedy BFS': greedy_best_first_search}

results = []
for size, maze in mazes.items():
    for heuristic_name, heuristic in heuristics.items():
        for algo_name, algo in algorithms.items():
            nodes_expanded, path_cost, exec_time = algo(maze, heuristic)
            results.append([size, algo_name, heuristic_name, nodes_expanded, path_cost, exec_time])

results_df = pd.DataFrame(results, columns=['Maze Size', 'Algorithm', 'Heuristic', 'Nodes Expanded', 'Path Cost', 'Execution Time'])

# تحسين عرض النتائج بصريًا
plt.figure(figsize=(12, 6))
sns.barplot(x='Maze Size', y='Nodes Expanded', hue='Algorithm', data=results_df, palette='coolwarm')
plt.title('Nodes Expanded Comparison per Algorithm and Maze Size')
plt.ylabel('Nodes Expanded')
plt.xlabel('Maze Size')
plt.legend(title='Algorithm')
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(x='Maze Size', y='Execution Time', hue='Algorithm', data=results_df, marker='o', palette='coolwarm')
plt.title('Execution Time per Algorithm and Maze Size')
plt.ylabel('Execution Time (s)')
plt.xlabel('Maze Size')
plt.legend(title='Algorithm')
plt.show()

# طباعة النتائج
print(results_df)
