import re
import socket
from http import HTTPStatus

import requests

URL = "https://sstmk.ru"


def get_ip_address(url):
    """Get IP address by url."""
    name = re.sub("^https?://", "", url)
    ip_address = socket.gethostbyname(name)
    return f"IP адрес хоста {url} : {ip_address}"


def extract_phone_number(text):
    """Extract phone from text."""
    pattern = r"\+?(\d{1,3})?\s?\((\d{1,})\)\s?(\d{1,})\-(\d{1,})\-(\d{1,})"
    match = re.search(pattern, text)
    if match:
        if match.group(1):
            if match.group(1) == "8":
                country_code = "+7"
            else:
                country_code = match.group(1)
        else:
            country_code = ""
        city_code = match.group(2)
        phone_number = match.group(3) + "-" + match.group(4) + "-" + match.group(5)
        return f"{country_code}({city_code}){phone_number}"
    else:
        return None


def main():
    """Main function."""
    response = requests.get(URL)
    if response.status_code == HTTPStatus.OK:
        print("Сайт", URL, "работает")
        ip = get_ip_address(URL)
        print(ip)
        phone_number = extract_phone_number(response.text)
        if phone_number:
            print("Номер телефона компании:", phone_number)
        else:
            print("Ошибка: Номер телефона не найден на сайте:", URL)
    else:
        print("Ошибка: Сайт", URL, "не доступен")


if __name__ == "__main__":
    main()
