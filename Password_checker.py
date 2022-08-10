import requests
import hashlib
import sys
import io

HASH_SPLIT = 5
ENCODING_TYPE = 'utf_8'

def request_APT_data(quary_char: str):
    url = 'https://api.pwnedpasswords.com/range/' + quary_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"error fetching: {res.status_code}, check the API and try again")
    return res

def pwnd_API_check(password: str):
    hash1password = hashlib.sha1(password.encode(ENCODING_TYPE)).hexdigest().upper()
    head = hash1password[:HASH_SPLIT]
    tail = hash1password[HASH_SPLIT:]

    res = request_APT_data(head)
    return get_leak_count(res, tail)

def get_leak_count(leaks, check):
    hashes = (line.split(':') for line in leaks.text.splitlines())
    for hash, count in hashes:
        if hash == check:
            return count
    return 0

def run(filename):
    try:
        with open(filename) as file:
            for line in file.readlines():
                password = line.strip()
                if not password:
                    continue
                count = pwnd_API_check(password)
                if count:
                    print(f"oh no, '{password}' been pwnd {count} time(s)!!")
                else:
                    print(f"{password} is GOLD!")
    except:
        print('file does not exist')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print(f'{sys.argv[0]} require 1 argument')