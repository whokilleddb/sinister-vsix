import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Example argument parser")

    parser.add_argument(
        "-e", "--ext",
        required=True,
        choices=["livepreview"],
        help="Extension type (livepreview)"
    )

    parser.add_argument(
        "-x", "--shellcode",
        required=True,
        help="Shell file (required)"
    )

    parser.add_argument(
        "-i", "--inflate",
        type=int,
        default=100,
        help="Inflate value (whole number, default: 100)"
    )

    parser.add_argument(
        "--enc",
        choices=["xor", "rc4"],
        default="xor",
        help="Encryption type (xor or rc4)"
    )

    args = parser.parse_args()

    if args.inflate < 0:
        parser.error("--inflate must be a whole number")

    abspath = os.path.abspath(args.shellcode)
    if (not os.path.exists(abspath)) or (not os.path.isfile(abspath)):
        parser.error("--shellcode must point to a valid file")
    

    return args
