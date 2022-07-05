from time import time, sleep
from os import system
from pypresence import Presence

inputText = """Select a Discord Bot for your Rich Presence!
0: Dank Memer
1: EPIC RPG
2: Idle Miner
3: IdleCapitalist
4: Lumby
5: Minecord
6: Minecord Classic
7: Mining Simulator
8: Pokétwo
9: TacoShack
a: Virtual Farmer
b: Virtual Fisher
"""

bot_raw = input(inputText)

while 1:
    if bot_raw not in range(0, 10) and bot_raw not in ["a", "b"]:
        print("Invalid! Please type an actual value.")
        bot_raw = input(inputText)
    else:
        bot = bot_raw
        break

if bot == "0":
    large_image = "https://images-ext-1.discordapp.net/external/sEev9rpzR51thKMUIm7PbgzWd4C_9bf9sNI2xpR5Be4/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/270904126974590976/d60c6bd5971f06776ba96497117f7f58.png"
    client_id = "270904126974590976"
    name = "Dank Memer"
elif bot == "1":
    large_image = "https://images-ext-1.discordapp.net/external/N575pc11N9QXpXh1IrghZ0_MqoAA0H9kUZ4eWjc2tpE/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/555955826880413696/117bb03dda322b41083a017736ae73c4.png"
    client_id = "555955826880413696"
    name = "EPIC RPG"
elif bot == "2":
    large_image = "https://images-ext-1.discordapp.net/external/ZRo4uC3Mty3pFEV2BaB3Hb1JQHMyfMnvEVu_RxV6ajU/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/518759221098053634/ab882ddd2d0327839c4b5c6f51debd63.png"
    client_id = "518759221098053634"
    name = "Idle Miner"
elif bot == "3":
    large_image = "https://images-ext-1.discordapp.net/external/kOI4joX2j75-95JULVGSE-Np52OznznX__-NaCN-w4o/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/512079641981353995/96a9ce5d7e088b53ad560912f5ab70bc.png"
    client_id = "512079641981353995"
    name = "IdleCapitalist"
elif bot == "4":
    large_image = "https://images-ext-1.discordapp.net/external/yw0ZduxBq7kRIwuSVeXW0UX0yxXNrcbZ1dDGjwYHhw4/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/735274365813522534/158346b9514aa991e4e3b0436669c808.png"
    client_id = "735274365813522534"
    name = "Lumby"
elif bot == "5":
    large_image = "https://cdn.discordapp.com/avatars/625363818968776705/e358ecca8de0be6227e31a2e71ed3fd4.png?size=1024"
    client_id = "953016872419356712"
    name = "Minecord"
elif bot == "6":
    large_image = "https://cdn.discordapp.com/avatars/878007103460089886/5a2ff049dfff59b0b8c6347a5db2f0cc.png?size=1024"
    client_id = "925612595271065622"
    name = "Minecord Classic"
elif bot == "7":
    large_image = "https://images-ext-1.discordapp.net/external/nXM75Y7z2B53DfLEYKi5dT3jO6bkLW0GtwGtK1vcJpA/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/520282851925688321/4b737a5e1450d893b2761d03e7b79974.png"
    client_id = "520282851925688321"
    name = "Mining Simulator"
elif bot == "8":
    large_image = "https://images-ext-1.discordapp.net/external/ej0X-9cXdW1DdkJklqTmopCMnCebf-cXB9VG7QpNJ6Y/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/716390085896962058/2489a9b2c2eb951ed908be416ced10a2.png"
    client_id = "716390085896962058"
    name = "Pokétwo"
elif bot == "9":
    large_image = "https://images-ext-2.discordapp.net/external/dG80z772GhQ3z9hK7lgDMxiuz0UlRrWmZ15pEEPMJuk/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/490707751832649738/67824035d1276a002ea0f3740c60dbc2.png"
    client_id = "490707751832649738"
    name = "TacoShack"
elif bot == "a":
    large_image = "https://images-ext-1.discordapp.net/external/D_D0V7pgAM52PWXuynccn1vpOwup-ANkDobE5qmRhuM/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/631216892606152714/a72fd6fcbac4d59da31ebfd88518caa0.png"
    client_id = "631216892606152714"
    name = "Virtual Farmer"
elif bot == "b":
    large_image = "https://cdn.discordapp.com/avatars/574652751745777665/4e69fb9ac96ca9a6bcb98e20a9cc2259.png?size=1024"
    client_id = "953016851024203778"
    name = "Virtual Fisher"


RPC = Presence(client_id, pipe_id=0)
start_time = time()
RPC.connect()

print("Rich Presence started!")

sleep(5)
print(
    "You can minimize this window, but closing the window will stop the Rich Presence."
)
while True:  # The presence will stay on as long as the program is running
    RPC.update(
        details=f"Grinding {name}!",
        start=start_time,
        large_image=large_image,
        large_text="Made possible with Flash Assist!",
        small_image="https://cdn.discordapp.com/avatars/836581672811495465/d9bc4406ca3b9667ce1912dd8155cadc.png?size=1024",
        small_text="© Flash Assist",
        buttons=[
            {
                "label": "Download",
                "url": "https://github.com/JustaSqu1d/flash-assist/releases",
            },
            {"label": "More Info", "url": "https://flash-assist.glitch.me"},
        ],
    )
    sleep(15)
