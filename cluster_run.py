import os
import time
import subprocess

import matplotlib as mpl
mpl.use('Agg')

import parse_output
from plot_result import plot_weak, plot_fix, plot_strong

current_dataset = 'None'
dataset = None
datasets = {}

def get_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def model_log(model):
    return os.path.join(log_dir, '{}_{}_{}_{}_{}.log'.format(model['label'], model['nodes'], model['ranks'], model['threads'], get_time()))

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
    print('Current dataset: {}'.format(str(current_dataset)))
    if dataset == None:
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
        info = '- {}: {}'.format(model['label'], model['status'])
        if 'running_on' in model: info += ' (Last run on {})'.format(model['running_on'])
        print(info)

def parse(label, print_result = True):
    if dataset == None:
        print('No dataset selected')
        return
    model = get_model(label)
    if model == None:
        print("invalid model name")
        return
    try:
        out = parse_output.parse_output(model_log(model), print_result, label, model['nodes'], model['ranks'])
        model['json-log'] = out
        return True
    except:
        print('Error while parsing {}'.format(label))
        return False

def switch_dataset(name):
    global current_dataset, dataset
    current_dataset = name
    if not name in datasets:
        print('Invalid dataset')
    else:
        dataset = datasets[name]
        print('Dataset switched to {}'.format(name))

def get_valid_result():
    check()
    done = []
    for model in dataset['models']:
        if model['status'] == 'DONE' and parse(model['label'], False):
            done.append(model)
    print("Available models: {}".format([x['label'] for x in done]))
    return done

def plot(show=False):
    if (not os.path.exists("plot")):
        os.mkdir("plot")
    if dataset == None:
        print('No dataset selected')
    else:
        done = get_valid_result()
        for func in dataset['plot']:
            func(done, show)

def run(label):
    if dataset == None:
        print('No dataset selected')
        return
    model = get_model(label)
    if model == None:
        print("invalid label name")
        return
    nodes_list_str = input('> Input list of nodes: ')
    nodes_list_arr = nodes_list_str.split(',')
    if len(nodes_list_arr) != model['nodes']:
        print('Number of nodes does not match')
        return
    for node_name in nodes_list_arr:
        if not node_name in available_nodes:
            print('Invalid node {}'.format(node_name))
            return
    global_conf = generate_global_conf(model)
    with open('global_conf', 'w') as f:
        f.write(global_conf)
    bash = ''
    bash += '#!/bin/bash\n'
    bash += 'export OMP_NUM_THREADS={}\n'.format(model['threads'])
    bash += env_cmd
    run_cmd = 'I_MPI_PIN=yes I_MPI_PIN_PROCESSOR_LIST=allcores:map=bunch mpirun -n {} -hosts {} bash -c "ulimit -s unlimited && {}"'.format(model['nodes'] * model['ranks'], nodes_list_str, bin_path)
    bash += run_cmd
    print('Command will be: {}'.format(run_cmd))
    choice = input('> Confirm? (y/n) ')
    if choice != 'y':
        print('Canceled')
        return
    with open('cluster_generated_run.sh', 'w') as f:
        f.write(bash)
    if not os.path.exists(model['outputdir']):
        print('Output directory {} does not exist, created'.format(model['outputdir']))
        os.makedirs(model['outputdir'])
    os.system('bash cluster_generated_run.sh | tee {}'.format(model_log(model)))
    model['running_on'] = nodes_list_str
    exit()

log_dir = 'logs/'
bin_path = '../bin/plmvcg_istar.out'
available_nodes = ['e1', 'e2', 'e3', 'e4']

env_cmd = 'source /etc/profile.d/modules.sh\nsource /opt/spack/share/spack/setup-env.sh\nsource $HOME/intel_env.sh\ncd $HOME/SC19/NormalModes/demos\nulimit -s unlimited\n'

datasets['final'] = {
    'models': [
        {'group': 0, 'label': 'f-w-M1-1',   'JOB': 2, 'basename': 'RTMDWAK_3L_1M.1', 'inputdir': 'final/input/M1',   'outputdir': 'final/output/M1',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 1, 'ranks': 56, 'threads': 1},
        {'group': 0, 'label': 'f-w-M2-2',   'JOB': 2, 'basename': 'RTMDWAK_3L_2M.1', 'inputdir': 'final/input/M2',   'outputdir': 'final/output/M2',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 2, 'ranks': 56, 'threads': 1},
        {'group': 0, 'label': 'f-w-M3-4',   'JOB': 2, 'basename': 'RTMDWAK_3L_16M.1', 'inputdir': 'final/input/M3',   'outputdir': 'final/output/M3',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 4, 'ranks': 56, 'threads': 1},
        {'group': 1, 'label': 'f-w-M4-1',   'JOB': 2, 'basename': 'RTMDWAK_3L_32M.1', 'inputdir': 'final/input/M4',   'outputdir': 'final/output/M4',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 1, 'ranks': 56, 'threads': 1},
        {'group': 1, 'label': 'f-w-M5-2',   'JOB': 2, 'basename': 'RTMDWAK_3L_64M.1', 'inputdir': 'final/input/M5',   'outputdir': 'final/output/M5',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 2, 'ranks': 56, 'threads': 1},
        {'group': 1, 'label': 'f-w-M6-4',   'JOB': 2, 'basename': 'RTMDWAK_3L_128M.1', 'inputdir': 'final/input/M6',   'outputdir': 'final/output/M6',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 4, 'ranks': 56, 'threads': 1},

        {'group': 2, 'label': 'f-s-M2-1',   'JOB': 2, 'basename': 'RTMDWAK_3L_2M.1', 'inputdir': 'final/input/M2',   'outputdir': 'final/output/M2-1',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 1, 'ranks': 56, 'threads': 1},
        {'group': 2, 'label': 'f-s-M2-4',   'JOB': 2, 'basename': 'RTMDWAK_3L_2M.1', 'inputdir': 'final/input/M2',   'outputdir': 'final/output/M2-4',   'lowfreq': 0.5, 'upfreq': 1.0, 'pOrder': 1, 'nodes': 4, 'ranks': 56, 'threads': 1},
    ],
    "plot": [plot_weak, plot_fix]
}

if __name__ == "__main__":
    print('SCC 19, Tsinghua University, Reproduciblity Command Line')
    print('Commands: switch <experiment>, run <label>, parse <label>, check, plot, download, exit')
    print('Notes: this script must be run in demos dir, e.g.: python3 tools/cluster_run.py in demos dir')
    pre_check()
    switch_dataset('final')
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
        elif command == 'plot':
            plot(show=(len(line) > 1))
        elif command == 'download':
            if (not os.path.exists("trash")):
                os.mkdir("trash")
            if (os.path.exists("logs")):
                cmd = "mv logs trash/logs-{}".format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
                print(cmd)
                os.system(cmd)
            cmd = "scp -r i1:~/SC19/NormalModes/demos/logs ."
            print(cmd)
            os.system(cmd)
        elif command == '':
            pass
        else:
            print('Invalid command')


