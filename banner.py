def banner():
    print("""
______  _____  ___                                      _     _             
| ___ \/  ___|/ _ \                                    | |   | |            
| |_/ /\ `--./ /_\ \_ __ _ __ ___   __ _  __ _  ___  __| | __| | ___  _ __  
|    /  `--. \  _  | '__| '_ ` _ \ / _` |/ _` |/ _ \/ _` |/ _` |/ _ \| '_ \ 
| |\ \ /\__/ / | | | |  | | | | | | (_| | (_| |  __/ (_| | (_| | (_) | | | |
\_| \_|\____/\_| |_/_|  |_| |_| |_|\__,_|\__, |\___|\__,_|\__,_|\___/|_| |_|
                                          __/ |                             
                                         |___/  

Written by M1gnus && Lotus -- PGIATASTI
                                                                            """)

def credits():
    print("""
Written by Vittorio aka M1gnus and Nalin aka L07u5

Glory to PGiatasti:
    - Vittorio aka M1gnus
    - Alessio aka Alexius
    - Cristiano aka ReverseBrain
    - Riccardo aka ODGrip
    - Nalin aka Lotus
    - Emanuele aka KaiserSource
    - Federico aka Heichou
    - Antonio aka CoffeeStraw

https://pgiatasti.it/ -- -- Visit our site to discover more about us
""")

def show_attacks():
    print("""
===== Implemented Attacks =====
===            5            ===
===============================

Attack <requirements: required, [alternative1 | alternative2]>

fermat <n>
wiener <n,e>
common_factor <n,[n-extra|publickeys-folder]>
p_1 <n>
factordb <n>
""")

def version():
    print("RSArmageddon v.1.0 --Athena--")

if __name__ == '__main__':
    banner()