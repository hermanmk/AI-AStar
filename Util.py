# coding=UTF-8
from turtle import *

__author__ = 'Øyvind & Herman'

# Dictionary with the different arc costs based on the square's value
terrains = {'.': 1, 'w': 100, 'm': 50, 'f': 10, 'g': 5, 'r': 1, 'A': 1, 'B': 1}
# Dictionary with terrain colors for the graphics
colors = {'.': '#ffffff', '#': '#000000', 'w': '#3f51b5', 'm': '#9e9e9e',
          'f': '#4caf50', 'g': '#8bc34a', 'r': '#795548', 'A': '#ff0000', 'B': '#00ff00'}

# Initial position and speed of the pencil
speed(0)
penup()
setpos(-500, 200)
pendown()
screensize(1000, 1000)


class Square:
    """
    Class representing a single square on the board, also referenced as a "node"
    """

    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.h = -1
        self.g = 0
        self.f = 0
        self.children = []
        self.parent = None

    def __pos__(self):
        return self.x, self.y

    def __str__(self):
        return self.value + '(' + str(self.x) + ', ' + str(self.y) + ')'

    def heuristic(self, other_sq):
        self.h = abs(self.x - other_sq.x) + abs(self.y - other_sq.y)

    def get_arc_cost(self):
        return terrains[self.value]

    def calculate_f(self):
        self.f = self.g + self.h

    def add_child(self, child):
        if not self.has_child(child):
            self.children.append(child)

    def has_child(self, child):
        return child in self.children

    def set_parent(self, parent):
        self.parent = parent

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def read_from_file(file):
    board = []
    start = -1
    goal = -1
    with open('boards/' + file + '.txt', 'r') as f:
        y = 0
        for line in f:
            x = 0
            row = []
            for char in line.strip():
                row.append(Square(char, x, y))
                if char == 'A':
                    start = Square(char, x, y)
                elif char == 'B':
                    goal = Square(char, x, y)
                x += 1
                fillcolor(colors[char])
                # Draws a square for each node in the board with a color based on node type
                begin_fill()
                for i in range(4):
                    forward(30)
                    left(90)
                end_fill()
                forward(30)
            board.append(row)
            y += 1
            penup()
            # Go back to start position for x and the new y position for the next row to be drawn
            goto(-500, ycor() - 30)
            pendown()

    return [board, start, goal]


def print_list(l):
    for n in l:
        print(str(n.f) + ' - ' + str(n))


def draw_best_route(final_route):
    """
    Draws the optimal route/path AFTER the algorithm has found it
    """
    shape('turtle')
    fillcolor('purple')
    pencolor('purple')
    pensize(4)
    speed(1)
    # Finds the start position of the node in the graphical grid
    start_pos_x = (final_route[0].x) * 30
    start_pos_y = (final_route[0].y - 1) * -30
    penup()
    # Sets the start position of the drawn path in the middle of the start node
    setpos(-500 + start_pos_x + 15, 200 + start_pos_y - 15)
    pendown()
    # Draws right, left, down or up based on the position of the next node in the list
    for i in range(0, len(final_route) - 1):
        if final_route[i].x < final_route[i + 1].x:
            goto(xcor() + 30, ycor())
        elif final_route[i].x > final_route[i + 1].x:
            goto(xcor() - 30, ycor())
        elif final_route[i].y < final_route[i + 1].y:
            goto(xcor(), ycor() - 30)
        else:
            goto(xcor(), ycor() + 30)
    done()


def draw_closed(x, y):
    """
    Draws the recently closed (visited) node
    """
    square_pos_x = x * 30
    square_pos_y = (y - 1) * -30
    penup()
    # Sets the position on the position (15, 25) in the square of size (30,30) and draws a filled circle
    setpos(-500 + square_pos_x + 15, 200 + square_pos_y - 25)
    pendown()
    fillcolor('#ff9800')
    begin_fill()
    circle(10)
    end_fill()


def draw_open(x, y):
    """
    Draws the newly opened (discovered) node
    """
    square_pos_x = x * 30
    square_pos_y = (y - 1) * -30
    penup()
    pencolor('#ff9800')
    # Sets the position on the position (15, 25) in the square of size (30,30) and draws a filled circle
    setpos(-500 + square_pos_x + 15, 200 + square_pos_y - 25)
    pendown()
    circle(10)


def attach_and_eval(node, parent, goal):
    """
    Part of the A* algorithm. Sets the parent of the node and calculates the g-, h- and f-function
    """
    node.set_parent(parent)
    node.g = parent.g + node.get_arc_cost()
    node.heuristic(goal)
    node.f = node.g + node.h


def propagate_path_improvements(parent):
    """
    When a cheaper path to a node is found, this method recursively updates all its children
    """
    for child in parent.children:
        if parent.g + 1 < child.g:
            child.set_parent(parent)
            child.g = parent.g + child.get_arc_cost()
            child.f = child.g + child.h
            # Recursive call to propagate possible path improvements to all children of the children
            propagate_path_improvements(child)


def handle_solution(node, start_sq):
    """
    Backtracks all the nodes of the optimal path and prints them chronologically
    """
    final_route = []
    while True:  # Find the best path by backtracking through all the parents, starting with the goal node
        final_route.insert(0, node)
        if node == start_sq:
            break
        node = node.parent
    print('Best path from A to B:')
    print_list(final_route)
    draw_best_route(final_route)


def a_star(board_name, draw_real_time):
    """
    The core of the A* algorithm with the agenda loop and main conditionals
    """
    #  Initializing the board through reading the file
    init = read_from_file(board_name)  # Returns a list containing the full board, start and goal square
    board = init[0]
    start_sq = init[1]
    goal_sq = init[2]
    open_nodes = []
    closed = []
    start_sq.heuristic(goal_sq)
    start_sq.f = start_sq.g + start_sq.h
    open_nodes.append(start_sq)
    neighbors = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    while open_nodes:
        node = open_nodes.pop()
        closed.append(node)
        if draw_real_time:
            draw_closed(node.x, node.y)
        print(node)
        if node == goal_sq:  # We have arrived at the solution
            handle_solution(node, start_sq)
            break
        for n in neighbors:
            # Make sure the neighbor is a valid square on the board
            if len(board) > (node.y + n[0]) >= 0 and len(board[node.y]) > (node.x + n[1]) >= 0:
                child = board[node.y + n[0]][node.x + n[1]]
                if child.value != '#':  # Checking if the node is an obstacle, and thus not accessible
                    node.add_child(child)
                    if child not in closed and child not in open_nodes:  # We have not yet generated this node
                        attach_and_eval(child, node, goal_sq)
                        open_nodes.append(child)
                        if draw_real_time:
                            draw_open(child.x, child.y)
                    elif node.g + child.get_arc_cost() < child.g:  # Found a cheaper path to this node, thus a better parent
                        attach_and_eval(child, node, goal_sq)  # Recalculate the costs for the node
                        if child in closed:  # If the node was already visited, make sure the children are also updated
                            propagate_path_improvements(child)
        #  Sort the open_nodes list in descending order based on the f-function, so that pop gets the least costly node
        open_nodes.sort(key=lambda s: s.f, reverse=True)
