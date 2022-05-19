# -*- coding: utf-8 -*-
import os

def main() -> int:
    pycaches = []
    for fromDir, hereDir, files in os.walk("."):
        for filename in files:
            filepath = os.path.join(fromDir, filename)
            if filepath.endswith(".pyc"):
                os.remove(filepath)
                print(f"del file => {filepath}")
            else:
                pass
        if fromDir.endswith("__pycache__"):
            pycaches.append(fromDir)

    for pycache in pycaches:
        os.removedirs(pycache)
        print(f"del dir => {pycache}")

    os.system("pause")
    return 0

if __name__ == "__main__":
    main()