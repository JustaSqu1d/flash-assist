from time import time, sleep
from os import system
from pypresence import Presence

bot_raw = input("Select a Discord Bot for your Rich Presence!\n0: Minecord\n1: Minecord Classic\n2: Virtual Fisher\n")

while 1:
    try:
        bot = int(bot_raw)
        if bot in range(0,3):
            break
    except:
        pass
    print("Invalid! Please type an actual value.")
    bot_raw = input("Select a Discord Bot for your Rich Presence!\n 0: Minecord\n1: Minecord Classic\n2: Virtual Fisher\n")

if bot == 0: large_image = "https://cdn.discordapp.com/avatars/625363818968776705/e358ecca8de0be6227e31a2e71ed3fd4.png?size=1024"; client_id = '953016872419356712'; name = "Minecord"
if bot == 1: large_image = "https://cdn.discordapp.com/avatars/878007103460089886/5a2ff049dfff59b0b8c6347a5db2f0cc.png?size=1024"; client_id = '925612595271065622'; name = "Minecord Classic"
if bot == 2: large_image = "https://cdn.discordapp.com/avatars/574652751745777665/4e69fb9ac96ca9a6bcb98e20a9cc2259.png?size=1024"; client_id = '953016851024203778'; name = "Virtual Fisher"

RPC = Presence(client_id, pipe_id=0)
start_time = time()
RPC.connect()

print("Rich Presence started!")

sleep(5)
print("You can minimize this window, but closing the window will stop the Rich Presence.")
while True: # The presence will stay on as long as the program is running
    RPC.update(
        details=f"Grinding {name}!",
        start=start_time,
        large_image=large_image,
        large_text="Made possible with Flash Assist!",
        small_image="https://cdn.discordapp.com/avatars/836581672811495465/d9bc4406ca3b9667ce1912dd8155cadc.png?size=1024",
        small_text="© Flash Assist",
        buttons=[{"label": "Invite", "url": "https://discord.com/api/oauth2/authorize?client_id=836581672811495465&permissions=321536&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2FfJt6yFeD5v&response_type=code&scope=identify%20bot%20applications.commands"},
        {"label": "Download", "url": "https://github.com/JustaSqu1d/flash-assist/releases"}]
    )
    sleep(15)