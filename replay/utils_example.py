import csv
from pathlib import Path
import agilkia
from datetime import datetime, date, time
def read_traces_csv(path: Path,separative_token='_') -> agilkia.TraceSet:
    # print("now=", datetime.now().timestamp())
    with path.open("r") as input:
        trace1 = agilkia.Trace([])
        for line in csv.reader(input):
            # we ignore the line id.
            timestr = line[1].strip()
            timestamp = date.fromtimestamp(int(timestr) / 1000.0)
            # print(timestr, timestamp.isoformat())
            sessionID = line[2].strip()
            objInstance = line[3].strip()
            action = line[4].strip()
            paramstr = line[5].strip()
            result = line[6].strip()
            action=action+separative_token+str(result)
            # now we identify the main action, inputs, outputs, etc.
            if paramstr == "[]":
                inputs = {}
            else:
                if  paramstr.startswith("[") and paramstr.endswith("]"):
                    paramstr = paramstr[1:-1]
                inputs = {"param" : paramstr}
            if result == "?":
                outputs = {}
            else:
                outputs = {'Status': float(result)}
            others = {
                    'timestamp': timestamp,
                    'sessionID': sessionID,
                    'object': objInstance
                    }
            event = agilkia.Event(action, inputs, outputs, others)
            trace1.append(event)
    traceset = agilkia.TraceSet([])
    traceset.append(trace1)
    return traceset