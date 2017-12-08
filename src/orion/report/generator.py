import pygal
from jinja2 import Template
import os
import time

curr_dir = os.path.dirname(os.path.realpath(__file__))


def tps(report):
    line_chart = pygal.Line(width=1200, height=500, show_x_labels=False)
    start = int(list(report['Tps'].keys())[0])
    end = int(list(report['Tps'].keys())[-1])
    avg = round(len(report['All']) / (end + 1 - start), 2)
    line_chart.title = f'Transaction Per Second, Average: {avg}/s'
    line_chart.x_labels = map(lambda d: time.strftime(
        '%H:%M:%S', time.localtime(d)), range(start, end + 1))
    line_chart.add(
        'TPS', [report['Tps'][str(k)] if str(k) in report['Tps'].keys() else None for k in range(start, end + 1)])
    return line_chart


def response_time(report):
    bar_chart = pygal.HorizontalBar(width=1200, height=500)
    bar_chart.title = 'Response Times (ms)'
    size = len(report['All'])
    average = round(sum(report['All']) / size, 2)
    med = report['All'][round(size * 0.5) - 1]
    minimum = report['All'][0]
    maximum = report['All'][-1]
    ninety = report['All'][round(size * 0.9) - 1]
    ninety_five = report['All'][round(size * 0.95) - 1]
    ninety_nine = report['All'][round(size * 0.99) - 1]
    bar_chart.add('Average', average)
    bar_chart.add('Median', med)
    bar_chart.add('Min', minimum)
    bar_chart.add('Max', maximum)
    bar_chart.add('90%', ninety)
    bar_chart.add('95%', ninety_five)
    bar_chart.add('99%', ninety_nine)
    return bar_chart


def status(report):
    bar_chart = pygal.HorizontalBar(width=1200, height=500)
    bar_chart.title = 'Status Codes'
    for k, v in report['Status'].items():
        bar_chart.add(k, v)
    return bar_chart


def generate(report, test_name, step_name, env):
    test_name = test_name.split('.')[0]
    os.makedirs(f'results/{env}/{test_name}', exist_ok=True)
    f = open(curr_dir + '/template/template.html')
    jquery = open(curr_dir + '/js/jquery-3.2.1.min.js')
    pygal = open(curr_dir + '/js/pygal-tooltips.min.js')
    semantic_css = open(curr_dir + '/js/semantic.min.css')
    semantic = open(curr_dir + '/js/semantic.min.js')
    template = Template(f.read())
    data = [tps(report).render().decode(),
            response_time(report).render().decode(),
            status(report).render().decode()]
    with open(f'results/{env}/{test_name}/{step_name}.html', 'w+') as result:
        result.write(template.render(data=data, jquery=jquery.read(),
                                     pygal=pygal.read(), semantic_css=semantic_css.read(), semantic=semantic.read()))
    f.close()
    jquery.close()
    pygal.close()
    semantic_css.close()
    semantic.close()
