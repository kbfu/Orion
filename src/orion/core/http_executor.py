import yaml
import string
import json
import re
from types import FunctionType
from ..components.http.http import execute
from os.path import basename


def run(test_file, container, env):
    with open(test_file, encoding='utf-8') as f:
        test_load = yaml.load(f)
    for k, v in test_load.items():
        duration = v['duration']
        rate = v['rate']
        workers = v['workers']

        dumped_data = json.dumps(v, ensure_ascii=False)
        matches = re.findall(r'\${[^}${]*}', dumped_data)
        data_list = []
        for _ in range(duration * rate):
            substitution = {}
            for m in matches:
                if isinstance(getattr(container, m[2:-1]), FunctionType):
                    substitution[m[2:-1]] = getattr(container, m[2:-1])()
                else:
                    substitution[m[2:-1]] = getattr(container, m[2:-1])
            test_data = json.loads(string.Template(
                dumped_data).safe_substitute(substitution), encoding='utf-8')
            test_data.pop('duration')
            test_data.pop('rate')
            test_data.pop('workers')
            data_list.append(test_data)

        execute(container.pegasus_hosts, test_data, env,
                workers, rate, basename(test_file).split('.')[0], k)
