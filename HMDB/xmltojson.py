import xmltodict
import json
import zipfile
import os
import glob
import shutil

NIL = {
    "@nil": "true"
}


def change_boolean(val):
    if val == "true":
        return True
    elif val == "false":
        return False


def change_vals_in_list(content):
    new = []
    for idx, val in enumerate(content):
        if val == NIL:
            val = None
        elif val == "true" or val == "false":
            val = change_boolean(val)
        elif isinstance(val, dict):
            val = change_vals_in_obj(val)
        elif isinstance(val, list):
            val = change_vals_in_list(val)
        new.append(val)
    return new


def change_vals_in_obj(content):
    new = {}
    for k, v in content.items():
        if v == NIL:
            v = None
        elif v == "true" or v == "false":
            v = change_boolean(v)
        elif isinstance(v, dict):
            v = change_vals_in_obj(v)
        elif isinstance(v, list):
            v = change_vals_in_list(v)
        new[k.replace('-', '_')] = v
    return new


def files_to_array(name):
    print('Started gathering name list')
    names = glob.glob(name + "/*.json")
    print('Finished gathering name list')
    first = True
    print('Started converting spectras to single array file')
    print(" 0 / " + str(names.__len__()))
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


def file_to_json():
    filename = "hmdb_metabolites/hmdb_metabolites"
    with open(filename + ".json", "w") as outfile:
        content = xmltodict.parse(open(filename + ".xml", "rb"))
        change_nil(content)
        json.dump(content, outfile, indent=1)


def spectras_to_json():
    dirname = "hmdb_all_spectra"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    zipfilename = dirname + ".zip"
    archive = zipfile.ZipFile(zipfilename, "r")
    for idx, name in enumerate(archive.namelist()):
        if name.find(".xml") != -1:
            with open(name.replace(".xml", ".json"), "w") as outfile:
                content = xmltodict.parse(archive.open(name))
                content = change_vals_in_obj(content)
                json.dump(content, outfile, indent=1)
        if idx % 1000 == 0:
            print(" " + str(idx) + " / " + str(archive.namelist().__len__()))
    files_to_array(name=dirname)


def metabolites_to_json():
    zipfilename = "hmdb_metabolites.zip"
    archive = zipfile.ZipFile(zipfilename, "r")
    for name in archive.namelist():
        if name.find(".xml") != -1:
            print(name.replace(".xml", ".json"))
            with open(name.replace(".xml", ".json"), "w") as outfile:
                outfile.write("[\n")
                content = xmltodict.parse(archive.open(name))
                content = content['hmdb']['metabolite']
                first = True
                print('Started replacing NIL objects with Nones')
                for metabolite in content:
                    if first:
                        first = False
                    else:
                        outfile.write(",\n")
                    json.dump(change_vals_in_obj(metabolite), outfile, indent=1)
                first = False
                outfile.write("\n]")
                print('Finished replacing NIL objects with Nones')


if __name__ == "__main__":
    spectras_to_json()
    metabolites_to_json()
