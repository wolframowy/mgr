from bson import ObjectId
from pymongo import MongoClient


def find_spectrum(peak_list, tolerance):
    # Connect to database and access spectra collection
    client = MongoClient('localhost', 27017)
    db = client.hmdb
    all_spectra = db.hmdb_spectra

    all_candidates = []
    already_seen_ids = []
    for peak in peak_list:
        for spectrum in all_spectra.find(
                {'top_peaks': {'$elemMatch': {'$gt': peak - tolerance, '$lt': peak + tolerance}}}):
            if str(spectrum['_id']) not in already_seen_ids:
                all_candidates.append(spectrum)
                already_seen_ids.append(str(spectrum['_id']))

    ranked_canditates = {}
    for candidate in all_candidates:
        candidte_peaks = candidate['top_peaks']
        ranking = 0
        for candidate_peak in candidte_peaks:
            for search_peak in peak_list:
                if candidate_peak > search_peak - tolerance and candidate_peak < search_peak + tolerance:
                    ranking += 1
            ranked_canditates[candidate['id']] = ranking

    final_candidates = [x for x in ranked_canditates.keys() if ranked_canditates[x] == len(peak_list)]
    if len(final_candidates) == 0:
        counter = 0
        while len(final_candidates) == 0 and counter < len(peak_list):
            counter +=1
            final_candidates = [x for x in ranked_canditates.keys() if ranked_canditates[x] == len(peak_list)-counter]

    return final_candidates

    pass


def find_metablites(spectra_list):
    # Connect to database and access spectra collection
    client = MongoClient('localhost', 27017)
    db = client.hmdb
    all_metabolites = db.hmdb_metabolite
    found_metabolites = {}
    found_metabolites_names = []
    for spectrum in spectra_list:
        for result in all_metabolites.find({"spectra.spectrum": {'$elemMatch': {'spectrum_id': f'{spectrum}'}}}):
            if result['accession'][0] not in found_metabolites:
                found_metabolites[result['accession'][0]] = 1
                found_metabolites_names.append(result['name'])
            else:
                found_metabolites[result['accession'][0]] += 1
    pass


def main():
    candidates = find_spectrum([102.1, 128.0, 146.0, 129.0, 148.1, 108.0, 84.0], 0.1)
    find_metablites(candidates)


if __name__ == '__main__':
    main()
