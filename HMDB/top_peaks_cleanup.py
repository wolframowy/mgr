from bson import ObjectId
from pymongo import MongoClient


def main():
    # Connect to database and access spectra collection
    client = MongoClient('localhost', 27017)
    db = client.hmdb
    all_spectra = db.hmdb_spectra

    counter = 0
    for spectrum in all_spectra.find():
        counter += 1
        # Update the spectrum with new list of top peaks
        all_spectra.update_one({'_id': ObjectId(spectrum['_id'])}, {'$unset': {'top_peaks': []}})

        if counter % 10000 == 0:
            print(counter)


if __name__ == '__main__':
    main()
