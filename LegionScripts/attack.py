import API

# Атака ближайшей враждебной цели.

HOSTILE = [API.Notoriety.Gray, API.Notoriety.Criminal,
           API.Notoriety.Enemy, API.Notoriety.Murderer]

target = API.NearestMobile(HOSTILE, 12)

if target:
    API.Attack(target.Serial)
else:
    API.HeadMsg("рядом никого", API.Player.Serial)
