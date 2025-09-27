import os

def remove_nuls(path):
    with open(path, "rb") as f:  
        data = f.read()

    # Replace NULs with spaces
        cleaned = data.replace(b"\x00", b"")

    with open(path, "wb") as f:   # overwrite original
        f.write(cleaned)
    
