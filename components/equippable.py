from __future__ import annotations

from typing import TYPE_CHECKING

import color
import components.inventory
from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        ranged_bonus: int = 0,
        defense_bonus: int = 0,
        accuracy_bonus: int = 0,
        durability: int = 255,
        max_ammo: int = 255,
        fully_accurate: bool = False,
        unjammable: bool = False
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.ranged_bonus = ranged_bonus
        self.defense_bonus = defense_bonus
        self.accuracy_bonus = accuracy_bonus

        self.durability = durability

        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.fully_accurate = fully_accurate
        self.unjammable = unjammable

        self.is_jammed = False

    def decrement_ammo(self):
        if self.ammo > 0:
            self.ammo = self.ammo - 1

    def decrement_durability(self):
        if self.durability > 1:
            self.durability -= 1
        else:
            self.break_equippable()

    def break_equippable(self):
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            self.engine.message_log.add_message(f"Your {entity.name} breaks!", color.red)
            entity.parent.parent.equipment.unequip_from_slot(entity.equippable.equipment_type.name.lower(), False)
            inventory.items.remove(entity)

    def unjam(self):
        entity = self.parent
        self.is_jammed = False
        self.engine.message_log.add_message(f"You carefully unjam your {entity.name}.")

    def jam(self):
        entity = self.parent
        self.is_jammed = True
        self.engine.message_log.add_message(f"Your {entity.name} jams!", color.red)


class BrassKnuckles(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE, power_bonus=2, durability=10)

class Knife(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE, power_bonus=4, durability=15)


class Pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.GUN, ranged_bonus=4, max_ammo=6, durability=24)

class Rifle(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.GUN, ranged_bonus=6, max_ammo=12, durability=36)


class LightArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1, durability=10)

class HeavyArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3, durability=15)

# very overpowered weapons meant for debugging only (so that I don't have to get good at my own game to test it)
class Lightsaber(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE, power_bonus=9999, durability=9999)

class BFG(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.GUN,
            ranged_bonus=9999, max_ammo=9999,
            fully_accurate=True,
            unjammable=True,
            durability=9999
        )

class PlotArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=9999, durability=9999)