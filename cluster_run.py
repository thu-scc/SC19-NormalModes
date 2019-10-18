import os
import time
import subprocess

import parse_output
import matplotlib.pyplot as plt

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

def parse(label, print_result = True):
    if dataset == None:
        print('No dataset selected')
        return
    model = get_model(label)
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

# the first line is title
def toTable(input, theme = "display"):
    for i in range(len(input)):
        if (len(input[i]) != len(input[0])):
            print("ERROR! Invalid format in row {}!".format(i))
            print(input[0])
            print(input[i])
            return ""

    in_line = ""
    enter = ""
    first = ""
    middle = ""
    last = ""
    if theme == "csv":
        in_line = ","
        first = ""
        middle = "\n"
        enter = "\n"
        last = ""
    elif theme == "complex":
        in_line = "&"
        enter = "^_^\n"
        first =  "=======================================\n"
        middle = "\n---------------------------------------\n"
        last =   "***************************************\n"
    elif theme == 'display':
        in_line = '\t'
        first = ""
        middle = "\n"
        enter = "\n"
        last = ""
    else:
        print("ERROR! Theme {} not support!".format(theme))
        return ""

    # and more format ...
    st = first
    is_title = True
    for item in input:
        is_first = True
        for x in item:
            if (not is_first):
                st += in_line
            is_first = False
            st += str(x)
        if (is_title):
            st += middle
            is_title = False
        else:
            st += enter
    st += last
    return st

def plot_weak():
    done = get_valid_result()
    
    # table
    tb_detail = [['model', 'nn', 'np', 'ele', 'Ag', 't_Av', 't_Mv']]
    for model in done:
        log = model['json-log']
        tb_detail.append([log['model'],
                         log['nn'],
                         log['np'],
                         log['elements'],
                         log['Ag_size'],
                         log['Av_time'],
                         log['Mv_time']])
    f = open('plot/weak.table', "w")
    f.write(toTable(tb_detail, 'display'))
    f.close()

    # plot time
    label = []
    Av = []
    Mv = []
    nodes = []
    for model in done:
        Av.append(model['json-log']['Av_time'])
        Mv.append(model['json-log']['Mv_time'])
        nodes.append(model['json-log']['nn'])
        label.append(model['label'])
    plt.semilogx(nodes, Av, 'o-', label="Av")
    plt.semilogx(nodes, Mv, '*-', label="Mv")
    plt.xlabel("number of nodes")
    plt.ylabel("time (s)")
    plt.legend()
    plt.savefig("plot/weak-time.eps")
    plt.close()

    # plot efficiency, assume done[0] is test M1
    Av_eff = [Av[0]/t for t in Av]
    Mv_eff = [Mv[0]/t for t in Mv]
    plt.semilogx(nodes, Av_eff, 'o-', label="Av")
    plt.semilogx(nodes, Mv_eff, '*-', label="Mv")
    plt.xlabel("number of nodes")
    plt.ylabel("efficiency")
    plt.legend()
    plt.savefig("plot/weak-efficiency.eps")
    plt.close()

    # save data used in plot
    f = open("plot/weak.plot", "w")
    tb_title = ["model", "Av", "Mv", "Av-eff", "Mv-eff"]
    tb = [tb_title]
    for i in range(len(done)):
        model = done[i]
        tb.append([label[i], Av[i], Mv[i], Av_eff[i], Mv_eff[i]])
    f.write(toTable(tb))
    f.close()

def plot_fix():
    done = get_valid_result()
    
    # table
    tb_detail = [['model', '(ln, lx)', '(xi,eta)',  '(deg, #it)', '#eigs', 'total']]
    for model in done:
        log = model['json-log']
        tb_detail.append([log['model'],
                         "({},{})".format(log['lambda_min'], log['lambda_max']),
                         "({},{})".format(log['xi'], log['eta']),
                         "({},{})".format(log['deg'], log['it']),
                         log['num_eigs'],
                         log['tot_time']])

    f = open('plot/fix.table', "w")
    f.write(toTable(tb_detail, 'display'))
    f.close()

    # plot
    tb_plot = [['model', 'size', 'deg', 'it', 'time']]
    size = []
    deg = []
    it = []
    tm = []
    for model in done:
        log = model['json-log']
        tb_plot.append([
            log['model'],
            log['Ag_size'],
            log['deg'],
            log['it'],
            log['tot_time']
        ])
        size.append(log['Ag_size'])
        deg.append(log['deg'])
        it.append(log['it'])
        tm.append(log['tot_time'])
    plt.subplot(2,2,1)
    plt.semilogx(size, deg, 'o-', label="deg")
    plt.xlabel("size")
    plt.legend()

    plt.subplot(2,2,2)
    plt.semilogx(size, it, 'o-', label="it")
    plt.xlabel("size")
    plt.legend()

    plt.subplot(2,2,3)
    plt.semilogx(size, tm, 'o-', label="tm")
    plt.xlabel("size")
    plt.legend()

    plt.savefig("plot/fix-plot.eps")
    plt.close()
    
    

def plot():
    if (not os.path.exists("plot")):
        os.mkdir("plot")
    if dataset == None:
        print('No dataset selected')
    else:        dataset['plot']()

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
        {'label': 'M1', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M1', 'outputdir': 'models/output/Moon/M1', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 1, 'ranks': 24, 'threads': 1},
        {'label': 'M2', 'JOB': 2, 'basename': 'Mtopo_6L_1M.1'  , 'inputdir': 'models/input/Moon/M2', 'outputdir': 'models/output/Moon/M2', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 2, 'ranks': 24, 'threads': 1},
        {'label': 'M3', 'JOB': 2, 'basename': 'Mtopo_6L_2M.1'  , 'inputdir': 'models/input/Moon/M3', 'outputdir': 'models/output/Moon/M3', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 3, 'ranks': 24, 'threads': 1},
        {'label': 'M4', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M4', 'outputdir': 'models/output/Moon/M4', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 4, 'ranks': 24, 'threads': 1},
        {'label': 'M5', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M5', 'outputdir': 'models/output/Moon/M5', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 5, 'ranks': 24, 'threads': 1},
        {'label': 'M6', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M6', 'outputdir': 'models/output/Moon/M6', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1, 'nodes': 6, 'ranks': 24, 'threads': 1}
    ],
    "plot": plot_fix
}

if __name__ == "__main__":
    print('SCC 19, Tsinghua University, Reproduciblity Command Line')
    print('Commands: switch <experiment>, run <label>, parse <label>, show, check, plot, download, exit')
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


