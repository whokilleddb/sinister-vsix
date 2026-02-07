

from src.cli import parse_args
from src.generator import Generator

def banner():
    """
    Print the banner 
    """

    print(
r"""
  _____ _       _     _         __      _______ _______   __
 / ____(_)     (_)   | |        \ \    / / ____|_   _\ \ / /
| (___  _ _ __  _ ___| |_ ___ _ _\ \  / / (___   | |  \ V / 
 \___ \| | '_ \| / __| __/ _ \ '__\ \/ / \___ \  | |   > <  
 ____) | | | | | \__ \ ||  __/ |   \  /  ____) |_| |_ / . \ 
|_____/|_|_| |_|_|___/\__\___|_|    \/  |_____/|_____/_/ \_\
                                
                                             by @whokilleddb
"""
    )

def main():
    banner()
    cli_args = parse_args()
    print(cli_args)

    gen = Generator(cli_args.ext, cli_args.shellcode, cli_args.inflate, cli_args.enc)

if __name__ == "__main__":
    main()
