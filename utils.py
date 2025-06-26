from requests import post
from re import search
from py_fumen import decode

from blockfish import AI, Snapshot
import sim

QUEUE_LEN = 5

rot_to_code = {
    "spawn": 0,
    "right": 1,
    "reverse": 2,
    "left": 3
}

async def code_to_json(replay_code):
    pages = decode(code_to_fumen(replay_code))
    turn_count = len(pages)
    if turn_count == 0:
        raise Exception("No pages found in fumen")

    json_out = {
        "accuracy": -1,
        "turn_count": turn_count,
        "turns": []
    }
    acc_sum = 0

    ai = AI()
    await ai.start()

    for page in pages[:2]:
        turn = await gen_turn(page, ai)
        if turn["paths"][0]["score"] == turn["paths"][turn["path_taken"]]["score"]:
            acc_sum += 1
        json_out["turns"].append(turn)

    await ai.shutdown()
    json_out["accuracy"] = acc_sum / turn_count
    return json_out

async def gen_turn(page, ai):
    fumen_field, hold, queue, placement = page_to_state(page)
    turn = {
        "path_taken": -1,
        "path_count": -1,
        "paths": []
    }

    snapshot = Snapshot(hold=hold, queue=queue, matrix=fumen_field)
    suggestions, stats = await ai.analyze(snapshot)
    nodes, iterations, time = stats

    for i, suggestion in enumerate(suggestions):
        first_placement, path = gen_path(suggestion, fumen_field, hold, queue)
        if first_placement == placement:
            turn["path_taken"] = i
        turn["paths"].append(path)

    # if no suggested path was taken
    turn["path_count"] = len(suggestions)
    if turn["path_taken"] == -1:
        turn["path_taken"] = turn["path_count"]
        did_hold = queue[0] == placement[0]
        turn["paths"].append({
            "score": 1000000,
            "page_count": 1,
            "pages": [{ #! todo
                "active": placement[1],
                "hold": queue[0] if did_hold else hold,
                "hold_available": not did_hold,
                "queue": hold + queue[1:] if hold else queue[1:],
                "rows": glue_ghost(fumen_field.copy(), placement)
            }]
        })
    return turn

def glue_ghost(fumen_field, placement):
    block, rot, x, y = placement
    mino_offsets = sim.BLOCK_SHAPES[rot][block]
    for x_off, y_off in mino_offsets:
        nx, ny = x + x_off, y + y_off
        row = list(fumen_field[ny])
        row[nx] = 'a'
        fumen_field[ny] = "".join(row)
    # pad with empty lines
    for _ in range(25 - len(fumen_field)):
        fumen_field.append("___________")
    return fumen_field[::-1]

def gen_path(suggestion, fumen_field, hold, queue):
    rating, inputs = suggestion
    path = {
        "piece_loc": "",
        "score": rating,
        "page_count": inputs.count("hd"),
        "pages" : []
    }
    tetsim = sim.TetSim(fumen_field, queue[0], hold, queue[1:])
    first_placement, piece_loc, pages = tetsim.export_pages(fumen_field, queue[0], hold, queue[1:], inputs)
    path["pages"] = pages
    path["piece_loc"] = piece_loc
    return first_placement, path

def code_to_fumen(replay_code):
    response = post("https://fumen.tstman.net/jstris",
                    data = {"replay": replay_code})
    return(response.json()['fumen'])

# (field, hold, queue, placement)
def page_to_state(page):
    queue_raw = page.comment
    queue_search = search(r'#Q=\[(.?)\]\((.?)\)(.*)', queue_raw)
    if queue_search:
        hold = queue_search.group(1)
        if hold == '':
            hold = None
        current = queue_search.group(2)
        queue = queue_search.group(3)
    else:
        raise Exception("Failed to parse queue from fumen comment")
    field = page.get_field().string().replace('X', 'G')
    field = field.split('\n')
    field.pop()
    field = field[::-1]
    op = page.operation
    op_piece = op.piece_type
    op_rot = rot_to_code[op.rotation]
    op_x, op_y = fumen_coords(op)
    return (field, hold, current + queue[:QUEUE_LEN], (op_piece, op_rot, op_x, op_y))

# FUMEN_COORDS_OFFSET[PIECE][ROTATION]
FUMEN_COORDS_OFFSET = {
    'I': [(1, 0), (0, 2), (2, 0), (0, 1)],
    'J': [(1, 0), (0, 1), (1, 1), (1, 1)],
    'L': [(1, 0), (0, 1), (1, 1), (1, 1)],
    'O': [(0, 0), (0, 1), (1, 1), (1, 0)],
    'S': [(1, 0), (0, 1), (1, 1), (1, 1)],
    'T': [(1, 0), (0, 1), (1, 1), (1, 1)],
    'Z': [(1, 0), (0, 1), (1, 1), (1, 1)]
}
def fumen_coords(op):
    offset = FUMEN_COORDS_OFFSET[op.piece_type][rot_to_code[op.rotation]]
    return (op.x - offset[0], op.y - offset[1])
