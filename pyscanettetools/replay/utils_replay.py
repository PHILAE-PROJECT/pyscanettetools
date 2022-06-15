from .utils_parameters import ParametersFiller
import csv
from agilkia import TraceSet
def list_of_traces_to_dict(list_of_events):
    traces_dict={}
    for event in list_of_events:
        if event[2] not in traces_dict:
            traces_dict[event[2]] = []
        traces_dict[event[2]].append(event)
    return traces_dict

def csv_to_dict(csv_path):
    with open(csv_path) as csv_file:
        dict_sessions = {}
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row[2] not in dict_sessions:
                dict_sessions[row[2]] = []

            dict_sessions[row[2]].append(row)
    return dict_sessions

def get_line_covered_by_files_dict(datacov):
    cov_by_file_dict=dict()
    for file_name in datacov.measured_files():
        file = open(file_name, "r")
        line_count = 0
        for line in file:
            line_count += 1
        file.close()
        lines_covered=datacov.lines(file_name)
        cov_by_file_dict[file_name]={"total_lines":line_count,"lines_covered":lines_covered}
    return cov_by_file_dict

def get_arcs_by_files_dict(datacov):
    cov_by_file_dict=dict()
    for file_name in datacov.measured_files():
        arcs=datacov.arcs(file_name)
        cov_by_file_dict[file_name]={"arcs":arcs}
    return cov_by_file_dict


def abstract2parameters(traceset_grouped,separative_token):
    """
    Fill traceset with abstract actions with real parameters

    :param traceset_grouped can be a list of list of string or a grouped agilkia traceset:
    :return:
    """

    if type(traceset_grouped)==TraceSet:
        list_of_traces = []
        for tr in traceset_grouped:
            list_of_traces.append([ev.action for ev in tr.events])
    elif type(traceset_grouped)==list and type(traceset_grouped[0])==list:
        list_of_traces=traceset_grouped
    else:
        raise ValueError("traceset_grouped should be an agilkia trace or a list of list")

    p=ParametersFiller(separative_token=separative_token)
    errors=0
    for trace in list_of_traces:
        try:
            p.decode(trace)
        except:
            errors+=1
    return p.export_list_of_traces()