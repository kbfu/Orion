import json
from collections import OrderedDict


def merge(reports):
    report = {}
    for r in reports:
        data = json.loads(r)
        if report:
            report['All'].extend(data['All'])
            for k in data['Tps'].keys():
                if k in report['Tps']:
                    report['Tps'][k] += data['Tps'][k]
                else:
                    report['Tps'][k] = data['Tps'][k]
            for k in data['Status'].keys():
                if k in report['Status']:
                    report['Status'][k] += data['Status'][k]
                else:
                    report['Status'][k] = data['Status'][k]
        else:
            report = data
    report['All'].sort()
    ordered = OrderedDict(sorted(report['Tps'].items()))
    report['Tps'] = dict(ordered)
    return report
