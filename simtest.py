from sim import BLOCK_SHAPES

for i in range(4):
    for block in BLOCK_SHAPES[i]:
        print(f"Rotation {i}, Block {block}")
        grid = [[" " for _ in range(4)] for _ in range(4)]
        for x, y in BLOCK_SHAPES[i][block]:
            grid[3 - y][x] = block[0]
        for row in grid:
            print("".join(row))
        print()

# import sim
# import json

# tetsim = sim.TetSim(["GG_GGGGGGG"], "O", None, "")
# print(json.dumps(tetsim.export_pages(["GG_GGGGGGG"], "O", None, "", ["left", "hd"]), indent=4, ensure_ascii=False))