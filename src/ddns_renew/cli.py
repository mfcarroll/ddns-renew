import os
import sys
import argparse
from dotenv import load_dotenv
from ddns_renew.core import confirm_host


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Auto-renew No-IP DDNS hostname.")
    parser.add_argument(
        "host_id",
        nargs="?",
        help="The No-IP confirmation host ID (the 'n' parameter in the URL).",
    )
    parser.add_argument(
        "--proxy_url",
        help="Proxy URL in the format http://USERNAME:PASSWORD@HOST:PORT/",
    )
    args = parser.parse_args()

    host_id = args.host_id or os.environ.get("NOIP_HOST_ID")
    proxy_url = args.proxy_url or os.environ.get("PROXY_URL")

    if not host_id:
        print(
            "Error: You must provide a host ID either as a command-line argument or via the NOIP_HOST_ID environment variable."
        )
        sys.exit(1)

    confirm_host(host_id, proxy_url)


if __name__ == "__main__":
    main()
