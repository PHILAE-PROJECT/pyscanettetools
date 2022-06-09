from replay.utils_replay import list_of_traces_to_dict,abstract2parameters
from agilkia import TraceSet
from replay.utils_executor import OneTraceExecutor
from coverage import Coverage

def executability(traceset_grouped,separative_token='_'):

    if type(traceset_grouped)==TraceSet:
        list_of_traces = []
        for tr in traceset_grouped:
            list_of_traces.append([ev.action for ev in tr.events])
    elif type(traceset_grouped)==list and type(traceset_grouped[0])==list:
        list_of_traces=traceset_grouped
    else:
        raise ValueError("traceset_grouped should be an agilkia trace or a list of list")
    errors = 0
    executed_sessions = 0
    error_keys=[]
    original_len=len(list_of_traces)
    list_of_traces=abstract2parameters(list_of_traces,separative_token=separative_token)

    traces_dict=list_of_traces_to_dict(list_of_traces)

    for k, v in traces_dict.items():

        o = OneTraceExecutor()
        o.setUp()
        o.SEQ = v
        try:
            o.test_one_trace_as_test()
            executed_sessions += 1
        except:
            error_keys.append(k)
            errors += 1

    return executed_sessions

    # print('---- Errors', errors)
    # print('---- Session Id(s) who failed at being executed as a test :'+str(error_keys))




def coverage(traceset_grouped,separative_token='_'):
    """

    :param path: path of the traces that will be analyzed by Coverage.py
    :param filetype: csv or json
    :return: None, Print the Coverage.py report, Generate a HTML report ./htmlcov/index.html
    """

    if type(traceset_grouped)==TraceSet:
        list_of_traces = []
        print("detected traceset")
        for tr in traceset_grouped:
            list_of_traces.append([ev.action for ev in tr.events])
    elif type(traceset_grouped)==list and type(traceset_grouped[0])==list:
        list_of_traces=traceset_grouped
    else:
        raise ValueError("traceset_grouped should be an agilkia trace or a list of list")
    errors = 0
    executed_sessions = 0
    error_keys=[]
    original_len=len(list_of_traces)
    list_of_traces=abstract2parameters(list_of_traces,separative_token=separative_token)

    traces_dict=list_of_traces_to_dict(list_of_traces)

    cov = Coverage()
    cov.start()
    errors = 0
    executed_sessions = 0
    error_keys=[]
    for k, v in traces_dict.items():

        o = OneTraceExecutor()
        o.setUp()
        o.SEQ = v
        try:
            o.test_one_trace_as_test()
            executed_sessions += 1
        except:
            error_keys.append(k)
            errors += 1



    cov.stop()

    cov.html_report(directory='../htmlcov')
    print("-- COVERAGE.PY API REPORT :")
    print(cov.report())



if __name__=='__main__':
    traceset_grouped=[['debloquer_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1'],['ajouter_0']]
    print(len(traceset_grouped))
    print(executability(traceset_grouped))
    print(coverage(traceset_grouped))
    from utils_example import read_traces_csv
    from pathlib import Path
    traceset = read_traces_csv(Path("../csv/1026-steps.csv"))
    traceset2 = traceset.with_traces_grouped_by("sessionID", property=True)
    print(executability(traceset2))
    coverage(traceset2)
