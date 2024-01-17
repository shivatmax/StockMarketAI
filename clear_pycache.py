import os
import shutil


def clear_pycache():
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name == "__pycache__":
                pycache_dir = os.path.join(root, name)
                print(f"Removing {pycache_dir}")
                shutil.rmtree(pycache_dir)
                
                
