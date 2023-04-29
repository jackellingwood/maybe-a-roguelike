from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, melee: Optional[Item] = None, gun: Optional[Item] = None, armor: Optional[Item] = None):
        self.melee = melee
        self.gun = gun
        self.armor = armor

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.melee is not None and self.melee.equippable is not None:
            bonus += self.melee.equippable.defense_bonus

        if self.gun is not None and self.gun.equippable is not None:
            bonus += self.gun.equippable.defense_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        return bonus

    @property
    def ranged_bonus(self) -> int:
        bonus = 0

        if self.melee is not None and self.melee.equippable is not None:
            bonus += self.melee.equippable.ranged_bonus

        if self.gun is not None and self.gun.equippable is not None:
            bonus += self.gun.equippable.ranged_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.ranged_bonus

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0

        if self.melee is not None and self.melee.equippable is not None:
            bonus += self.melee.equippable.power_bonus

        if self.gun is not None and self.gun.equippable is not None:
            bonus += self.gun.equippable.power_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.power_bonus

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.melee == item or self.gun == item or self.armor == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.MELEE
        ):
            slot = "melee"
        elif (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.GUN
        ):
            slot = "gun"
        else:
            slot = "armor"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)