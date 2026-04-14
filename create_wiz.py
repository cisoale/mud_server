from core.database import create_player, make_builder, get_player

# crea player
if not get_player("wiz"):
    create_player("wiz", "1234")
    print("Creato wiz")

# rendilo builder
make_builder("wiz")
print("wiz ora è builder")