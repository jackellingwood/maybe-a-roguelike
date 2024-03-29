"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers


# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    starting_floor = 1
    engine.game_world.current_floor = starting_floor - 1
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "You enter the Hostile Corridors! Good luck, stay alive.", color.welcome_text
    )

    brassknuckles = copy.deepcopy(entity_factories.brassknuckles)
    knife = copy.deepcopy(entity_factories.knife)
    pistol = copy.deepcopy(entity_factories.pistol)
    light_armor = copy.deepcopy(entity_factories.light_armor)

    lightsaber = copy.deepcopy(entity_factories.lightsaber)
    bfg = copy.deepcopy(entity_factories.bfg)
    plot_armor = copy.deepcopy(entity_factories.plot_armor)

    brassknuckles.parent = player.inventory
    knife.parent = player.inventory
    pistol.parent = player.inventory
    light_armor.parent = player.inventory

    lightsaber.parent = player.inventory
    bfg.parent = player.inventory
    plot_armor.parent = player.inventory

    # player.inventory.items.append(brassknuckles)
    # player.equipment.toggle_equip(brassknuckles, add_message=False)

    player.inventory.items.append(knife)
    player.equipment.toggle_equip(knife, add_message=False)

    player.inventory.items.append(pistol)
    player.equipment.toggle_equip(pistol, add_message=False)

    player.inventory.items.append(light_armor)
    player.equipment.toggle_equip(light_armor, add_message=False)


    # player.inventory.items.append(lightsaber)
    # player.equipment.toggle_equip(lightsaber, add_message=False)
    #
    # player.inventory.items.append(bfg)
    # player.equipment.toggle_equip(bfg, add_message=False)
    #
    # player.inventory.items.append(plot_armor)
    # player.equipment.toggle_equip(plot_armor, add_message=False)


    return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            2,
            console.height // 2 - 4,
            "maybe-a-roguelike",
            fg=color.menu_title,
            bg=tcod.black,
            alignment=tcod.LEFT,
        )
        # console.print(
        #     console.width // 2,
        #     console.height - 2,
        #     "By Jack",
        #     fg=color.menu_title,
        #     alignment=tcod.CENTER,
        # )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                2,
                console.height // 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.LEFT,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None