from __future__ import annotations

import random
from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You descend the staircase.", color.descend
            )
        else:
            raise exceptions.Impossible("There are no stairs here.")

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        if self.entity.equipment.melee is not None:
            attack_desc = f"{self.entity.name.capitalize()} attacks {target.name} with {self.entity.equipment.melee.name}"
            self.entity.equipment.melee.equippable.decrement_durability()
        else:
            attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )
        if target.equipment.armor is not None:
            target.equipment.armor.equippable.decrement_durability()


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class RangedAction(Action):
    def __init__(
        self, entity: Actor, accurate: bool, target_xy: Optional[Tuple[int, int]] = None,
    ):
        super().__init__(entity)
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        target = self.target_actor

        if not target or not self.engine.game_map.visible[target.x, target.y]:
            raise exceptions.Impossible("Nothing to attack.")
        if target is self.entity:
            raise exceptions.Impossible("Can't take the easy way out, I have a mission to do.")
        if self.entity.equipment.gun is None:
            raise exceptions.Impossible("Finger guns can't cause any real damage.")
        if not self.entity.equipment.gun.equippable.ammo > 0:
            raise exceptions.Impossible("You're out of ammo.")
        if self.entity.equipment.gun.equippable.is_jammed:
            raise exceptions.Impossible("Your gun is jammed!")

        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.entity.equipment.gun.equippable.fully_accurate:
            hit_chance = 1.0
        else:
            hit_chance = pow(1.15, -distance + 1) * self.entity.fighter.accuracy_mult

        if self.entity.equipment.gun.equippable.unjammable:
            jam_chance = 0.0
        else:
            jam_chance = 0.1

        attack_desc = f"{self.entity.name.capitalize()} shoots at the {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if random.random() < jam_chance:
            self.entity.equipment.gun.equippable.jam()
        elif random.random() < hit_chance:
            self.entity.equipment.gun.equippable.decrement_ammo()
            damage = self.entity.fighter.ranged_power - target.fighter.defense

            if damage > 0:
                self.engine.message_log.add_message(
                    f"{attack_desc} for {damage} hit points.", attack_color
                )
                target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(
                    f"{attack_desc} but does no damage.", attack_color
                )
            if target.equipment.armor is not None:
                target.equipment.armor.equippable.decrement_durability()
        else:
            self.entity.equipment.gun.equippable.decrement_ammo()
            self.engine.message_log.add_message(
                f"{attack_desc} but misses!", attack_color
            )
        # self.entity.equipment.gun.equippable.decrement_durability()


class PickupAction(Action):
    """Take an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You took the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to take.")

class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)

class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)

class UnjamAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        if self.entity.equipment.gun is None:
            raise exceptions.Impossible("You have no gun to unjam.")
        if not self.entity.equipment.gun.equippable.is_jammed:
            raise exceptions.Impossible(f"Your {self.entity.equipment.gun.name} isn't jammed.")

        self.entity.equipment.gun.equippable.unjam()