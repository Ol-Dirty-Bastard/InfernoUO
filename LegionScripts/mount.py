import API

# Сесть на скакуна или слезть.
#
# Скакун запоминается при посадке и при слезании, поэтому дальше хватает
# одной клавиши: слез - сел обратно, даже если рядом стоят чужие животные.
# Если запомненного нет рядом, берём ближайшее своё животное.
# Эфирный скакун в рюкзаке важнее живого: есть эфирка - садимся на неё.

VAR = "shard_mount"
MINE = [API.Notoriety.Ally, API.Notoriety.Innocent, API.Notoriety.Invulnerable]

# Эфирные скакуны в рюкзаке идут раньше живых: первые пять выдаёт
# EtherealBox на шарде, остальные - на случай других эфирок
ETHEREALS = [
    0x20DD,  # Ethereal Horse
    0x25CE,  # Ethereal Unicorn
    0x25A0,  # Ethereal Kirin
    0x2619,  # Ethereal Swamp Dragon
    0x260F,  # Ethereal Beetle
    0x20F6,  # Ethereal Llama
    0x2135,  # Ethereal Ostard
    0x2615,  # Ethereal Ridgeback
    0x20E1,  # Ethereal Polar Bear
    0x276A,  # Ethereal Hiryu
    0x2D95,  # Ethereal Reptalon
    0x2D96,  # Ethereal Cu Sidhe
]


def ethereal():
    for graphic in ETHEREALS:
        item = API.FindType(graphic, API.Backpack)

        if item:
            return item

    return None


def saved():
    try:
        return int(API.GetPersistentVar(VAR, "0", API.PersistentVar.Char))
    except ValueError:
        return 0


def remember(serial):
    API.SavePersistentVar(VAR, str(serial), API.PersistentVar.Char)
    API.SetMount(serial)


def nearby():
    # IsRenamable стоит только у своих питомцев: чужую лошадь
    # переименовать нельзя, по этому признаку её и отсекаем
    for mob in API.NearestMobiles(MINE, 2) or []:
        if mob.Serial == API.Player.Serial:
            continue

        if mob.IsHuman or not mob.IsRenamable:
            continue

        return mob

    return None


if API.Player.IsMounted:
    API.Dismount()
    API.Pause(0.8)

    # слезли с эфирки - она уже в рюкзаке, запоминать живность незачем
    horse = None if ethereal() else nearby()

    if horse:
        remember(horse.Serial)
else:
    statuette = ethereal()

    if statuette:
        API.UseObject(statuette.Serial)
    else:
        serial = saved()
        horse = API.FindMobile(serial) if serial else None

        if horse is None or horse.Distance > 3:
            horse = nearby()

            if horse:
                remember(horse.Serial)

        if horse:
            API.Msg("all stop")
            API.Mount(horse.Serial)
        else:
            API.HeadMsg("скакуна рядом нет", API.Player.Serial)
