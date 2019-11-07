import glob
import shutil


def files_to_array(name):
    names = glob.glob(name + "/*.json")
    first = True
    with open(name + '.json', 'wb') as wfd:
        wfd.write(bytes("[\n", encoding="utf8"))
        for idx, f in enumerate(names):
            with open(f, 'rb') as fd:
                if first:
                    first = False
                    shutil.copyfileobj(fd, wfd)
                else:
                    wfd.write(bytes(",\n", encoding="utf8"))
                    shutil.copyfileobj(fd, wfd)
            if idx % 1000 == 0:
                print(" " + str(idx) + " / " + str(names.__len__()) + " : " + f)
        wfd.write(bytes("\n]", encoding="utf8"))
