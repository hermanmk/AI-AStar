# coding=UTF-8
import Util as U  # Provides the Square class, A* algorithm methods and helper methods
__author__ = 'Øyvind & Herman'


def a_star_with_bfs(board_name):
    """
    The core of the A* algorithm with the agenda loop and main conditionals
    This implementation has been altered by not sorting the list of open nodes
    Thus this version of A* is using Breadth First Search
    """
    #  Initializing the board through reading the file
    init = U.read_from_file(board_name)  # Returns a list containing the full board, start and goal square
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
        U.draw_closed(node.x, node.y)
        print(node)
        if node == goal_sq:  # We have arrived at the solution
            U.handle_solution(node, start_sq)
            break
        for n in neighbors:
            # Make sure the neighbor is a valid square on the board
            if len(board) > (node.y + n[0]) >= 0 and len(board[node.y]) > (node.x + n[1]) >= 0:
                child = board[node.y + n[0]][node.x + n[1]]
                if child.value != '#':  # Checking if the node is an obstacle, and thus not accessible
                    node.add_child(child)
                    if child not in closed and child not in open_nodes:  # We have not yet generated this node
                        U.attach_and_eval(child, node, goal_sq)
                        open_nodes.insert(0, child)
                        U.draw_open(child.x, child.y)
                    elif node.g + child.get_arc_cost() < child.g:  # Found a cheaper path to this node, thus a better parent
                        U.attach_and_eval(child, node, goal_sq)  # Recalculate the costs for the node
                        if child in closed:  # If the node was already visited, make sure the children are also updated
                            U.propagate_path_improvements(child)
        #  SORTING OF open_nodes IS OMITTED BECAUSE THIS IMPLEMENTATION OF A* USES BFS


#a_star_with_bfs('board-2-4')


def a_star_with_dijkstra(board_name):
    """
    The core of the A* algorithm with the agenda loop and main conditionals
    This implementation has been altered by sorting the list of open nodes by the g-function instead of the f-function
    Thus this version of A* is using Dijkstra's algorithm
    """
    #  Initializing the board through reading the file
    init = U.read_from_file(board_name)  # Returns a list containing the full board, start and goal square
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
        U.draw_closed(node.x, node.y)
        print(node)
        if node == goal_sq:  # We have arrived at the solution
            U.handle_solution(node, start_sq)
            break
        for n in neighbors:
            # Make sure the neighbor is a valid square on the board
            if len(board) > (node.y + n[0]) >= 0 and len(board[node.y]) > (node.x + n[1]) >= 0:
                child = board[node.y + n[0]][node.x + n[1]]
                if child.value != '#':  # Checking if the node is an obstacle, and thus not accessible
                    node.add_child(child)
                    if child not in closed and child not in open_nodes:  # We have not yet generated this node
                        U.attach_and_eval(child, node, goal_sq)
                        open_nodes.append(child)
                        U.draw_open(child.x, child.y)
                    elif node.g + child.get_arc_cost() < child.g:  # Found a cheaper path to this node, thus a better parent
                        U.attach_and_eval(child, node, goal_sq)  # Recalculate the costs for the node
                        if child in closed:  # If the node was already visited, make sure the children are also updated
                            U.propagate_path_improvements(child)
        #  Sort the open_nodes list in descending order based on the g-function instead of the f-function
        open_nodes.sort(key=lambda s: s.g, reverse=True)

a_star_with_dijkstra('board-2-4')
