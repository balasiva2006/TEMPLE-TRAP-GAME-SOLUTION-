```latex
\documentclass[a4paper,11pt]{article}

\usepackage[a4paper,margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{listings}
\usepackage{xcolor}

\title{\textbf{Temple Trap Puzzle Solver}}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

\section{Project Overview}

This project implements an \textbf{Temple Trap Puzzle Solver} using the 
\textbf{A* Search Algorithm}. The objective of the puzzle is to guide a pawn 
through a dynamic temple environment by sliding tiles and moving strategically 
until the pawn reaches the exit.

The implementation models the puzzle as a \textbf{state-space search problem}, 
where every valid board configuration represents a unique state. The solver 
searches for an optimal sequence of actions with minimum total cost.

\section{Features}

\begin{itemize}
    \item Implements the \textbf{A* Search Algorithm} for optimal pathfinding.
    \item Supports \textbf{multiple puzzle levels}.
    \item Models both:
    \begin{itemize}
        \item \textbf{Tile movement} (sliding tiles)
        \item \textbf{Pawn movement} (walking across connected paths)
    \end{itemize}
    \item Handles:
    \begin{itemize}
        \item Ground and top floor navigation
        \item Stair transitions
        \item Tile orientations
        \item Reachability checking
    \end{itemize}
    \item Uses a \textbf{heuristic function} to improve search efficiency.
    \item Produces a detailed step-by-step solution path.
\end{itemize}

\section{Problem Formulation}

The puzzle is represented as a \textbf{3 × 3 board} consisting of:

\begin{itemize}
    \item 8 unique temple tiles (A--H)
    \item 1 blank cell
    \item A pawn that moves across valid paths
\end{itemize}

The pawn can move between tiles if the corresponding sides are connected. 
Movement can happen on:

\begin{itemize}
    \item \textbf{Ground Layer}
    \item \textbf{Top Layer}
\end{itemize}

Some tiles contain \textbf{stairs}, allowing transitions between layers.

The goal is to guide the pawn to the exit at cell 0 with a valid opening toward 
the left boundary.

\section{State Representation}

Each puzzle configuration is represented using a \texttt{State} class containing:

\begin{itemize}
    \item Puzzle configuration
    \item Pawn position
    \item Pawn level (Ground / Top)
    \item Blank tile position
    \item Parent state
    \item Action taken
    \item Path cost ($g$)
    \item Evaluation cost ($f = g + h$)
\end{itemize}

\section{Heuristic Function}

The heuristic estimates the cost to reach the exit using:

\[
h(S) = r_p + c_p +
\begin{cases}
2, & \text{if exit is not immediately accessible} \\
0, & \text{otherwise}
\end{cases}
\]

where:

\begin{itemize}
    \item $r_p$ = row index of pawn
    \item $c_p$ = column index of pawn
\end{itemize}

This helps A* prioritize states closer to the exit.

\section{Algorithms Used}

\subsection{A* Search}

The A* algorithm is used to explore possible puzzle configurations while minimizing:

\[
f(n) = g(n) + h(n)
\]

where:

\begin{itemize}
    \item $g(n)$ = actual cost from start
    \item $h(n)$ = estimated remaining cost
\end{itemize}

\subsection{Breadth First Search (BFS)}

BFS is internally used for:

\begin{itemize}
    \item Pawn movement exploration
    \item Exit reachability checking
    \item Valid movement generation
\end{itemize}

\section{Project Structure}

\begin{lstlisting}[language=Python]
project/
│── main.py
│── REPORT.docx
│── problem statement.pdf
│── README.tex
\end{lstlisting}

\section{How to Run}

\subsection{Requirements}

Install Python 3.x.

\subsection{Run the Solver}

Execute:

\begin{lstlisting}[language=bash]
python main.py
\end{lstlisting}

To test a different puzzle level, modify:

\begin{lstlisting}[language=Python]
puzzle_level = '55'
\end{lstlisting}

inside \texttt{main.py}.

\section{Example Output}

The solver generates:

\begin{itemize}
    \item Step-by-step moves
    \item Tile slides
    \item Pawn transitions
    \item Total path cost
    \item Final exit path
\end{itemize}

\section{Applications}

This project demonstrates concepts in:

\begin{itemize}
    \item Artificial Intelligence
    \item Search Algorithms
    \item State Space Representation
    \item Heuristic Optimization
    \item Graph Traversal
\end{itemize}

\section{Future Improvements}

\begin{itemize}
    \item Add graphical visualization
    \item Support larger puzzle sizes
    \item Improve heuristic accuracy
    \item Add interactive gameplay
\end{itemize}

\section{References}

\begin{itemize}
    \item Temple Trap Puzzle Problem Statement
    \item A* Search Algorithm
    \item Artificial Intelligence Search Problems
\end{itemize}

\end{document}
```
