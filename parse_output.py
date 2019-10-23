import re
import sys

def parse_output(filename, print_result=True, model='', nodes=0, ranks=0):
    f = open(filename)
    st = ''.join(f.readlines())

    print('Parsing results of {} ... '.format(filename), flush=True, end='')
    meshname = re.compile('mesh name: (.*)').search(st).group(1)
    mpi_ranks = int(re.compile('mpi_size.*?(\d+)').search(st).group(1))
    lower_freq = float(re.compile('lower frequency in mHz.*?([\d.]+)').search(st).group(1))
    upper_freq = float(re.compile('upper frequency in mHz.*?([\d.]+)').search(st).group(1))
    elements = int(re.compile('of elements:.*?(\d+)').search(st).group(1))
    vertices = int(re.compile('of vertices:.*?(\d+)').search(st).group(1))
    threads = int(re.compile('check number of threads.*?(\d+)').search(st).group(1))

    xi_eta = re.compile('intv:\[([-+e.\d]+), ([-+e.\d]+),').search(st)
    xi = float(xi_eta.group(1))
    eta = float(xi_eta.group(2))

    deg = int(re.compile('polynomial deg.*?(\d+)').search(st).group(1))
    Ag_size = A_size = Ap_size = 0
    if st.find('total Ad size') != -1: Ag_size = int(re.compile('total Ad size.*?(\d+)').search(st).group(1))
    # if st.find('total A size')  != -1: A_size = int(re.compile('total A size.*?(\d+)').search(st).group(1))
    if st.find('total Ap size') != -1: Ap_size = int(re.compile('total Ap size.*?(\d+)').search(st).group(1))

    lb = re.compile('lmin ([-+E.\d]+).*?lmax.*?([-+E.\d]+)', re.S).search(st)
    lambda_min = float(lb.group(1))
    lambda_max = float(lb.group(2))

    tot_time = float(re.compile('Iteration time.*?([\d.]+)').search(st).group(1))
    it = int(re.compile('Pol\(A\)\*v.*?([\d.]+).*?([\d]+).*?([\d.]+)').search(st).group(2))
    rev_M_v_time = float(re.compile('Solve with B.*?([\d.]+).*?([\d]+).*?([\d.]+)').search(st).group(3))

    M_A_Times = re.compile('Matvec in ChebIter.*?([\d.]+).*?([\d]+).*?([\d.]+)').findall(st)
    Mv_time = float(M_A_Times[0][2])
    Av_time = float(M_A_Times[1][2])

    num_eigs = int(re.compile('Row\D*?(\d+?)\D*?[\d.E+-]*?\D*?Transform', re.S).search(st).group(1))
    np = nodes * ranks

    print('OK!', flush=True)
    if print_result:
        print('Model Info:')
        if nodes > 0:
            print('-   Model: {}'.format(model))
            print('-   nn/np: {}/{}'.format(nodes, np))
        print('-     elm: {}'.format(elements))
        if Ag_size: print('- Ag size: {}'.format(Ag_size))
        # if A_size : print('- A  size: {}'.format(A_size))
        if Ap_size: print('- Ap size: {}'.format(Ap_size))
        print('Weak Scaling:')
        print('-      Av: {:.6f}'.format(Av_time))
        print('-      Mv: {:.6f}'.format(Mv_time))
        print('Fixed Interval:')
        print('- (ln,lx): ({:.6f}, {:.6f})'.format(lambda_min, lambda_max))
        print('- (xi,eta): ({}, {})'.format(xi, eta))
        print('- (dg,it): ({}, {})'.format(deg, it))
        print('- eigs: {}'.format(num_eigs))
        print('-   total: {:.6f}'.format(tot_time))
        print('Strong Scalability:')
        print('-      Av: {:.6f}'.format(Av_time))
        print('-      Mv: {:.6f}'.format(Mv_time))
        print('-  rev_Mv: {:.6f}'.format(rev_M_v_time))
        print('-   total: {:.6f}'.format(tot_time))
    return {
        "model": model,
        "nn": nodes,
        "np": np,
        "meshname": meshname,
        "mpi_ranks": mpi_ranks,
        "lower_freq": lower_freq,
        "upper_freq": upper_freq,
        "xi": xi,
        "eta": eta,
        "elements": elements,
        "vertices": vertices,
        "threads": threads,
        "deg": deg,
        "Ag_size": Ag_size,
        "Ap_size": Ap_size,
        "lambda_min": lambda_min,
        "lambda_max": lambda_max,
        "tot_time": tot_time,
        "it": it,
        "Av_time": Av_time,
        "rev_M_v_time": rev_M_v_time,
        "Mv_time": Mv_time,
        "num_eigs": num_eigs
    }

if __name__ == '__main__':
    filename = sys.argv[1]
    print('Reading output file: ' + filename + ' ... OK!')
    parse_output(filename)