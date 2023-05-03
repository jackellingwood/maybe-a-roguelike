import random

from components.ai import HostileEnemy, WanderingEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2, base_ranged_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

grunt = Actor(
    char="G",
    color=(63, 127, 63),
    name="Grunt",
    ai_cls=WanderingEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),

)
brute = Actor(
    char="B",
    color=(0, 127, 0),
    name="Brute",
    ai_cls=WanderingEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)
marvin = Actor(
    char="M",
    color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    name="Marvin",
    ai_cls=WanderingEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=0),
)

tactical_flashlight = Item(
    char="═",
    color=(207, 63, 255),
    name="Tactical Flashlight",
    consumable=consumable.TacticalFlashlightConsumable(number_of_turns=10),
)
grenade = Item(
    char="◉",
    color=(40, 127, 40),
    name="Grenade",
    consumable=consumable.GrenadeDamageConsumable(damage=12, radius=3),
)
stimpak = Item(
    char="!",
    color=(127, 0, 255),
    name="Stimpak",
    consumable=consumable.HealingConsumable(amount=4),
)
shuriken = Item(
    char="*",
    color=(60, 60, 60),
    name="Shuriken",
    consumable=consumable.ShurikenDamageConsumable(damage=20, maximum_range=5),
)
ammo_box = Item(
    char="#",
    color=(50, 127, 50),
    name="Ammo Box",
    consumable=consumable.AmmoConsumable(12),
)

brassknuckles = Item(
    char="}",
    color=(0, 191, 255),
    name="Brass Knuckles",
    equippable=equippable.BrassKnuckles()
)
knife = Item(
    char="/",
    color=(0, 191, 255),
    name="Knife",
    equippable=equippable.Knife()
)

pistol = Item(
    char="p",
    color=(40, 40, 40),
    name="Pistol",
    equippable=equippable.Pistol()
)
rifle = Item(
    char="r",
    color=(40, 40, 40),
    name="Rifle",
    equippable=equippable.Rifle()
)

light_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Light Armor",
    equippable=equippable.LightArmor()
)
heavy_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Heavy Armor",
    equippable=equippable.HeavyArmor()
)

# very overpowered weapons meant for debugging only (so that I don't have to get good at my own game to test it)
lightsaber = Item(
    char="/",
    color=(0, 191, 255),
    name="Lightsaber",
    equippable=equippable.Lightsaber()
)

bfg = Item(
    char="b",
    color=(40, 40, 40),
    name="BFG",
    equippable=equippable.BFG()
)

plot_armor = Item(
    char="[",
    color=(40, 40, 40),
    name="Plot Armor",
    equippable=equippable.PlotArmor()
)