from bson import ObjectId
from pymongo import MongoClient


class MetaboliteFinder:
    def __init__(self, database_server, database_port):
        self.mongo_client = MongoClient(database_server, database_port)

    def find_metabolite_by_id(self, id):
        database = self.mongo_client.hmdb
        all_metabolites_collection = database.hmdb_metabolite
        results = []
        for result in all_metabolites_collection.find(
                {"id": id}):
            results.append(result)
        return results[0]

    def get_spectrum_data(self, spectrum_id, peaks, tolerance):
        database = self.mongo_client.hmdb
        all_spectra_collection = database.hmdb_spectra
        spectra = []
        for spectrum in all_spectra_collection.find({'id': int(spectrum_id)}):
            spectra.append(spectrum)
        spectrum_peaks = spectra[0]['top_peaks']
        matched_peaks = set()
        # checking every combination of peak matches
        for candidate_peak in spectrum_peaks:
            for search_peak in peaks:
                if search_peak - tolerance < candidate_peak < search_peak + tolerance:
                    # counting how many spectrum peaks match the search parameters
                    matched_peaks.add(search_peak)

        collision_energy_voltage = None
        ionization_mode = None
        if 'collision_energy_voltage' in spectra[0]['ms_ms']:
            collision_energy_voltage = spectra[0]['ms_ms']['collision_energy_voltage']
        if 'ionization_mode' in spectra[0]['ms_ms']:
            ionization_mode = spectra[0]['ms_ms']['ionization_mode']

        return len(matched_peaks), collision_energy_voltage, ionization_mode

    def _find_spectra(self, peak_list, tolerance):
        """
        Returns a dict of ranking to list of spectra.
        Ranking is based on how many peaks in spectrum match the search parameters
        """

        # Connect to database and access spectra collection
        database = self.mongo_client.hmdb
        all_spectra_collection = database.hmdb_spectra

        all_candidates = []
        already_seen_ids = []
        for peak in peak_list:
            # Searching for spectra with at least one matching peak
            for spectrum in all_spectra_collection.find(
                    {'top_peaks': {'$elemMatch': {'$gt': peak - tolerance, '$lt': peak + tolerance}}}):
                if str(spectrum['_id']) not in already_seen_ids:
                    all_candidates.append(spectrum)
                    already_seen_ids.append(str(spectrum['_id']))

        # ranking spectra based on the number of matching peaks
        ranked_candidates = {}
        for candidate in all_candidates:
            candidate_peaks = candidate['top_peaks']
            matched_peaks = set()
            # checking every combination of peak matches
            for candidate_peak in candidate_peaks:
                for search_peak in peak_list:
                    if search_peak - tolerance < candidate_peak < search_peak + tolerance:
                        # counting how many spectrum peaks match the search parameters
                        matched_peaks.add(search_peak)
            if len(matched_peaks) not in ranked_candidates.keys():
                ranked_candidates[len(matched_peaks)] = []
            ranked_candidates[len(matched_peaks)].append(candidate['id'])
        return ranked_candidates

    def find_metabolites(self, peak_list, tolerance, minimum_ranking):
        ranked_candidates = self._find_spectra(peak_list, tolerance)
        top_candidates = {}

        # Getting at least a specified amount of spectra to have a wide range of results
        total_candidates = 0
        current_ranking = max(ranked_candidates.keys())
        while current_ranking >= minimum_ranking:
            top_candidates[current_ranking] = ranked_candidates[current_ranking]
            total_candidates += len(ranked_candidates[current_ranking])
            current_ranking -= 1

        database = self.mongo_client.hmdb
        all_metabolites_collection = database.hmdb_metabolite
        found_metabolites = {}
        found_metabolites_ids = {}
        found_metabolites_names = {}
        for ranking in top_candidates.keys():
            found_metabolites[ranking] = []
            found_metabolites_ids[ranking] = []
            found_metabolites_names[ranking] = []

        for ranking in top_candidates.keys():
            for spectrum in top_candidates[ranking]:
                for result in all_metabolites_collection.find(
                        {"spectra.spectrum": {'$elemMatch': {'spectrum_id': f'{spectrum}'}}}):
                    if result['accession'][0] not in found_metabolites_ids[ranking]:
                        found_metabolites[ranking].append(result)
                        found_metabolites_ids[ranking].append(result['accession'][0])
                        found_metabolites_names[ranking].append(result['name'])

        return (found_metabolites, found_metabolites_names, found_metabolites_ids)


def main():
    metabolite_finder = MetaboliteFinder('localhost', 27017)
    _, found_metabolites_names, _ = metabolite_finder.find_metabolites(peak_list=[148, 131.2, 130, 102.1, 84.1],
                                                                       tolerance=0.1,
                                                                       minimum_ranking=1)
    print(found_metabolites_names)


if __name__ == '__main__':
    main()
