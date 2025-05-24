#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + """
██╗  ██╗███████╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗
██║  ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝
███████║█████╗  ██████╔╝█████╗  █████╗  ██████╔╝ ╚████╔╝ 
██╔══██║██╔══╝  ██╔═══╝ ██╔══╝  ██╔══╝  ██╔═══╝   ╚██╔╝  
██║  ██║███████╗██║     ███████╗███████╗██║        ██║   
╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚══════╝╚═╝        ╚═╝   
        HTTP Header & CMS Detector - HeaderSpy
              Made by PrinceAKA930 | GitHub.com
""")

def detect_cms(html):
    if "wp-content" in html or "wordpress" in html:
        return "WordPress"
    elif "joomla" in html:
        return "Joomla"
    elif "drupal" in html:
        return "Drupal"
    elif "shopify" in html:
        return "Shopify"
    else:
        return "Unknown"

def check_security_headers(headers):
    security_headers = [
        "X-Frame-Options",
        "Content-Security-Policy",
        "X-XSS-Protection",
        "Strict-Transport-Security",
        "X-Content-Type-Options"
    ]
    print(Fore.YELLOW + "\n[+] Security Headers:")
    for h in security_headers:
        if h in headers:
            print(Fore.GREEN + f"✔ {h}: {headers[h]}")
        else:
            print(Fore.RED + f"✘ {h}: Not Found")

def scan_target(url):
    try:
        print(Fore.MAGENTA + f"\n[~] Scanning {url}...\n")
        response = requests.get(url, timeout=10)
        headers = response.headers
        soup = BeautifulSoup(response.text, "html.parser")

        print(Fore.BLUE + "[+] Response Headers:")
        for key, value in headers.items():
            print(Fore.CYAN + f"{key}: {value}")

        cms = detect_cms(response.text)
        print(Fore.YELLOW + f"\n[+] Detected CMS: {Fore.GREEN + cms}")

        check_security_headers(headers)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] Error: {e}")

if __name__ == "__main__":
    banner()
    target = input(Fore.LIGHTWHITE_EX + "\nEnter website URL (with http:// or https://): ").strip()
    if not target.startswith("http"):
        target = "http://" + target
    scan_target(target)
