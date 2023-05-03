import requests
from hashlib import md5


def get_resource(tmp_dir, url, platformName):
    domainList = requests.get(url, allow_redirects=True)
    open(F"{tmp_dir}{platformName}.json", 'wb').write(domainList.content)


def generate_program_key(programName, programURL):
    program_key = md5(
        f"{programName}|{programURL}".encode('utf-8')).hexdigest()
    return program_key
