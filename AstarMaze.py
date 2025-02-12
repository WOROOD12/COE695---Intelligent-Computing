import sys
import heapq  # مكتبة نستفيد منها للـ Priority Queue
from PIL import Image, ImageDraw

# كلاس يمثل كل عقدة في الخوارزمية
class Node():
    def __init__(self, state, parent, action, cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def total_cost(self):
        return self.cost + self.heuristic

# كلاس للـ Priority Queue عشان نستخدمها مع A*
class PriorityQueue():
    def __init__(self):
        self.elements = []

    def add(self, node):
        heapq.heappush(self.elements, (node.total_cost(), node))

    def empty(self):
        return len(self.elements) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return heapq.heappop(self.elements)[1]

class Maze():
    def __init__(self, filename):
        # نقرأ الملف ونحدد ارتفاع وعرض المتاهة
        with open(filename) as f:
            contents = f.read()

        # نتأكد إن فيه نقطة بداية ونقطة نهاية
        if contents.count("A") != 1:
            raise Exception("المتاهة لازم يكون فيها نقطة بداية وحدة")
        if contents.count("B") != 1:
            raise Exception("المتاهة لازم يكون فيها نقطة نهاية وحدة")

        # نحدد ارتفاع وعرض المتاهة
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # نحدد أماكن الجدران ونخزنها
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

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
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

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def heuristic(self, state):
        # نحسب المسافة بين النقطة الحالية والهدف (Manhattan Distance)
        row1, col1 = state
        row2, col2 = self.goal
        return abs(row1 - row2) + abs(col1 - col2)

    def solve(self):
        # نحسب الحل باستخدام A*
        self.num_explored = 0

        # البداية
        start = Node(state=self.start, parent=None, action=None, cost=0, heuristic=self.heuristic(self.start))
        frontier = PriorityQueue()
        frontier.add(start)

        # مجموعة تخزن النقاط اللي زرناها
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("ما فيه حل")

            # نختار النقطة الأقل تكلفة
            node = frontier.remove()
            self.num_explored += 1

            # إذا وصلنا الهدف، نرجع الحل
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # نضيف النقطة الحالية إلى النقاط اللي زرناها
            self.explored.add(node.state)

            # نضيف الجيران إلى الـ Frontier
            for action, state in self.neighbors(node.state):
                if state not in self.explored:
                    child = Node(
                        state=state,
                        parent=node,
                        action=action,
                        cost=node.cost + 1,
                        heuristic=self.heuristic(state)
                    )
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        # إنشاء صورة فارغة
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # الجدران
                if col:
                    fill = (40, 40, 40)

                # البداية
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # الهدف
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # الحل
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # المستكشف
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # خلية فارغة
                else:
                    fill = (237, 240, 252)

                # نرسم الخلية
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze_astar.png", show_explored=True)
