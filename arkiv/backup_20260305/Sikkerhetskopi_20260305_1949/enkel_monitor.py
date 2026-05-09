import requests
import time
import os

SERVER = "http://100.103.79.103:8765"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("=== SANDKASSE MONITOR (ENKEL HTTP) ===")
    print(f"Server: {SERVER}\n")
    while True:
        try:
            r = requests.get(f"{SERVER}/status", timeout=3)
            if r.status_code == 200:
                data = r.json()
                clear()
                print(f"Prosjekt: {data.get('siste_prosjekt', 'ingen')}")
                print(f"Fase: {data.get('fase', '—')}  {data.get('prosent', 0)}%")
                print("Logg:")
                for linje in data.get('logg', [])[-5:]:  # vis siste 5
                    print(f"  {linje}")
                print("\n[oppdateres hvert 2. sekund - Ctrl+C for å avslutte]")
            else:
                print(f"Feil: {r.status_code}")
        except Exception as e:
            print(f"Ingen kontakt: {e}")
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvsluttet.")