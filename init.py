import os
import shutil
import time
import uuid
from subprocess import Popen

DETACHED_PROCESS = 0x00000008

parent_dir = __file__.rsplit("\\", 1)[0] + "\\"

dir_name = input("Name of the Directory: ")
if not os.path.exists(parent_dir + dir_name):
    shutil.copytree(
        f".",
        parent_dir + dir_name,
        ignore=lambda src, names: [
            name
            for name in names
            if any([x in name or x in src for x in [".git", ".venv", "init.py"]])
        ],
    )

time.sleep(1)

with open(parent_dir + dir_name + "\\bot-setup.iss", "r") as f:
    text = f.read()

with open(parent_dir + dir_name + "\\bot-setup.iss", "w") as f:
    text = text.replace("Base Bot", f"{dir_name} Bot")
    text = text.replace("%APP_ID%", str(uuid.uuid4()))
    f.write(text)

p = Popen(
    f'code.cmd "{parent_dir + dir_name}"',
    shell=True,
    stdin=None,
    stdout=None,
    stderr=None,
    close_fds=True,
    creationflags=DETACHED_PROCESS,
)
