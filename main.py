import time, os
from valclient.client import Client
import tkinter as tk
from tkinter import messagebox

import win32gui, keyboard, threading


def get_valorant_window_handle():
    def callback(hwnd, hwnds):
        if win32gui.GetWindowText(hwnd) == "VALORANT":
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def check_if_valorant_running():
    hwnd = get_valorant_window_handle()
    print(hwnd)
    if hwnd == 0:
        messagebox.showerror("Valorant Not Found", "Valorant is not running. Please start Valorant before running this application.")
        os._exit(0)

check_if_valorant_running()


client = Client(region='na')
client.activate()

os.system('cls')
print("Made by bznel on discord\n")
print("Don't close this window (it's needed for the instalocker to stay running)\n\nThis also won't work if you select an agent you don't own.\n\nTo toggle the instalocker, click the top half of the window where the status shows.\nThen, you select the agent you want to lock as in the dropdown under it.")

toggle = False

lockChar = ""

mapCodes = {
    "ascent": "Ascent",
    "duality": "Bind",
    "foxtrot": "Breeze",
    "canyon": "Fracture",
    "triad": "Haven",
    "port": "Icebox",
    "pitt": "Pearl",
    "bonsai": "Split",
    "jam": "Lotus"
}

agents = {
    "jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
    "reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
    "raze": "f94c3b30-42be-e959-889c-5aa313dba261",
    "yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
    "phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
    "neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
    "breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
    "skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
    "sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
    "kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
    "killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
    "cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
    "sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
    "chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
    "omen": "8e253930-4c05-31dd-1b6c-968525494517",
    "brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
    "astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
    "viper": "707eab51-4836-f488-046a-cda6bf494859",
    "fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
    "harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
    "gekko": "e370fa57-4757-3604-3648-499e1f642d3f"
}


def select_agent(a, b, c):
    global lockChar

    selected_agent = dropdown.get().lower()
    lockChar = selected_agent

def toggle_variable():
    global toggle
    toggle = not toggle
    update_button_outline()

def update_button_outline():
    if toggle: 
        header_label.configure(text="Loading...")
        check_match()
        header_label.configure(borderwidth=0, relief="solid", fg="white")
    else:
        header_label.configure(text="Instalocker Off")
        header_label.configure(borderwidth=0, relief="solid", fg="red")



def check_match():
    global lockChar

    
    if toggle:

        try:
            sessionState = client.fetch_presence(client.puuid)['sessionLoopState']

            if sessionState == "PREGAME":
                matchID = client.pregame_fetch_match()['ID']

                matchInfo = client.pregame_fetch_match(matchID)
                mapName = matchInfo["MapID"].split('/')[-1].lower()

                client.pregame_select_character(agents[lockChar])
                client.pregame_lock_character(agents[lockChar])

                status_header = f'Locked in on {mapCodes[mapName].capitalize()}'
                header_label.configure(text=status_header)

            elif sessionState == "INGAME":
                header_label.configure(text="Status: In Game")
            elif sessionState == "MENUS":
                header_label.configure(text="Waiting for game...")
            else:
                header_label.configure(text="Loading...")

        except Exception as e:
            print(e)
            pass
    else:
        header_label.configure(text="Instalocker Off")


window = tk.Tk()
window.title("Instalocker")
window.resizable(False, False)
window.attributes("-topmost", True)  
window.geometry("250x150")
window.pack_propagate(0)

valorant_hwnd = get_valorant_window_handle()
win32gui.SetParent(window.winfo_id(), valorant_hwnd)

window.configure(bg="#333333")

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

header_label = tk.Button(
    window, text="Status: Waiting for game", font=("Times", 23), fg="red", anchor="center",
    justify="center", relief="flat", bg="#333333", command=toggle_variable
)
header_label.configure(padx=10, pady=10)
header_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

dropdown = tk.StringVar(window)
dropdown.set("Select an Agent")
dropdown.set("jett")
dropdown.trace("w", select_agent)
dropdown_menu = tk.OptionMenu(window, dropdown, *agents.keys())
dropdown_menu.configure(
    font=("Times", 20),
    borderwidth = "1px",
    bg="#111111",
    fg="#FFFFFF",
    highlightthickness=0,
    relief = "flat"
)
dropdown_menu.configure(padx=10, pady=10)
dropdown_menu.grid(row=1, column=0, columnspan=2, sticky="nsew")

def check_match_thread():
    while True:
        check_match()
        time.sleep(1)  


threading.Thread(target=check_match_thread, daemon=True).start()



window.mainloop()
