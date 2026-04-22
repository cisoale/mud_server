def execute(player, conn, args):
    if not args:
        return "Di cosa vuoi parlare?"

    return f"Dici: {' '.join(args)}"