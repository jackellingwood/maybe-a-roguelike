from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from playaudio import playaudio
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(
        self,
        hp: int,
        base_defense: int = 0,
        base_power: int = 1,
        base_ranged_power: int = 1,
        base_accuracy: int = 1
    ):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power
        self.base_ranged_power = base_ranged_power
        self.base_accuracy = base_accuracy

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
        if self.hp > 0:
            playaudio("audio/jsfxr-hit.wav")
        else:
            playaudio("audio/jsfxr-kill.wav")

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def ranged_power(self) -> int:
        return self.base_ranged_power + self.ranged_bonus

    @property
    def accuracy_mult(self) -> int:
        return self.base_accuracy + self.accuracy_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def ranged_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.ranged_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    @property
    def accuracy_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.accuracy_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)