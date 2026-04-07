from core.command_handler import commands


def execute(player, args, cmd=None):
    # 📌 help specifico
    if args:
        name = args[0].lower()

        if name in commands:
            cmd_module = commands[name]

            desc = getattr(cmd_module, "description", "Nessuna descrizione.")
            usage = getattr(cmd_module, "usage", "Nessun uso.")

            return f"{name}\n{desc}\nUso: {usage}"

        return "Comando non trovato."

    # 📌 lista comandi
    output = ["Comandi disponibili:"]

    for name in sorted(commands.keys()):
        cmd_module = commands[name]
        desc = getattr(cmd_module, "description", "")

        output.append(f"{name} - {desc}")

    return "\n".join(output)