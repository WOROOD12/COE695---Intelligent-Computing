import heapq
import os

# تعريف كلاس العقدة التي تمثل نقطة في المتاهة
class Node():
    def __init__(self, state, parent, action, cost=0, heuristic=0):
        self.state = state  # الحالة الحالية (الموقع في المتاهة)
        self.parent = parent  # العقدة الأصل التي أتت منها هذه العقدة
        self.action = action  # الحركة التي قادت إلى هذه العقدة
        self.cost = cost  # التكلفة للوصول إلى هذه العقدة
        self.heuristic = heuristic  # القيم الإرشادية في خوارزمية A*
    
    def total_cost(self):
        return self.cost + self.heuristic

    # 🔥 الحل: إضافة دالة مقارنة حتى يعرف heapq كيفية ترتيب الكائنات
    def __lt__(self, other):
        return self.total_cost() < other.total_cost()

# كلاس يمثل قائمة الأولويات للبحث باستخدام A* و Dijkstra
class PriorityQueueFrontier():
    def __init__(self):
        self.frontier = []  # قائمة الأولويات باستخدام heapq
        self.states = set()  # مجموعة لحفظ الحالات لمنع التكرار

    def add(self, node):
        heapq.heappush(self.frontier, (node.total_cost(), node))  # إضافة العقدة إلى القائمة مع تحديد الأولوية
        self.states.add(node.state)

    def contains_state(self, state):
        return state in self.states  # التحقق مما إذا كانت الحالة موجودة مسبقًا

    def empty(self):
        return len(self.frontier) == 0  # التحقق مما إذا كانت القائمة فارغة

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        _, node = heapq.heappop(self.frontier)  # إزالة العنصر ذو الأولوية الأعلى (الأقل تكلفة)
        self.states.remove(node.state)
        return node

# كلاس المتاهة لقراءة وتحليل الملف
class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Maze must have exactly one start and one goal")
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution_astar = None
        self.solution_dijkstra = None

    def print(self, solution=None):
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()

    def neighbors(self, state):
        row, col = state
        candidates = [("up", (row - 1, col)), ("down", (row + 1, col)), ("left", (row, col - 1)), ("right", (row, col + 1))]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def solve(self, algorithm):
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None, cost=0, heuristic=self.heuristic(self.start) if algorithm == 'astar' else 0)
        frontier = PriorityQueueFrontier()
        frontier.add(start)
        self.explored = set()
        while not frontier.empty():
            node = frontier.remove()
            self.num_explored += 1
            if node.state == self.goal:
                actions, cells = [], []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                if algorithm == 'astar':
                    self.solution_astar = (actions, cells)
                else:
                    self.solution_dijkstra = (actions, cells)
                return
            self.explored.add(node.state)
            for action, state in self.neighbors(node.state):
                new_cost = node.cost + 1
                heuristic_value = self.heuristic(state) if algorithm == 'astar' else 0
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, cost=new_cost, heuristic=heuristic_value)
                    frontier.add(child)

# تشغيل الكود تلقائيًا على جميع المتاهات
maze_files = ["maze_30x30.txt", "maze_35x35.txt", "maze_40x40.txt"]

for maze_file in maze_files:
    if os.path.exists(maze_file):
        print(f"\n🔹 Processing: {maze_file}")
        m = Maze(maze_file)
        print("📌 Maze Layout:")
        m.print()
        print("🔍 Solving with A*...")
        m.solve("astar")
        print("📊 States Explored (A*):", m.num_explored)
        m.print(m.solution_astar[1])
        print("⚡ Solving with Dijkstra...")
        m.solve("dijkstra")
        print("📊 States Explored (Dijkstra):", m.num_explored)
        m.print(m.solution_dijkstra[1])
    else:
        print(f"❌ Error: File {maze_file} not found.")
