# Micromouse Maze Simulator with Floodfill Pathfinding (INCOMPLETE)

A Python-based Micromouse simulator that navigates a virtual maze using the **floodfill algorithm**. Built with the `turtle` module for visual simulation and customizable grid logic for wall-following and dynamic maze solving.

---

## Features

- Interactive **18x18 grid-based maze**
- Walls encoded with directional strings (`"n"`, `"e"`, `"s"`, `"w"`)
- Turtle graphics-based visualization
- Floodfill algorithm for live cost-map path planning
- Mouse "senses" surroundings and updates the maze knowledge
- Modular architecture:
  - `maze.py`: grid + wall generation
  - `mouse.py`: visual and logical mouse control
  - `logic.py`: floodfill and decision-making
  - `main.py`: simulation runner

---

## Project Structure

```
micromouse-maze_sim_floodfill/
├── main.py            # Entry point to run the simulator
├── maze.py            # Maze generator and wall utility functions
├── mouse.py           # Visual mouse with heading, movement, and grid drawing
├── logic.py           # FloodFillMap logic (cost map + next move decisions)
└── README.md          # This file
```

---

##  How to Run

1. **Install Python 3.9**
2. Clone this repository:

   ```bash
   git clone https://github.com/your-username/micromouse-maze_sim_floodfill.git
   cd micromouse-maze_sim_floodfill
   ```

3. Run the simulator:

   ```bash
   python main.py
   ```

---

## Controls (Autonomous)

- The mouse starts at the bottom-left (cell `[17, 0]`)
- The goal is top-right (cell `[0, 17]`)
- The mouse reads nearby walls and updates a **floodfill cost map**
- It chooses the next best cell to move toward the goal

---

## Notes

- The maze is generated in `maze.py` with a mix of real paths and false paths
- The mouse maintains internal knowledge and updates its cost map using local wall sensing
- The visual output updates using Python's turtle module, which may run slow on very large updates (for now, it's great for concept visualizations)

---

## To-Do 

- Allow user to draw maze manually with clicks

---