import os
import subprocess
import requests
import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from fake_useragent import UserAgent
import string

console = Console()

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

clear()

def stp(port):
    console.print(f"[cyan]CONNECTION TO PORT {port}[/cyan]", style="bold blue")
    if not os.path.exists("/data/data/com.termux/files/usr/bin/tinyproxy"):
        console.print("[red]MENGINSTALL BAHAN[/red]", style="bold yellow")
        os.system("pkg install tinyproxy -y")

    config_path = f"/data/data/com.termux/files/usr/etc/tinyproxy_{port}.conf"
    if not os.path.exists(config_path):
        console.print(f"[yellow]DEFAULT[/yellow]", style="bold yellow")
        os.system(f"echo 'Port {port}\nAllow 127.0.0.1' > {config_path}")

    subprocess.Popen(["tinyproxy", "-c", config_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    console.print(f"[green]CONNECTION TO http://127.0.0.1:{port}[/green]")
    return f"127.0.0.1:{port}"

def vp(proxy):
    test_url = "http://httpbin.org/ip"
    proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        response = requests.get(test_url, proxies=proxies_dict, timeout=5)
        if response.status_code == 200:
            console.print(f"[green]CONNECTION : {proxy} : True[/green]")
            return True
    except Exception:
        console.print(f"[red]CONNECTION : {proxy} : False[/red]")
    return False

def rua():
    ua = UserAgent()
    return ua.random

def rc():
    csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return {
        'wa_csrf': csrf_token,
        'wa_lang_pref': 'id',
        'wa_ul': session_id
    }

def rs(length=10):
    characters = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(characters) for _ in range(length))

url = 'https://www.whatsapp.com/contact/noclient/async/new/'

def sr(pn, proxies):
    headers = {
        'authority': 'www.whatsapp.com',
        'accept': '*/*',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.whatsapp.com',
        'referer': 'https://www.whatsapp.com/contact/?subject=messenger',
        'sec-ch-ua': f'"{random.choice(["Not-A.Brand", "Chromium"])}";v="{random.randint(90, 99)}", "Chromium";v="{random.randint(110, 124)}"',
        'sec-ch-ua-mobile': random.choice(['?0', '?1']),
        'sec-ch-ua-platform': f'"{random.choice(["Windows", "Android", "iOS"])}"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': rua(),
        'x-asbd-id': str(random.randint(100000, 999999)),
        'x-fb-lsd': 'AVoCvX9IGCU'
    }

    proxy = random.choice(proxies)
    proxies_dict = {"http": proxy, "https": proxy}

    data = {
        'country_selector': 'ID',
        'email': f'{rs()}@tempmail.com',
        'email_confirm': f'{rs()}@tempmail.com',
        'phone_number': pn,
        'platform': random.choice(['WHATS_APP_WEB_DESKTOP', 'WHATS_APP_ANDROID']),
        'your_message': f'Nomer ini +62{pn} Tidak melakukan kesalahan apapun tetapi sempat memasukan peserta ke anggota mungkin terlalu banyak hingga menyebabkan whatsapp terblokir, Tolong buka kembali akun saya karena itu tidak kesengajaan, saya meminta maaf atas kesalahan saya, mohon buka kembali akun saya, Terimakasih',
        'step': 'submit',
    }

    try:
        cookies = rc()
        response = requests.post(url, headers=headers, data=data, proxies=proxies_dict, cookies=cookies, timeout=10)
        if response.status_code == 200:
            console.print(f"\n[bold cyan]╭───────────────────────────────────────\n╰─> [ BERHASIL SPAM RIPORT ] : +62{pn}[/bold cyan]")
        else:
            print(f"ANDA LIMIT : {response.status_code}")
    except requests.RequestException as e:
        print(f"GAGAL : {e}")

ports = [8888 + i for i in range(15)]
proxies_list = []

for port in ports:
    proxy = stp(port)
    if vp(proxy):
        proxies_list.append(proxy)

if not proxies_list:
    console.print("[red]PROXY MATI SEMUA SERVER OFF[/red]", style="bold red")
    exit()

clear()
console.print(Panel("[bold red]██████╗  ██╗ ███████╗  █████╗   █████╗   █████╗\n██╔══██╗ ██║ ╚══███╔╝ ██╔══██╗ ██╔══██╗ ██╔══██╗\n██║  ██║ ██║   ███╔╝  ╚██████║ ╚██████║ ╚██████║\n[bold white]██║  ██║ ██║  ███╔╝    ╚═══██║  ╚═══██║  ╚═══██║\n██████╔╝ ██║ ███████╗  █████╔╝  █████╔╝  █████╔╝\n╚═════╝  ╚═╝ ╚══════╝  ╚════╝   ╚════╝   ╚════╝\n\n[bold red]● [bold yellow]● [bold green]●\n[bold red]────────────────────────────────────────────────‎\n[bold yellow]-----● SCRIPT SPAM RIPORT ●-----[/bold yellow]\n\n[bold green]PEMBUAT : DIZ FLYZE 999\nYOUTUBE : DIZFLYZE999\nVERSION : v999 KING SPAM REPORT[/bold green]\n[bold red]──────────────────────────────────────────────── ‎", style="bold red"))
console.print(Panel("[bold yellow]MASUKAN NOMOR TARGET DENGAN 8XXX\nINGAT JANGAN SPAM BERLEBIHAN!\nSCRIPT INI MUDAH DOWN JADI SPAM REPORT\n1 HARI 5X SPAM RIPORT KE NOMOR YANG SAMA", style="bold red"))
console.print("[bold cyan]╭───────────────────────────────────────────────────")
pn = console.input("[bold cyan]╰─> [ NOMER TARGET ] : [/bold cyan]")

with Progress() as progress:
    task = progress.add_task("[cyan]PROSES BANG :", total=10)
    for _ in range(15):
        sr(pn, proxies_list)
        progress.update(task, advance=1)
        time.sleep(random.randint(2, 5))
