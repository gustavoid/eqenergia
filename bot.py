# import wathdog
import threading
import argparse
import os
from eqenergia.eqenergia import Automation

def parser():
    parser = argparse.ArgumentParser(description='List the content of a folder',epilog='Enjoy the program! :)')
    parser.add_argument('--email', action='store', type=str, required=True)
    parser.add_argument('--nome', action='store', type=str, required=True)
    parser.add_argument('--cnpj', action='store', type=str, required=True)
    parser.add_argument('--mes', action='store', type=str)
    parser.add_argument('--uc', action='store', type=str)
    parser.add_argument('--dir', action='store', type=str)
    parser.add_argument('--headless', help="Não exibe a interface grafica do navegador")
    args = parser.parse_args()
    if args.headless:
        headless = True
    else:
        headless = False
    return (args.email,args.cnpj,args.mes,args.uc,args.dir,args.nome,headless)

def verifyDir(directory):
    if os.path.isdir(directory):
        return True
    else:
        return False

def main():
    email,cnpj,mes,uc,directory,nome,headless = parser()
    if not directory:
        if not os.path.exists("output"):
            os.mkdir("output")
        directory = 'output'
    else:
        if not verifyDir(directory):
            print(f"[-] Não foi possivel encontrar o diretorio {directory}")
            exit(0)
    aut = Automation(cnpj,email,nome,uc,directory,headless,mes)
    aut.login()
    aut.downloadBills()

if __name__ == '__main__':
    main()
