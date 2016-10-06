# coding=UTF-8
__author__ = 'Øyvind & Herman'


class Square:

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
            board.append(row)
            y += 1
    return [board, start, goal]


def print_list(l):
    for n in l:
        print(str(n.f) + ' - ' + str(n))


def attach_and_eval(node, parent, goal):
    node.set_parent(parent)
    node.g = parent.g + 1
    node.heuristic(goal)
    node.f = node.g + node.h


def propagate_path_improvements(parent):
    for child in parent.children:
        if parent.g + 1 < child.g:
            child.set_parent(parent)
            child.g = parent.g + 1
            child.f = child.g + child.h
            # Recursive call to propagate possible path improvements to all children of the children
            propagate_path_improvements(child)


def a_star(board_name):
    init = read_from_file(board_name)
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
        print(node)
        if node == goal_sq:  # We have arrived at the solution
            final_route = []
            while True:  # Find the best path by backtracking through all the parents, starting with the goal node
                final_route.insert(0, node)
                if node == start_sq:
                    break
                node = node.parent
            print('Best path from A to B:')
            print_list(final_route)
            break
        for n in neighbors:
            if len(board) > (node.y + n[0]) >= 0 and len(board[node.y]) > (node.x + n[1]) >= 0:
                child = board[node.y + n[0]][node.x + n[1]]
                if child.value != '#':
                    node.add_child(child)
                    if child not in closed and child not in open_nodes:  # We have not yet generated this node
                        attach_and_eval(child, node, goal_sq)
                        open_nodes.append(child)
                    elif node.g + 1 < child.g:  # Found a cheaper path to this node, thus a better parent
                        attach_and_eval(child, node, goal_sq)
                        if child in closed:
                            propagate_path_improvements(child)
        open_nodes.sort(key=lambda s: s.f, reverse=True)
        if not node.has_child(open_nodes[len(open_nodes) - 1]):
            print('next node is not a neighbor!')

a_star('board-1-3')
