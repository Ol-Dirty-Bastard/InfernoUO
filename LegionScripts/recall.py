import API

# Рекол по руне из рюкзака.

RUNE = 0x1F14

rune = API.FindType(RUNE, API.Backpack)

if not rune:
    API.HeadMsg("руны нет", API.Player.Serial)
else:
    API.CastSpell("Recall")

    if API.WaitForTarget("neutral", 3):
        API.Target(rune.Serial)
