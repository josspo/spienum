import requests
import argparse

def print_banner():
    banner = """
                __                                       
  ____  _____ /\_\     __    ___   __  __    ___ ___    
 /',__\\/\\ '__`\\/\\ \\  /'__`\\/' _ `\\/\\ \\/\\ \\ /' __` __`\\  
/\\__, `\\ \\ \\L\\ \\ \\ \\/\\  __//\\ \\/\\ \\ \\ \\_\\ \\/\\ \\/\\ \\/\\ \\ 
\\/\\____/\\ \\ ,__/\\ \\_\\ \\____\\ \\_\\ \\_\\ \\____/\\ \\_\\ \\_\\ \\_\\
 \\/___/  \\ \\ \\/  \\/_/\\/____/\\/_/\\/_/\\/___/  \\/_/\\/_/\\/_/
          \\ \\_\\                          Author: 5p1d4r         
           \\/_/   
    """
    print(banner)

def read_wordlist(filepath):
    try:
        with open(filepath, 'r') as file:
            words = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        return words
    except FileNotFoundError:
        print("\n[i] Error: Could not find the wordlist!")
        return []

def subenum():
    # Take CLI argument for URL and a wordlist (spienum.py --u or -u and -w or --wordlist)
    parser = argparse.ArgumentParser(description='Fetch a URL and process a wordlist')
    parser.add_argument('-u', '--url', type=str, required=True, help='The URL to fetch')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to wordlist for subdomains')
    args = parser.parse_args()
    target = args.url
    wordlist = args.wordlist

    protocol = target.split("://", 1)[0]
    base_domain = target.split("://", 1)[1]

    # Check if the target is alive and add colors to the response
    print('\n----Check if the target is alive----\n')
    print(f"[*] Checking if \033[34m{target}\033[0m is alive")
    try:
        r = requests.head(target)
        print(f"[i]  \033[32m{target}\033[0m is alive")
    except requests.ConnectionError:
        print(f"[i]  \033[31m{target}\033[0m failed to connect")
        

    # Check for the wordlist, if wordlist is not found exit
    words = read_wordlist(wordlist)
    if not words:
        exit(1)

    # Subdomain Enumeration
    print('\n----Subdomain Enumeration----\n')
    print(f"[*] Enumerating subdomains for \033[34m{target}\033[0m")

    for word in words:
        subdomain = f"{protocol}://{word}.{base_domain}"
        try:
            r = requests.head(subdomain)
            if r.status_code == 200 or 302:
                print(f"\n[!] Subdomain Found: \033[32m{subdomain}\033[0m\n")
        except requests.ConnectionError:
            pass


def main():
    print_banner()
    subenum()


if __name__ == "__main__":
    main()
