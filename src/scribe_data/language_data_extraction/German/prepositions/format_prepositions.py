"""
Formats the German prepositions queried from Wikidata using query_prepositions.sparql.
"""

import collections
import os
import sys

from scribe_data.utils import (
    export_formatted_data,
    load_queried_data,
    map_cases,
    order_annotations,
)

file_path = sys.argv[0]

prepositions_list, update_data_in_use, data_path = load_queried_data(
    file_path=file_path, language="German", data_type="prepositions"
)

prepositions_formatted = {}

for prep_vals in prepositions_list:
    if "preposition" in prep_vals.keys():
        if "case" in prep_vals.keys():
            if prep_vals["preposition"] not in prepositions_formatted:
                prepositions_formatted[prep_vals["preposition"]] = map_cases(
                    prep_vals["case"]
                )

            else:
                prepositions_formatted[prep_vals["preposition"]] += "/" + map_cases(
                    prep_vals["case"]
                )

        elif (
            "case" not in prep_vals.keys() and prep_vals["preposition"] != "a"
        ):  # à is the correct preposition
            prepositions_formatted[prep_vals["preposition"]] = ""

for k in prepositions_formatted:
    prepositions_formatted[k] = order_annotations(prepositions_formatted[k])

    # Contracted versions of German prepositions (ex: an + dem = am).
contractedGermanPrepositions = {
    "am": "Acc/Dat",
    "ans": "Acc/Dat",
    "aufs": "Acc/Dat",
    "beim": "Dat",
    "durchs": "Acc",
    "fürs": "Acc",
    "hinters": "Acc/Dat",
    "hinterm": "Acc/Dat",
    "ins": "Acc/Dat",
    "im": "Acc/Dat",
    "übers": "Acc/Dat",
    "überm": "Acc/Dat",
    "ums": "Acc",
    "unters": "Acc/Dat",
    "unterm": "Acc/Dat",
    "vom": "Dat",
    "vors": "Acc/Dat",
    "vorm": "Acc/Dat",
    "zum": "Dat",
    "zur": "Dat",
}

for p in contractedGermanPrepositions:
    if p not in prepositions_formatted:
        prepositions_formatted[p] = contractedGermanPrepositions[p]

prepositions_formatted = collections.OrderedDict(sorted(prepositions_formatted.items()))

export_formatted_data(
    formatted_data=prepositions_formatted,
    update_data_in_use=update_data_in_use,
    language="German",
    data_type="prepositions",
)

os.remove(data_path)