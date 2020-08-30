from pymongo import MongoClient, ReplaceOne
import re
import json
import time
import datetime
import pprint
import numpy as np
import matplotlib.pyplot as plt
from efficient_apriori import apriori
import sys
from collections import defaultdict
from typing import List


def check_ev_variations(mode: str, spectra):
    to_search_col = spectra.collection.find({'ms_ms.ionization_mode': re.compile(mode, re.IGNORECASE)}).collection
    if to_search_col.find_one({'ms_ms.collision_energy_voltage': 10}) is not None:
        if to_search_col.find_one({'ms_ms.collision_energy_voltage': 20}) is not None:
            if to_search_col.find_one({'ms_ms.collision_energy_voltage': 40}) is not None:
                return True
    return False


class DbOperator:

    def __init__(self, db_server, db_port, db_user, db_pwd, db_auth_source):
        self.mongo_client = MongoClient(db_server, db_port,
                                        username=db_user, password=db_pwd, authSource=db_auth_source)
        self.hmdb = self.mongo_client.hmdb

    def insert_met_id_to_spec(self):
        met_count = self.hmdb.hmdb_metabolite.count_documents({})
        metabolites = self.hmdb.hmdb_metabolite.find()
        spectra = self.hmdb.hmdb_spectra
        it = 1
        for met in metabolites:
            if met['spectra'] is not None:
                for spectrum in met['spectra']['spectrum']:
                    spectra.update_one({'id': int(spectrum['spectrum_id'])}, {'$set': {'met_id': met['id']}})
            print(f'Met {it} / {met_count}')
            it += 1
        return

    def count_mets_with_10_20_40(self):
        spectra_col = self.hmdb.hmdb_spectra
        met_ids = spectra_col.distinct('met_id')
        print(f'{len(met_ids)} distinct metabolites with at least one spectrum')
        pos_count = 0
        neg_count = 0
        both_count = 0
        for idx, met_id in enumerate(met_ids):
            print(f'{idx} / {len(met_ids)}')
            spectra = spectra_col.find({'met_id': met_id})
            is_pos = check_ev_variations('positive', spectra)
            is_neg = check_ev_variations('negative', spectra)
            if is_pos:
                pos_count += 1
                if is_neg:
                    neg_count += 1
                    both_count += 1
            elif is_neg:
                neg_count += 1

        print(f'{pos_count} of positives \n {neg_count} of negatives \n {both_count} of both')

    def find_met_wo_spectra(self):
        metabolites = self.hmdb.hmdb_metabolite.find({'$or': [
            {'$or': [{'spectra': {'$exists': False}}, {'spectra': None}]}
        ]})
        print(metabolites.count())

    def calculate_distances(self):
        with self.mongo_client.start_session() as session:
            batch_size = 10000
            spectra = self.hmdb.hmdb_spectra.find({'met_id': {'$exists': True}}, no_cursor_timeout=True, batch_size=batch_size)
            start = time.perf_counter()
            try:
                count = spectra.count()
                batch_request = []
                for spec_idx, spectrum in enumerate(spectra):
                    current = time.perf_counter()
                    if spectrum['ms_ms']['collision_energy_voltage'] in [10, 20, 40]:
                        if 'ms_ms_peaks' in spectrum['ms_ms']:
                            distances = []
                            peaks = spectrum['ms_ms']['ms_ms_peaks']['ms_ms_peak']
                            highest_peak = max(peaks, key=lambda x: x['intensity'])
                            for peaks_idx, peak in enumerate(peaks):
                                if peaks[peaks_idx]['intensity'] / highest_peak['intensity'] <= 0.02:
                                    peaks.pop(peaks_idx)
                            for peaks_idx, peak in enumerate(peaks):
                                for i in range(peaks_idx + 1, len(peaks) - 1):
                                    distances.append(abs(peaks[peaks_idx]['mass_charge'] - peaks[i]['mass_charge']))
                            distances.sort(reverse=True)
                            batch_request.append({
                                'id': spectrum['id'],
                                'met_id': spectrum['met_id'],
                                'collision_energy_voltage': spectrum['ms_ms']['collision_energy_voltage'],
                                'ionization_mode': spectrum['ms_ms']['ionization_mode'],
                                'distances': distances
                                })
                    if spec_idx % batch_size == 0:
                        self.mongo_client.admin.command(
                            'refreshSessions', [session.session_id], session=session)
                        print(f'[{datetime.timedelta(seconds=current - start)}] {spec_idx} / {count} Bulk write start')
                        self.hmdb.hmdb_spectra_distance.insert_many(batch_request)
                        print(f'[{datetime.timedelta(seconds=current - start)}] {spec_idx} / {count} Bulk write end')
                        batch_request = []
                print('Finished calculating and inserting distances')
            except Exception:
                print(f'[{datetime.timedelta(seconds=current - start)}] {spec_idx} / {count} ERROR!')
                raise
            finally:
                spectra.close()

    def rem_short_and_round_distances(self):
        self.hmdb.hmdb_spectra_distance_filtered.drop()
        spectra = self.hmdb.hmdb_spectra_distance.find({})
        count = self.hmdb.hmdb_spectra_distance.count_documents({})
        for idx, spectrum in enumerate(spectra):
            new_dist = []
            for distance in spectrum['distances']:
                if distance >= 16.5:
                    new_dist.append(round(distance))
            spectrum['distances'] = new_dist
            self.hmdb.hmdb_spectra_distance_filtered.insert_one(spectrum)
            print(f'{idx} / {count}')

    def count_distances_instances(self):
        spec_dist = self.hmdb.hmdb_spectra_distance_filtered.find({})
        count = self.hmdb.hmdb_spectra_distance_filtered.count_documents({})
        for i, spectrum in enumerate(spec_dist):
            distances = spectrum['distances']
            dist_count = defaultdict(int)
            for distance in distances:
                dist_count[str(distance)] += 1
            spectrum.pop('distances', None)
            spectrum['distance_count'] = dist_count
            self.hmdb.hmdb_spectra_distance_count.insert_one(spectrum)
            print(f'{i} / {count}')

    def count_global_dist_instances(self):
        cur = self.hmdb.hmdb_metabolite.find({'taxonomy.super_class': 'Lipids and lipid-like molecules'}, {'id': 1, '_id': 0})
        ids = [x['id'] for x in list(cur)]
        print(len(ids))
        spec_dist = self.hmdb.hmdb_spectra_distance_count.find({'met_id': {'$in': ids}})
        count = self.hmdb.hmdb_spectra_distance_count.count_documents({})
        global_dist_count = dict()
        global_dist_count['positive'] = {'10': defaultdict(int), '20': defaultdict(int), '40': defaultdict(int)}
        global_dist_count['negative'] = {'10': defaultdict(int), '20': defaultdict(int), '40': defaultdict(int)}
        global_dist_count['n/a'] = {'10': defaultdict(int), '20': defaultdict(int), '40': defaultdict(int)}
        for i, spectrum in enumerate(spec_dist):
            distance_count = spectrum['distance_count']
            to_write = global_dist_count[spectrum['ionization_mode'].lower()][str(spectrum['collision_energy_voltage'])]
            for key, value in distance_count.items():
                to_write[key] += value
            print(f'{i} / {count}')
        self.hmdb.hmdb_spectra_distance_lipid_count.insert_one(global_dist_count)

    def print_count_to_file(self):
        global_count = self.hmdb.hmdb_spectra_distance_lipid_count.find({})[0]
        global_count.pop('_id')
        to_show = {}
        for key, value in global_count.items():
            to_show[key] = {}
            for k, v in value.items():
                # to_show[key][k] = sorted(value[k].items(), key=lambda item: item[1], reverse=True)[:10]
                if key != 'n/a':
                    sys.stdout = open('lipid_count_' + key[0] + '_' + k + '.csv', 'w')
                    print('distance, count')
                    for dist, item in v.items():
                        print(f'{dist}, {item}')
        # pprint.pprint(to_show)

    def apriori_alg(self, super_class: str, voltage: int, ionization: str):
        """
        Function calculating association between distances
        :param voltage: collision energy voltage
        :param ionization: ionization mode
        """
        cur = self.hmdb.hmdb_metabolite.find({'taxonomy.super_class': super_class}, {'id': 1, '_id': 0})
        ids = [x['id'] for x in list(cur)]
        print(len(ids))
        # preprocess data
        spec_dist = self.hmdb.hmdb_spectra_distance_filtered.find({
            'met_id': {'$in': ids},
            'collision_energy_voltage': voltage,
            'ionization_mode': re.compile(ionization, re.IGNORECASE)})
        count = spec_dist.count()
        data = []
        print(f'Preprocessing for {voltage} eV and {ionization} mode started')
        for idx, spectrum in enumerate(spec_dist):
            data.append(tuple(spectrum['distances']))
            print(f'{idx} / {count}')
        print(f'Preprocessing for {voltage} eV and {ionization} mode ended')

        # apriori
        itemsets, rules = apriori(data, min_support=0.1, min_confidence=0.5, max_length=3, verbosity=1)
        print(len(rules))
        # print(rules)
        sys.stdout = open('apriori.csv', 'w')
        rules_sorted = sorted(rules, key=lambda rule: rule.lift)
        for rule in rules_sorted:
            print(rule)  # Prints the rule and its confidence, support, lift, ...

    def find_group(self, e_v: int, mode: str, dists: List[int]):
        spec_dist = self.hmdb.hmdb_spectra_distance_filtered.find({
            'collision_energy_voltage': e_v,
            'ionization_mode': re.compile(mode, re.IGNORECASE),
            'distances': {'$all': dists}
        })
        met_ids = []
        for spec in spec_dist:
            met_ids.append(spec['met_id'])
        print(f'Count: {len(met_ids)}')
        mets = self.hmdb.hmdb_metabolite.find({
            'id': {'$in': met_ids}
        })
        taxonomy = {
            'direct_parent': defaultdict(int),
            'kingdom': defaultdict(int),
            'super_class': defaultdict(int),
            'main_class': defaultdict(int),
            'sub_class': defaultdict(int)
        }
        for met in mets:
            if met['taxonomy'] is not None:
                taxonomy['direct_parent'][met['taxonomy']['direct_parent']] += 1
                taxonomy['kingdom'][met['taxonomy']['kingdom']] += 1
                taxonomy['super_class'][met['taxonomy']['super_class']] += 1
                taxonomy['main_class'][met['taxonomy']['main_class']] += 1
                taxonomy['sub_class'][met['taxonomy']['sub_class']] += 1
        with open(f'group_{mode[0]}_{e_v}_{dists[0]}_{dists[1]}.json', 'w') as f:
            f.write(json.dumps(taxonomy, indent=4))

        print(taxonomy)
        return


def main():
    db_operator = DbOperator('localhost', 27017, 'admin', 'Haslodomongodb1', 'admin')
    # db_operator.insert_met_id_to_spec()
    # db_operator.find_met_wo_spectra()
    # db_operator.count_mets_with_10_20_40()
    # db_operator.calculate_distances()
    # db_operator.rem_short_and_round_distances()
    # db_operator.count_distances_instances()
    # db_operator.count_global_dist_instances()
    # db_operator.print_count_to_file()
    db_operator.apriori_alg('Lipids and lipid-like molecules', 10, 'positive')
    # db_operator.find_group(e_v=10, mode='positive', dists=[40, 18])
    return


if __name__ == '__main__':
    main()
