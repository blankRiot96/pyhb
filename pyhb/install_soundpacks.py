import os
import requests
from zipfile import ZipFile


def install(path: str):
    print(path)
    print("Installing all the files now...")
    url = 'https://github.com/blankRiot96/hello_cargo/files/7574193/Soundpacks.zip'
    r = requests.get(url, allow_redirects=True)

    with open(path + "/Soundpacks.zip", "wb") as f:
        f.write(r.content)

    file_name = path + "/Soundpacks.zip"

    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as f:
        # printing all the contents of the zip file
        f.printdir()

        f.extractall(path=path)
        print('Done!')

    if os.path.exists(path + "/Soundpacks.zip"):
        os.remove(path + "/Soundpacks.zip")
