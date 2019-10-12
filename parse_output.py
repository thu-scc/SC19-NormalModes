import re
import sys

# warning: all variables are string! convert to int/float before use
def parse_output(filename):
    f = open(filename)
    st = "".join(f.readlines())

    print('Parsing results ... ', flush=True, end='')
    meshname = re.compile("mesh name: (.*)").search(st).group(1)
    mpi_ranks = int(re.compile("mpi_size.*?(\d+)").search(st).group(1))
    lower_freq = float(re.compile("lower frequency in mHz.*?([\d.]+)").search(st).group(1))
    upper_freq = float(re.compile("upper frequency in mHz.*?([\d.]+)").search(st).group(1))
    elements = int(re.compile("of elements:.*?(\d+)").search(st).group(1))
    vertices = int(re.compile("of vertices:.*?(\d+)").search(st).group(1))
    threads = int(re.compile("check number of threads.*?(\d+)").search(st).group(1))
    deg = int(re.compile("polynomial deg.*?(\d+)").search(st).group(1))

    lb = re.compile("lmin ([-+E.\d]+).*?lmax.*?([-+E.\d]+)", re.S).search(st)
    lambda_min = float(lb.group(1))
    lambda_max = float(lb.group(2))

    tot_time = float(re.compile("Iteration time.*?([\d.]+)").search(st).group(1))
    it = int(re.compile("Pol\(A\)\*v.*?([\d.]+).*?([\d]+).*?([\d.]+)").search(st).group(2))
    rev_M_v_time = float(re.compile("Solve with B.*?([\d.]+).*?([\d]+).*?([\d.]+)").search(st).group(3))

    M_A_Times = re.compile("Matvec in ChebIter.*?([\d.]+).*?([\d]+).*?([\d.]+)").findall(st)
    Mv_time = float(M_A_Times[0][2])
    Av_time = float(M_A_Times[1][2])

    num_eigs = int(re.compile("Row\D*?(\d+?)\D*?[\d.E+-]*?\D*?Transform", re.S).search(st).group(1))

    print('OK!', flush=True)
    print('[FIGURE 7] RESULTS:')
    print('-      Av: {:.6f}'.format(Av_time))
    print('-      Mv: {:.6f}'.format(Mv_time))
    print('- M^(-1)v: {:.6f}'.format(rev_M_v_time))
    print('-   total: {:.6f}'.format(tot_time))

if __name__ == '__main__':
    filename = sys.argv[1]
    print('Reading output file: ' + filename + ' ... OK!')
    parse_output(filename)