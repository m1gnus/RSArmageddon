#!/bin/bash

# tested on the following OS:
# - kali 2020.1

# check that setup is running in the correct directory
if [[ ! -e "./RSAGD_core.py" ]]
then
    echo -e "[-] Please run the setup inside RSArmageddon root directory"
    exit 1
fi

# check that the user is not root
if [[ $(whoami) == "root" ]]
then
    echo -e "[-] Please don't run the setup as root"
    exit 1
fi

# print the banner
echo -e '$$$$$$$$$$$$$$$$$$$$$$$$$$'
echo -e '$$$ RSArmageddon Setup $$$'
echo -e '$$$$$$$$$$$$$$$$$$$$$$$$$$\n'

echo -e "[*] Now the following dependencies will be installed: gcc, m4, pkg-config, libpng-dev, libssl-dev"

while [[ $ANS != "N" && $ANS != "n" && $ANS != "Y" && $ANS != "y" ]]
do
    echo -n "[*] Proceed? [Y/N]: "
    read ANS
    if [[ $ANS == 'N' || $ANS == "n" ]]
    then
        echo "[+] Exiting with exit code 0"
        exit 0
    elif [[ $AND == 'Y' || $ANS == "y" ]]
    then
        echo
        break
    fi
done

# install needed dependencies
echo "[+] Installing dependencies:"
sudo apt-get update -y
sudo apt-get install -y gcc
sudo apt-get install -y m4
sudo apt-get install -y pkg-config
sudo apt-get install -y libpng-dev
sudo apt-get install -y libssl-dev

# if /usr/local/bin is not in PATH, add it to PATH
A=0
for i in $(echo "$PATH" | tr ':' ' ')
do
    if [[ $i == "/usr/local/bin" ]]
    then
        A=1
        break
    fi
done

if [[ $A -eq 0 ]]
then
    echo "[+] adding \"/usr/local/bin\" to your PATH..."
    echo 'executing: $PATH=$PATH:/usr/local/bin >> ~/.bashrc'
    echo '$PATH=$PATH:/usr/local/bin' >> ~/.bashrc
    echo "if you don't use bash please manually add /usr/local/bin to your path"
    PATH="$PATH:/usr/local/bin"
    echo "press any key to continue..."
    read
fi

# if sage is not installed, download and install it
ANS="Z"
if [[ $(which sage) == '' ]]
then
    while [[ $ANS != "N" && $ANS != "n" && $ANS != "Y" && $ANS != "y" ]]
    do
        echo -n "Sage not found on your system, do you want to install it? [Y/N]: "
        read ANS
        if [[ $ANS == 'N' || $ANS == "n" ]]
        then
            echo "[-] In order to continue the setup sage must be installed on your system"
            exit 1
        elif [[ $ANS == 'Y' || $ANS == "y" ]]
        then
            echo "[+] Downloading Sage..."
            wget http://www-ftp.lip6.fr/pub/math/sagemath/linux/64bit/sage-9.1-Debian_GNU_Linux_10-x86_64.tar.bz2 -O Sage.tar.bz2
            echo "[+] Installing Sage..."
	    tar -xvf Sage.tar.bz2
            sudo mv ./SageMath/ /opt/SageMath
            rm -rf Sage.tar.bz2

            _PWD="$PWD"
            PWD="/opt/SageMath"

            make
            break
        fi
    done
fi

if [[ ! -z $_PWD ]]
then
    PWD="$_PWD"
fi

echo -e "\n[+] Creating absolute path reference for RSArmageddon modules\n"
echo "SOFTWARE_PATH = \"$PWD\"" > misc/software_path.py

echo -e "\n[+] Creating symlink in /usr/local/bin\n"
# be sure that the executable files have execution permission
chmod +x /opt/SageMath/sage
chmod +x "$PWD"/RSAGD_core.py
chmod +x "$PWD"/cipher_tools/openssl_cipherfile.sh
sudo ln -s /opt/SageMath/sage /usr/local/bin/sage
sudo ln -s "$PWD"/RSAGD_core.py /usr/local/bin/rsarmageddon
sudo ln -s "$PWD"/cipher_tools/openssl_cipherfile.sh /usr/local/bin/cipherfile-rsarmageddon

echo -e "\n[+] Installing needed modules\n"
sage -pip install lxml
sage -pip install pycryptodome
sage -pip install gmpy2
sage -pip install bs4
sage -pip install argparse
sage -pip install requests
