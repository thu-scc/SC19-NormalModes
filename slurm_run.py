import os
import time
import subprocess

run_user = 'zhaocg'
log_dir = 'logs'
env_cmd = 'source /home/zhaocg/intel_env.sh\ncd /home/zhaocg/SC19/NormalModes/demos\n'
bin_path = '../bin/plmvcg_stampede2.out'

def generate_bash(nodes, ranks_per_node, threads_per_rank, log_label):
    bash = ''
    bash += '#!/bin/bash\n'
    bash += '#SBATCH -o {}/{}_{}_{}_{}.log\n'.format(log_dir, log_label, nodes, ranks_per_node, threads_per_rank)
    bash += '#SBATCH --nodes={}\n'.format(nodes)
    bash += '#SBATCH --job-name={}_{}_{}_{}\n\n'.format(log_label, nodes, ranks_per_node, threads_per_rank)
    bash += 'export OMP_NUM_THREADS={}\n'.format(threads_per_rank)
    bash += 'export I_MPI_PROCESS_MANAGER=mpd\n\n'
    bash += env_cmd
    bash += 'mpirun -bootstrap slurm -n {} {}'.format(nodes * ranks_per_node, bin_path)
    return bash

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

# Test configurations
datasets = [
    {'label': 'M1', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M1', 'outputdir': 'models/output/Moon/M1', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1},
    {'label': 'M2', 'JOB': 2, 'basename': 'Mtopo_6L_1M.1'  , 'inputdir': 'models/input/Moon/M2', 'outputdir': 'models/output/Moon/M2', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1},
    {'label': 'M3', 'JOB': 2, 'basename': 'Mtopo_6L_2M.1'  , 'inputdir': 'models/input/Moon/M3', 'outputdir': 'models/output/Moon/M3', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1},
    {'label': 'M4', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M4', 'outputdir': 'models/output/Moon/M4', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1},
    {'label': 'M5', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M5', 'outputdir': 'models/output/Moon/M5', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1},
    {'label': 'M6', 'JOB': 2, 'basename': 'Mtopo_6L_test.1', 'inputdir': 'models/input/Moon/M6', 'outputdir': 'models/output/Moon/M6', 'lowfreq': 0.2, 'upfreq': 2.0, 'pOrder': 1}
]
nodes_list = [1, 2, 3, 4, 5, 6, 7, 8]
ranks = 24
threads = 1

print('[N] Notes: this script must be run in demos dir, e.g.: python3 tools/slurm_run.py in demos dir')
for model in datasets:
    print('[@] Preparing model: {}'.format(model['label']))
    print('[-]   Global conf:')
    global_conf = generate_global_conf(model)
    if not os.path.exists(model['inputdir']):
        print('[E]   Model does not exist, jump to next one')
        continue
    if not os.path.exists(model['outputdir']):
        os.makedirs(model['outputdir'])
        print('[I]   {} created'.format(model['outputdir']))
    with open('global_conf', 'w') as f:
        f.write(global_conf)
        print('[I] global_conf written')
    print('[-]   Beginning to run on {} nodes'.format(nodes_list))
    for nodes in nodes_list:
        print('[!]     Nodes: {}'.format(nodes))
        print('[!]     Ranks per node: {}'.format(ranks))
        print('[!]     Threads per rank: {}'.format(threads))
        with open('slurm_generated_run.sh', 'w') as f:
            f.write(generate_bash(nodes, ranks, threads, model['label']))
        os.system('sbatch slurm_generated_run.sh')
        print('[!]     Task submitted, sleep 5s')
        time.sleep(5)
    print('[!]   Waiting the tasks to be finished')
    while True:
        if subprocess.check_output(['squeue']).decode('utf-8').find(run_user) == -1:
            print('[!]   Task finished: {}'.format(model['label']))
            break
        time.sleep(30)


