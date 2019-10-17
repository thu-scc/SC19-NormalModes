import os
import time
import subprocess

import parse_output

current_dataset = 'None'
dataset = None
datasets = {}

def model_log(model):
    return os.path.join(log_dir, '{}_{}_{}_{}.log'.format(model['label'], model['nodes'], model['ranks'], model['threads']))

def get_model(label):
    for model in dataset['models']:
        if model['label'] == label:
            return model
    return None

def generate_global_conf(model):
    global_conf = ''
    global_conf += 'JOB = {}\n'.format(model['JOB'])               ; print('[-]     JOB={}'.format(model['JOB']))
    global_conf += 'basename = {}\n'.format(model['basename'])     ; print('[-]     basename={}'.format(model['basename']))
    if not model['inputdir'].endswith('/'):
        model['inputdir'] += '/'
    if not model['outputdir'].endswith('/'):
        model['outputdir'] += '/'        
    global_conf += 'inputdir = {}\n'.format(model['inputdir'])     ; print('[-]     inputdir={}'.format(model['inputdir']))
    global_conf += 'outputdir = {}\n'.format(model['outputdir'])   ; print('[-]     outputdir={}'.format(model['outputdir']))
    global_conf += 'lowfreq = {}\n'.format(model['lowfreq'])       ; print('[-]     lowfreq={}'.format(model['lowfreq']))
    global_conf += 'upfreq = {}\n'.format(model['upfreq'])         ; print('[-]     upfreq={}'.format(model['upfreq']))
    global_conf += 'pOrder = {}\n'.format(model['pOrder'])         ; print('[-]     pOrder={}'.format(model['pOrder']))
    return global_conf

def pre_check():
    if not os.path.exists(log_dir):
        print('Log directory {} does not exist, created'.format(log_dir))
        os.makedirs(log_dir)

def check():
    if dataset == None:
        print('No dataset selected')
        return
    logs = os.listdir(log_dir)
    logs.sort()
    models = dataset['models']
    for model in models:
        model['status'] = 'NOT STARTED'
    for log in logs:
        if not log.endswith('.log'): continue
        label = log.split('_')[0]
        status = 'UNFINISHED'
        with open(os.path.join(log_dir, log), 'r') as f:
            if f.read().find('save the results') != -1:
                status = 'DONE'
        for model in models:
            if model['label'] == label:
                model['status'] = status
    print('Current status:')
    for model in models:
        print('- {}: {}'.format(model['label'], model['status']))

def parse(label):
    if dataset == None:
        print('No dataset selected')
        return
    model = get_model(label)
    try:
        parse_output.parse_output(model_log(model), True, label, model['nodes'], model['ranks'])
    except:
        print('Error while parsing')

def switch_dataset(name):
    global current_dataset, dataset
    current_dataset = name
    if not name in datasets:
        print('Invalid dataset')
    else:
        dataset = datasets[name]
        print('Dataset switched to {}'.format(name))

def plot_weak():
    pass

def plot():
    if dataset == None:
        print('No dataset selected')
    else:
        dataset['plot']()

def show():
    print('Current dataset: {}'.format(str(current_dataset)))

def run(label):
    if dataset == None:
        print('No dataset selected')
        return
    nodes_list = input('> Input list of nodes: ')
    model = get_model(label)
    if len(nodes_list.split(',')) != model['nodes']:
        print('Numbers of nodes do not match')
        return
    bash = ''
    bash += '#!/bin/bash\n'
    bash += 'export OMP_NUM_THREADS={}\n'.format(model['threads'])
    bash += env_cmd
    run_cmd = 'mpirun -n {} -hosts {} {}'.format(model['nodes'] * model['ranks'], nodes_list, bin_path)
    bash += run_cmd
    print('Command will be: {}'.format(run_cmd))
    choice = input('> Confirm? (y/n) ')
    if choice != 'y':
        print('Canceled')
        return
    with open('cluster_generated_run.sh', 'w') as f:
        f.write(bash)
    os.system('nohup bash cluster_generated_run.sh > {} 2>&1 &'.format(model_log(model)))
    print('Task submitted')

log_dir = 'logs/'
bin_path = '../bin/plmvcg_istar.out'

env_cmd = 'source /etc/profile.d/modules.sh\nsource /opt/spack/share/spack/setup-env.sh\nsource $HOME/intel_env.sh\ncd $HOME/SC19/NormalModes/demos\n'

datasets['weak'] = {
    'models': [
        {'label': 'M1', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M1', 'outputdir': 'models/output/Moon/M1', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 1, 'ranks': 56, 'threads': 1},
        {'label': 'M2', 'JOB': 2, 'basename': 'Mtopo_6L_1M.1'  , 'inputdir': 'models/input/Moon/M2', 'outputdir': 'models/output/Moon/M2', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 2, 'ranks': 56, 'threads': 1},
        {'label': 'M3', 'JOB': 2, 'basename': 'Mtopo_6L_2M.1'  , 'inputdir': 'models/input/Moon/M3', 'outputdir': 'models/output/Moon/M3', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 3, 'ranks': 56, 'threads': 1},
        {'label': 'M4', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M4', 'outputdir': 'models/output/Moon/M4', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 4, 'ranks': 56, 'threads': 1},
        {'label': 'M5', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M5', 'outputdir': 'models/output/Moon/M5', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 5, 'ranks': 56, 'threads': 1},
        {'label': 'M6', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M6', 'outputdir': 'models/output/Moon/M6', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 6, 'ranks': 56, 'threads': 1}
    ],
    "plot": plot_weak
}

if __name__ == "__main__":
    print('SCC 19, Tsinghua University, Reproduciblity Command Line')
    print('Commands: switch <experiment>, run <label>, parse <label>, show, check, plot, exit')
    print('Notes: this script must be run in demos dir, e.g.: python3 tools/cluster_run.py in demos dir')
    pre_check()
    while True:
        line = input('> ').split()
        if len(line) == 0: continue
        command = line[0]
        if command == 'exit':
            break
        elif command == 'switch':
            if len(line) < 2:
                print('Invalid args')
                continue
            switch_dataset(line[1])
        elif command == 'run':
            if len(line) < 2:
                print('Invalid args')
                continue
            run(line[1])
        elif command == 'parse':
            if len(line) < 2:
                print('Invalid args')
                continue
            parse(line[1])
        elif command == 'check':
            check()
        elif command == 'show':
            show()
        elif command == 'plot':
            plot()
        elif command == '':
            pass
        else:
            print('Invalid command')


