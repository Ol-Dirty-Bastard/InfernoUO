import API

# Зелье маны: сначала бутылка, если её нет - кег.
# Ищем по названию, поэтому работает и с бутылкой, и с кегом,
# как делал орионовский ADrink по свойствам предмета.

WORDS = ["mana"]
KEG = "keg"

bottle = None
keg = None

for item in API.ItemsInContainer(API.Backpack, True):
    name = item.Name.lower()

    if not any(word in name for word in WORDS):
        continue

    if KEG in name:
        if keg is None:
            keg = item
    elif bottle is None:
        bottle = item

target = bottle if bottle is not None else keg

if target is None:
    API.HeadMsg("маны нет ни в бутылке, ни в кеге", API.Player.Serial)
else:
    API.UseObject(target.Serial)
