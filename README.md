# COE695---Intelligent-Computing
Heuristic Search Algorithms for Maze Solving
This repository contains the implementation of heuristic-based search algorithms for solving mazes using A Search* and Greedy Best-First Search. The algorithms are evaluated using different heuristics: Manhattan Distance and Euclidean Distance.

📌 How to Run the Code
1️⃣ Clone the Repository

git clone https://github.com/WOROOD12/COE695---Intelligent-Computing.git

cd COE695---Intelligent-Computing

2️⃣ Install Dependencies

Ensure you have Python 3.x installed, then install the required packages:

pip install -r requirements.txt

3️⃣ Run the Program

Execute the script to generate and solve a maze:

python main.py

This will:

Generate random mazes of different sizes (30×30, 35×35, 40×40).

Solve them using A and Greedy BFS*.

Visualize the expanded nodes, path cost, and execution time.

📊 Output Results

Maze Images:

generated_mazes.png → Displays randomly generated mazes.

Performance Graphs:

nodes_expanded_comparison.png → Shows expanded nodes per algorithm.

execution_time_comparison.png → Compares execution time across heuristics.

🔧 Configuration

Modify main.py to customize:

Maze size (default: 30x30, 35x35, 40x40).

Obstacle density (default: 30%).

Algorithm selection (A* or Greedy BFS).

📚 Dependencies

Listed in requirements.txt:

numpy

matplotlib

seaborn

pandas

Install them using:

pip install -r requirements.txt

📜 License

This project is for educational purposes only.

