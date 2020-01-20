from bson import ObjectId
from pymongo import MongoClient


def main():
    # Connect to database and access spectra collection
    client = MongoClient('localhost', 27017)
    db = client.hmdb
    all_spectra = db.hmdb_spectra

    counter = 0
    for spectrum in all_spectra.find():
        if 'top_peaks' in spectrum:
            #print(f'Spectrum already updated {spectrum["_id"]}')
            continue

        counter = counter + 1
        # Get peak list

        try:
            peak_list = spectrum['ms_ms']['ms_ms_peaks']['ms_ms_peak']
        except KeyError:
            print(f'Cannot find peak list in spectrum {spectrum["_id"]}')
            continue

        # Sort peak list by intensity ascending
        peak_list.sort(key=lambda x: x['intensity'], reverse=True)
        # Get intensities
        intensity_list = [x['intensity'] for x in peak_list]
        # Calculate intensities that matter
        max_intensity = intensity_list[0]
        cutoff_intensity = max_intensity * 0.05

        # Create a list of proper intensities that define this spectrum and get top 10 elements
        filtered_list = [x for x in intensity_list if x > cutoff_intensity]
        if len(filtered_list) > 10:
            filtered_list = filtered_list[0:10]

        mass_charge_list = []
        for peak in peak_list:
            if peak['intensity'] in filtered_list:
                mass_charge_list.append(peak['mass_charge'])



        # Update the spectrum with new list of top peaks
        all_spectra.update_one({'_id': ObjectId(spectrum['_id'])}, {'$set': {'top_peaks': mass_charge_list}})

        if counter % 10000 == 0:
            print(counter)


if __name__ == '__main__':
    main()
