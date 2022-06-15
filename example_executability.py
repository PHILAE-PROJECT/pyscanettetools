from pyscanettetools.samplequality import executability,coverage_report

traceset_grouped=[['debloquer_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1'],['ajouter_0']]
print(len(traceset_grouped))
print(executability(traceset_grouped))
print(coverage_report(traceset_grouped))
from pyscanettetools.utils_example import read_traces_csv
from pathlib import Path
traceset = read_traces_csv(Path("pyscanettetools/csv/1026-steps.csv"))
traceset2 = traceset.with_traces_grouped_by("sessionID", property=True)
print(executability(traceset2))
coverage(traceset2)
