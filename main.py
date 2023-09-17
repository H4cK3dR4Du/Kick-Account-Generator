import json, hotmailbox, random, string, os, time, getpass, ctypes, sys, threading, re

try:
    import tls_client
    import colorama
    import datetime
    import pystyle
    import requests
    import imaplib
    import websocket
    import easygui
except ModuleNotFoundError:
    os.system("pip install tls_client")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install requests")
    os.system("pip install imaplib")
    os.system("pip install websocket")
    os.system("pip install easygui")

from tls_client import Session
from colorama import Fore, Style
from pystyle import Write, System, Colors, Colorate
from datetime import datetime

output_lock = threading.Lock()
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

class Utils:
    @staticmethod
    def get_birthdate():
        birthdate = f"{str(random.randint(1, 12)).zfill(2)}/{str(random.randint(1, 30)).zfill(2)}/{random.randint(1985, 2003)}"
        return birthdate

    @staticmethod
    def get_time():
        date = datetime.now()
        hour, minute, second = date.hour, date.minute, date.second
        timer = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        return timer

    @staticmethod
    def generate_password():
        password = f"TLS_spoofing${random.randint(0, 10000000)}$"
        return password

    @staticmethod
    def generate_username():
        usernames = ['tls_spoofing', 'PyController', 'H4cK3dR4Du', 'Radu', 'ILoveFeds', 'Python', 'Tls_gay']
        s = random.choice(usernames)
        username = f"{s}{random.randint(0, 10000000)}"
        return username

def generate_kick_accounts():
    config = json.load(open('config.json', 'r', encoding='utf-8'))
    token = config["kopeechka-key"]
    session = tls_client.Session(
        client_identifier="chrome114",
        random_tls_extension_order=True,
    )
    
    with open("proxies.txt", "r") as f:
        proxies = f.read().splitlines()
        proxy = random.choice(proxies)
        
    session.proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
    }

    r = requests.get(f"http://api.kopeechka.store/mailbox-get-email?site=kick.com&mail_type=OUTLOOK&token={token}&password=0&regex=&subject=&investor=0&soft=28677&type=undefined&api=2.0")

    email = r.json()['mail']
    id_kope = r.json()['id']
    time_rn = Utils.get_time()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({orange}${gray}) {pretty}Purchased {gray}---> {cyan}{email}{gray} | ID : {cyan}{id_kope}")

    ws = websocket.create_connection("wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false", header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    socket_id = json.loads(json.loads(ws.recv())["data"])["socket_id"]
    time_rn = Utils.get_time()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({magenta}*{gray}) {pretty}Got Socked ID {gray}---> {cyan}{socket_id}")

    session.headers = {
        'authority': 'kick.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'fr-FR,fr;q=0.9',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    session.cookies = session.get('https://kick.com/').cookies
    cookies_str = str(session.cookies)
    result = re.search(r'<RequestsCookieJar\[<Cookie\s+([^=]+)=', cookies_str)
    if result:
        value = result.group(1) 

    xsrf_token = session.cookies.get("XSRF-TOKEN").replace("%3D", "=")
    cf_bm = session.cookies.get(f"__cf_bm")
    
    session.headers.update({
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {xsrf_token}",
        "x-socket-id": socket_id,
        "x-xsrf-token": xsrf_token
    })

    response = session.get("https://kick.com/kick-token-provider")
    session.cookies.update(response.cookies)
    encryptedValidFrom = response.json()['encryptedValidFrom']
    nameFieldName = response.json()['nameFieldName']

    birthdate = Utils.get_birthdate()
    password = Utils.generate_password()
    username = Utils.generate_username()

    data = {
        'email': email
    }

    r = session.post("https://kick.com/api/v1/signup/send/email", json=data)
    
    if r.status_code == 204:
        time_rn = Utils.get_time()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}/{gray}) {pretty}Sent OTP Code {gray}---> {pink}{email}")
        time.sleep(30)
    else:
        time_rn = Utils.get_time()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Failed To Send OTP Code {gray}---> {pink}{email}")
        generate_kick_accounts()

    r = requests.get(f"http://api.kopeechka.store/mailbox-get-message?id={id_kope}&token={token}&full=1&api=2.0")
    pattern = r'\b\d{6}\b'
    matches = re.findall(pattern, r.text)
    
    for match in matches:
        if not match.startswith("070809"):
            time_rn = Utils.get_time()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({blue}@{gray}) {pretty}Got OTP Code {gray}---> {green}{match}")
            data = {
                'code': match,
                'email': email
            }
            
            r = session.post(f"https://kick.com/api/v1/signup/verify/code", json=data)

            if r.status_code == 204:
                time_rn = Utils.get_time()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({cyan}#{gray}) {pretty}Verified Email {gray}---> {pink}{email}")
            else:
                time_rn = Utils.get_time()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {pretty}Failed To Verify Email {gray}---> {pink}{email}")

    payload = {
        'agreed_to_terms': True,
        'birthdate': birthdate,
        'cf_captcha_token': "",
        'email': email,
        'enable_sms_promo': False,
        'enable_sms_security': False,
        'newsletter_subscribed': False,
        'password': password,
        'password_confirmation': password,
        't': "",
        'username': username,
        nameFieldName: "",
        '_kick_token_valid_from': encryptedValidFrom
    }

    response2 = session.post(f"https://kick.com/register", json=payload)
    session.cookies.update(response2.cookies)
    time_rn = Utils.get_time()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}Generated {gray}---> {pink}{email}{gray}:{pink}{password}")
    with open(f"Results/genned_accounts.txt", "a+", encoding='utf-8') as f:
        f.write(f"{email}:{password}" + "\n")

    generate_kick_accounts()

def ui():
    ctypes.windll.kernel32.SetConsoleTitleW(f"[ Kick.com Account Generator ] By H4cK3dR4Du & PyController | github.com/H4cK3dR4Du ~ github.com/PyController")
    threads = []
    config = json.load(open('config.json', 'r', encoding='utf-8'))
    threads_f = config['threads']
    for _ in range(int(threads_f)):
        thread = threading.Thread(target=generate_kick_accounts)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
ui()