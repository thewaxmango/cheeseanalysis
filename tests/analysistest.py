from blockfish import AI, Snapshot
import asyncio

async def main():
    ai = AI()
    await ai.start()

    # Replace this with your actual board string
    hold = 'L'
    queue = "OSIZSZIOJTLSZIOJLTLZIJSTOSOZLTJIISJOTZLJTISZLOLITZJOSTSZOLJIZILJSOTILOSJZTTJZSILOTZOJSILJLSTIOZTOJLZISSZILTOJTIZJOSLZITJSOLJITZSLOLSIOTZJIJLOZTSSLOJITZJOTZISLOSZTLIJLIOZJTSLSOITZJITOZLJSZSILTJOTISJOZLOJSZITLTZSLJOIZOIJSLTTJZSIOLOLIZTSJTILZSJOJOLTSZI"
    queue = queue[:6]
    matrix = ['________T_', '_____JJJTT', '_GGGGGGGGG', 'GG_GGGGGGG', 'G_GGGGGGGG', 'GGGGGG_GGG', 'G_GGGGGGGG', 'GG_GGGGGGG', 'GGGGG_GGGG']
    matrix = matrix[:]

    snapshot = Snapshot(hold=hold, queue=queue, matrix=matrix)
    suggestions, stats = await ai.analyze(snapshot)
    print(suggestions)
    print(stats)
    ai.shutdown()

if __name__ == "__main__":
    asyncio.run(main())