from hashlib import md5


def generate_program_key(programName, programURL):
    program_key = md5(
        f"{programName}|{programURL}".encode('utf-8')).hexdigest()
    return program_key
