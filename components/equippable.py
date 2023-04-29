from __future__ import annotations

from typing import TYPE_CHECKING

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
        durability: int = 255,
        max_ammo: int = 255,
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.ranged_bonus = ranged_bonus
        self.defense_bonus = defense_bonus
        self.durability = durability
        self.max_ammo = max_ammo
        self.ammo = max_ammo

    def decrement_ammo(self):
        if self.ammo > 0:
            self.ammo = self.ammo - 1

    def decrement_durability(self):
        if self.durability > 1:
            self.durability = self.durability - 1
        else:
            self.break_equippable()

    def break_equippable(self):
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            self.engine.message_log.add_message(f"Your {entity.name} breaks!")
            entity.parent.parent.equipment.unequip_from_slot("melee", False)
            inventory.items.remove(entity)


class BrassKnuckles(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE, power_bonus=2, durability=10)

class Knife(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.MELEE, power_bonus=4, durability=15)


class Pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.GUN, ranged_bonus=2, max_ammo=6)

class Rifle(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.GUN, ranged_bonus=4, max_ammo=12)


class LightArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1, durability=10)

class HeavyArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3, durability=15)