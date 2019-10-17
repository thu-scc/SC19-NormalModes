import os
import time
import subprocess

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

print('[N] Notes: this script must be run in demos dir, e.g.: python3 tools/cluster_run.py in demos dir')
