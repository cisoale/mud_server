def execute(player, args, cmd=None):
    if not args:
        return "Di cosa vuoi parlare?"

    return f"Dici: {' '.join(args)}"