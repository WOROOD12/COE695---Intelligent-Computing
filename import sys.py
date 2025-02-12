import sys
import heapq
from PIL import Image, ImageDraw

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

# كلاس المتاهة الذي يقوم بقراءة الملف النصي وتحليل البيانات
class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Maze must have exactly one start and one goal")
        contents = contents.splitlines()
        self.height = len(contents)  # تحديد ارتفاع المتاهة
        self.width = max(len(line) for line in contents)  # تحديد عرض المتاهة
        self.walls = []  # مصفوفة الجدران
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)  # تحديد نقطة البداية
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)  # تحديد نقطة الهدف
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)  # المساحات الفارغة (مسموح بالحركة فيها)
                    else:
                        row.append(True)  # الجدران (عائق للحركة)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution_astar = None  # تخزين الحل باستخدام A*
        self.solution_dijkstra = None  # تخزين الحل باستخدام Dijkstra

    # طباعة المتاهة والحل إن وجد
    def print(self, solution=None):
        print()
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
        print()

    # تحديد الجيران الممكنين لكل حالة (الحركات الممكنة)
    def neighbors(self, state):
        row, col = state
        candidates = [("up", (row - 1, col)), ("down", (row + 1, col)), ("left", (row, col - 1)), ("right", (row, col + 1))]
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    # الدالة الإرشادية لخوارزمية A* (المسافة بين الحالة الحالية والهدف باستخدام مانهاتن)
    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    # دالة لحل المتاهة باستخدام A* أو Dijkstra بناءً على اختيار المستخدم
    def solve(self, algorithm):
        self.num_explored = 0  # عدد العقد المستكشفة
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

# التحقق من صحة المدخلات عند تشغيل البرنامج
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

# تنفيذ البرنامج
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving with A*...")
m.solve("astar")
print("States Explored (A*):", m.num_explored)
print("Solution (A*):")
m.print(m.solution_astar[1])
print("Solving with Dijkstra...")
m.solve("dijkstra")
print("States Explored (Dijkstra):", m.num_explored)
print("Solution (Dijkstra):")
m.print(m.solution_dijkstra[1])
