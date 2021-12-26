import click
import os
import requests
from zipfile import ZipFile


def install(path: str) -> None:
    """
    :param path: The path to which the installation shall happen

    This function is to allow the user to install the Soundpacks using the
    'pyhb install soundpacks' command
    """
    click.echo("Installing all the soundpacks now...")
    url = "https://github.com/blankRiot96/hello_cargo/files/7574193/Soundpacks.zip"
    r = requests.get(url, allow_redirects=True)

    with open(path + "/Soundpacks.zip", "wb") as f:
        f.write(r.content)

    file_name = path + "/Soundpacks.zip"

    # Extracting zip file
    with ZipFile(file_name, "r") as f:
        f.extractall(path=path)
        print("Done!")

    # Removing zip file
    if os.path.exists(path + "/Soundpacks.zip"):
        os.remove(path + "/Soundpacks.zip")
