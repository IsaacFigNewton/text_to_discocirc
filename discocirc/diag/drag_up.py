from discopy import monoidal
from discopy.utils import AxiomError

def swap_right(diagram, i):
    left, box, right = diagram.layers[i]
    if box.dom:
        raise ValueError(f"{box} is not a word.")
    new_left, new_right = left @ right[:1], right[1:]
    new_layer = monoidal.Id(new_left) @ box @ monoidal.Id(new_right)
    swaps = monoidal.Id(left) @ monoidal.Diagram.swap(right[:1], box.cod) @ monoidal.Id(right[1:])
    new_layer = new_layer >> swaps
    return diagram[:i] >> new_layer >> diagram[i+1:]


def drag_out(diagram, i, stop):
    while i > stop:
        try:
            diagram = diagram.interchange(i-1, i)
            i -= 1
        except AxiomError:
            diagram = swap_right(diagram, i)
    return diagram


def drag_all(diagram):
    """
    takes in a circuit (discopy diagram), and 'drags all the nouns to the top'
    """
    i = len(diagram) - 1
    stop = 0
    while i >= stop:
        box = diagram.boxes[i]
        if not box.dom:  # is word
            diagram = drag_out(diagram, i, stop)
            i = len(diagram)
            stop += 1
        i -= 1
    return diagram
