import API

# Перебор роб по кругу: нажал - надел следующую, прошлую снял в рюкзак.
# Кончились - начинает сначала.
#
# По названию робы не различить: Апешка и Регенка на шарде одинаково
# зовутся magicrobe. Поэтому берём все робы, что есть при себе, и
# различаем их по типу и цвету - у каждой он свой.

ROBE_LAYER = 0x16

# Подписи по цвету: имена у роб одинаковые, различает их только цвет.
# Новую робу добавлять не нужно - она подхватится сама, а здесь можно
# дать ей понятное имя для сообщения над головой.
NAMES = {
    0x0487: "Кахуна",
    0x0501: "Апешка",
    0x0863: "Регенка",
}


def is_robe(item):
    data = item.GetItemData()
    return data is not None and data.Layer == ROBE_LAYER


def key(item):
    # порядок стабильный: сперва по типу, потом по цвету, потом по вещи
    return (item.Graphic, item.Hue, item.Serial)


robes = []

for item in API.ItemsInContainer(API.Backpack, True) or []:
    if is_robe(item):
        robes.append(item)

worn = API.FindLayer("robe")

if worn and is_robe(worn):
    robes.append(worn)

robes.sort(key=key)

if not robes:
    API.HeadMsg("роб при себе нет", API.Player.Serial)
else:
    at = -1

    if worn:
        for i, item in enumerate(robes):
            if item.Serial == worn.Serial:
                at = i
                break

    if at >= 0:
        API.MoveItem(worn.Serial, API.Backpack)
        API.Pause(0.25)

    nxt = robes[(at + 1) % len(robes)]

    if nxt.Serial == (worn.Serial if worn else 0):
        API.HeadMsg("роба одна", API.Player.Serial)
    else:
        API.EquipItem(nxt.Serial)
        API.HeadMsg(NAMES.get(nxt.Hue, "0x%04X" % nxt.Hue), API.Player.Serial)
