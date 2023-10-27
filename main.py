import time


class Node():
    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state
        self.collisions = [0, 0, 0, 0, 0, 0, 0, 0]
        self.h = 0

    def __eq__(self, other):
        return self.state == other.state


def astar(start):
    start_node = Node(None, start)
    start_node.h = heuristic(start, start_node.collisions)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    start_time = time.time()
    max_execution_time = 60  # Обмеження на час виконання програми (60 секунд).

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        # Перевірка часу виконання
        if (time.time() - start_time) > max_execution_time:
            print("Час виконання перевищив обмеження.")
            return None
        for index, item in enumerate(open_list):
            if item.h < current_node.h:
                current_node = item
                current_index = index
            elif item.h > current_node.h + 2:
                open_list.remove(item)

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node.h == 0:
            print("Результат розташування: ", current_node.state)
            print((time.time() - start_time), "seconds")
            return current_node.state

        children = []
        for collisioned in range(0, 8):
            if current_node.collisions[collisioned]:
                for new_state in [1, 2, 3, 4, 5, 6, 7]:
                    new_node = Node(current_node, current_node.state.copy())

                    new_node.state[collisioned] = (new_node.state[collisioned] + new_state) % 8

                    children.append(new_node)
        for child in children:

            skip = False
            for closed_child in closed_list:
                if child == closed_child:
                    skip = True
            if skip: continue

            child.h = heuristic(child.state, child.collisions)

            for open_node in open_list:
                if child == open_node and child.h >= open_node.h:
                    skip = True
            if skip: continue

            open_list.append(child)


def heuristic(state, collisions):
    h = 0
    rowLock = -1
    upperDiagLock = -1
    lowerDiagLock = -1
    for i in range(0, 8):
        for j in range(i + 1, 8):
            if state[i] == state[j] and rowLock != i:
                rowLock = i
                collisions[i] = collisions[j] = 1
                h += 1
            elif state[i] - state[j] == i - j and upperDiagLock != i:
                upperDiagLock = i
                collisions[i] = collisions[j] = 1
                h += 1
            elif state[i] - state[j] == - (i - j) and lowerDiagLock != i:
                lowerDiagLock = i
                collisions[i] = collisions[j] = 1
                h += 1
    return h


def main():
    # statring state:
    start = [0, 0, 0, 0, 0, 0, 0, 0]
    print("Початкове розташування: ", start)
    result = astar(start)


if __name__ == '__main__':
    main()
