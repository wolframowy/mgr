import xmltodict
import json
import zipfile

from filestoarray import files_to_array

NIL = {
    "@nil": "true"
}


def change_nil(content):
    for k, v in content.items():
        if v == NIL:
            content[k] = None
        elif isinstance(v, dict):
            change_nil(v)


def file_to_json():
    filename = "hmdb_metabolites/hmdb_metabolites"
    with open(filename + ".json", "w") as outfile:
        content = xmltodict.parse(open(filename + ".xml", "rb"))
        change_nil(content)
        json.dump(content, outfile, indent=1)


def spectras_to_json():
    name = "hmdb_all_spectra"
    zipfilename = name + ".zip"
    archive = zipfile.ZipFile(zipfilename, "r")
    for name in archive.namelist():
        if name.find(".xml") != -1:
            print(name.replace(".xml", ".json"))
            with open(name.replace(".xml", ".json"), "w") as outfile:
                content = xmltodict.parse(archive.open(name))
                change_nil(content)
                json.dump(content, outfile, indent=1)
    files_to_array(name=name)


def metabolites_to_json():
    zipfilename = "hmdb_metabolites.zip"
    archive = zipfile.ZipFile(zipfilename, "r")
    for name in archive.namelist():
        if name.find(".xml") != -1:
            print(name.replace(".xml", ".json"))
            with open(name.replace(".xml", ".json"), "w") as outfile:
                content = xmltodict.parse(archive.open(name))
                change_nil(content)
                json.dump(content['hmdb']['metabolite'], outfile, indent=1)


if __name__ == "__main__":
    metabolites_to_json()
