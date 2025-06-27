import py_fumen

fumen_code = "v115@vhAxOJbhTaPeJkB9gQaIeQaIeQaIeQaSehuBbhTaPe?ZkB9gQaIeQaIeQaIeQaSeyuBThgWGeiWQeKpBHhgWIegWIe?hWReipBRhiWGegWSe6pBHhhWIegWIegWReTpBRhxSHexSRe?LpBRhxSHexSReDpBRhxSHexSRebpBRhxSHexSRe0pBRhBPI?eBPQeMpBIhAPHeBPHeAPSekpBRhBPIeBPQecpBIhAPHeBPH?eAPSe1uBShQLHeSLQeNpBHhQLIeRLHeQLSelpBRhSLHeQLR?e9pBIhQLHeRLIeQLRe2uBRhgHIeiHQeOpBHhhHHegHIegHS?empBRhiHIegHQe+pBIhgHIegHHehHRe3pBShxDGexDRevpB?HhwDIexDIewDRenpBShxDGexDRe/pB"
rot_to_code = {
    "spawn": 0,
    "right": 1,
    "reverse": 2,
    "left": 3
}
data = {
    "I": [],
    "J": [],
    "L": [],
    "O": [],
    "S": [],
    "T": [],
    "Z": [],
}
pages = py_fumen.decode(fumen_code)
for page in pages:
    op = page.operation
    data[op.piece_type].append((op.x, op.y))
print(data)