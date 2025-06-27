from requests import post
from re import search
from py_fumen import decode
from time import time_ns
import asyncio

from blockfish import AI, Snapshot
import sim

QUEUE_LEN = 5

rot_to_code = {
    "spawn": 0,
    "right": 1,
    "reverse": 2,
    "left": 3
}

def log(arg="helloe"):
    with open("log.txt", "a") as f:
        f.write(str(time_ns()) + " " + str(arg) + "\n")

async def code_to_json(replay_code, cancel_flag, update_progress):
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

    results = []
    completed = 0

    async def process_page(idx, page):
        nonlocal completed
        if cancel_flag():
            return None
        result = await gen_turn(page, ai)
        completed += 1
        update_progress(completed, turn_count)
        return (idx, result)

    tasks = [process_page(idx, page) for idx, page in enumerate(pages)]
    for coro in asyncio.as_completed(tasks):
        res = await coro
        if res is not None:
            results.append(res)
        if cancel_flag():
            break

    sorted_results = [res for _, res in sorted(results, key=lambda x: x[0])]

    if cancel_flag():
        await ai.shutdown()
        return

    for turn in sorted_results:
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

    # rotation symmetry for IOSZ
    placement_symm = list(placement)
    if placement[0] == "O":
        placement_symm[1] = 0
    elif placement[0] in "ILSZ":
        placement_symm[1] %= 2

    for i, suggestion in enumerate(suggestions):
        first_placement, path = gen_path(suggestion, fumen_field, hold, queue)
        # rotation symmetry for IOSZ
        first_placement_symm = list(first_placement)
        if first_placement[0] == "O":
            first_placement_symm[1] = 0
        elif first_placement[0] in "ILSZ":
            first_placement_symm[1] %= 2

        if first_placement_symm == placement_symm:
            turn["path_taken"] = i
        turn["paths"].append(path)

    # if no suggested path was taken
    turn["path_count"] = len(suggestions)
    if turn["path_taken"] == -1:
        turn["path_taken"] = turn["path_count"]
        did_hold = queue[0] == placement[0]
        width = sim.BLOCK_WIDTHS[placement[1]][placement[0]]
        cols = ''.join(list(map(str, range(placement[2], placement[2] + width))))
        turn["paths"].append({
            "score": "?",
            "page_count": 1,
            "piece_loc": f"{placement[0]}-{cols}",
            "pages": [{
                "active": placement[0],
                "hold": queue[0] if did_hold else hold,
                "hold_available": not did_hold,
                "queue": hold + queue[1:] if did_hold and hold else queue[1:],
                "rows": glue_ghost(fumen_field.copy(), placement)
            }]
        })
        turn["path_count"] += 1

    return turn

def glue_ghost(fumen_field, placement):
    block, rot, x, y = placement
    mino_offsets = sim.BLOCK_SHAPES[rot][block]
    for _ in range(25 - len(fumen_field)):
        fumen_field.append("___________")
    for x_off, y_off in mino_offsets:
        nx, ny = x + x_off, y + y_off
        row = list(fumen_field[ny])
        row[nx] = 'a'
        fumen_field[ny] = "".join(row)
    # pad with empty lines
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
