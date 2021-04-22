import re
import zipfile

if __name__ == '__main__':
    files = {}
    with zipfile.ZipFile('http://www.pythonchallenge.com/pc/def/channel.zip') as file:
        for name in file.namelist():
            with file.open(name) as f:
                files[name] = f.read().decode("utf-8")
        nothing = "90052"
        while True:
            f = nothing + ".txt"
            print(file.getinfo(f).comment.decode("utf-8"), end="")
            if f in files:
                result = re.search(r"Next nothing is (\d+)", files[f])
                try:
                    nothing = result.group(1)
                except:
                    break
