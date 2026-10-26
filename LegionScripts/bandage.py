import API

# Бинт на себя. Из орионовского BandageEquip.

BANDAGE = 0x0E21

found = API.FindType(BANDAGE, API.Backpack)

if found:
    API.BandageSelf()
else:
    API.HeadMsg("бинтов нет", API.Player.Serial)
