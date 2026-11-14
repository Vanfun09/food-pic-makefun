import shutil
import os

os.makedirs("/output", exist_ok=True)
shutil.copy("/bot/entry.png", "/output/entry.png")
