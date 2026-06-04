# 🏛️ Temple Trap Puzzle Solver

An intelligent **Temple Trap Puzzle Solver** built using the **A-Star Search Algorithm** to automatically find the **optimal sequence of tile slides and pawn movements** required for escaping the temple.

This project models the **Temple Trap logic puzzle** as a **state-space search problem**, applying concepts from **Artificial Intelligence**, **heuristic search**, and **graph traversal**.

---

## 📌 Project Overview

Temple Trap is a challenging sliding puzzle game where a pawn must escape through a maze formed by movable tiles.

The puzzle contains:

* A **3×3 board**
* **8 movable tiles**
* **1 blank cell**
* **2 vertical layers** (Ground & Top)
* **Special stair tiles**
* **Sliding mechanics with movement constraints**

This solver automatically computes the **minimum-cost solution** using **A*** search.


---

## 🧩 Puzzle Rules

### 1. Board Structure

The board consists of a **3×3 grid**:

```text
0 1 2
3 4 5
6 7 8
```

One cell is always empty (**blank tile**).

---

### 2. Two Layers

The puzzle contains two movement layers:

* **Ground Layer**
* **Top Layer**

The pawn may switch layers **only through stair tiles (D & E)**.

---

### 3. Tile Connectivity

Movement is allowed only when adjacent tiles have matching openings.

#### Horizontal Connection

* Left tile → Side II open
* Right tile → Side IV open

#### Vertical Connection

* Upper tile → Side III open
* Lower tile → Side I open

---

### 4. Lock Rule

A tile **cannot be moved** if the pawn is currently standing on it.

---

### 5. Goal Condition

The puzzle is solved when:

1. The pawn reaches **Cell 0**
2. The tile at Cell 0 is open on **Side IV (left boundary)**
3. The pawn exits the temple successfully

---

## 🧠Approach

This project models the puzzle as a **State Space Search Problem**.

### State Representation

Each state is represented as:

```math
s = (p, l, b, T)
```

Where:

* **p** → Pawn position
* **l** → Pawn layer (Ground/Top)
* **b** → Blank tile position
* **T** → Current board configuration

The state is implemented using a custom `State` class containing:

* Pawn Position
* Pawn Level
* Puzzle Configuration
* Blank Position
* Parent State
* Action Taken
* `g(n)` → Actual Cost
* `f(n)` → Total Cost

---

## 🔍 Search Algorithm

The solver uses the **A-Star Search Algorithm**.

### Why A*?

A* guarantees:

* **Optimal solutions**
* **Efficient search**
* **Heuristic-guided exploration**

The total evaluation function:

```math
f(n) = g(n) + h(n)
```

Where:

* `g(n)` → Actual cost from start state
* `h(n)` → Heuristic estimate to goal

---

## 📏 Heuristic Function

The heuristic combines:

### 1. Manhattan Distance

Distance from pawn to exit cell:

```math
|x_p - x_0| + |y_p - y_0|
```

### 2. Exit Penalty

Additional penalty is added when the exit tile is not correctly oriented.

This improves search efficiency while preserving solution quality.

---

## ⚙️ Project Structure

```text
Temple-Trap-Solver/
│── main.py
│── REPORT.docx
│── problem statement.pdf
│── README.md
```

### File Descriptions

| File                    | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `main.py`               | Complete implementation of Temple Trap Solver    |
| `REPORT.docx`           | Explanation of algorithms, heuristic, and design |
| `problem statement.pdf` | Puzzle definition and assignment description     |
| `README.md`             | Project documentation                            |

---

## 🧱 Tile Definitions

The game contains **8 unique tiles (A–H)**.

### Top Layer Tiles

| Tile | Description                  |
| ---- | ---------------------------- |
| A    | Top openings on Side I & II  |
| B    | Top openings on Side I & II  |
| C    | Top openings on Side II & IV |

### Stair Tiles

| Tile | Description                 |
| ---- | --------------------------- |
| D    | Stairs between Ground ↔ Top |
| E    | Stairs between Ground ↔ Top |

### Ground Layer Tiles

| Tile | Description                    |
| ---- | ------------------------------ |
| F    | Ground openings on Side I & II |
| G    | Ground openings on Side I & II |
| H    | Ground openings on Side I & II |

---

## 🔄 State Expansion

The solver generates neighbors using:

### 1. Tile Sliding

The blank tile is moved in all valid directions.

Restrictions:

* Cannot move the tile containing the pawn
* Only valid board positions allowed

---

### 2. Pawn Movement

The pawn traverses:

* Ground layer paths
* Top layer paths
* Stair transitions

Implemented using **Breadth First Search (BFS)** to find reachable locations.

---

## 📚 Supported Levels

The solver currently supports multiple levels:

### Starter

* starter-1
* starter-2
* starter-3
* starter-4

### Junior

* junior-1
* junior-2
* junior-3
* junior-4

### Expert

* expert-1
* expert-2
* expert-3
* expert-4

### Master

* master-1
* master-2

Custom puzzle IDs:

* `43`
* `55`

To change the puzzle level:

```python
puzzle_level = '55'
```

Replace `'55'` with:

```python
'starter-1'
'junior-4'
'expert-2'
'master-1'
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/balasiva2006/TEMPLE-TRAP-GAME-SOLUTION-.git
```

### Navigate to Project

```bash
cd TEMPLE-TRAP-GAME-SOLUTION-
```

### Run the Solver

```bash
python main.py
```

---

## 🖥️ Example Output

The solver prints:

* Total Cost
* Configuration Steps
* Exit Steps
* Pawn Position
* Board Configuration
* Final Escape Path

Example:

```text
SOLUTION FOUND!

Step 1:
Action: Slide 'C' from cell 7 to cell 6

Step 2:
Action: Walk from cell 5 to 2

...

GOAL REACHED!
Pawn has successfully escaped the temple!
```

---

## 🛠️ Technologies Used

* **Python**
* **A* Search**
* **Breadth First Search (BFS)**
* **Heap Queue (Priority Queue)**
* **Object-Oriented Programming**

---

## 📖 Concepts Used

This project demonstrates concepts of:

* Artificial Intelligence
* State Space Search
* Heuristic Search
* Graph Traversal
* Pathfinding
* BFS
* A* Search
* Object-Oriented Design

---

## 🎓 Academic Context

This project was developed as part of an **AI/Search Problem formulation assignment**, where the Temple Trap puzzle was modeled as a formal search problem and solved using optimal search techniques.

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve:

* Heuristics
* Performance
* Additional puzzle levels
* UI visualization

Feel free to fork the repository and create a pull request.


---

## 👨‍💻 Author

**Perneedi Bala Siva Satyanarayana**

GitHub:
https://github.com/balasiva2006
