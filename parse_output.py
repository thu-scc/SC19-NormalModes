import re
import sys

# warning: all variables are string! convert to int/float before use
def parse_output(filename):
    f = open(filename)
    st = "".join(f.readlines())

    meshname = re.compile("mesh name: (.*)").search(st).group(1)
    print("meshname " + meshname)

    mpisize = re.compile("mpi_size.*?(\d+)").search(st).group(1)
    print("mpisize " + mpisize)
    mpisize = int(mpisize)
    
    lower_freq = re.compile("lower frequency in mHz.*?([\d.]+)").search(st).group(1)
    print("lower_freq " + lower_freq)
    lower_freq = float(lower_freq)

    upper_freq = re.compile("upper frequency in mHz.*?([\d.]+)").search(st).group(1)
    print("upper_freq " + upper_freq)
    upper_freq = float(upper_freq)

    elements = re.compile("of elements:.*?(\d+)").search(st).group(1)
    print("elements " + elements)
    elements = int(elements)

    vertices = re.compile("of vertices:.*?(\d+)").search(st).group(1)
    print("vertices " + vertices)
    vertices = int(vertices)

    threads = re.compile("check number of threads.*?(\d+)").search(st).group(1)
    print("threads " + threads)
    threads = int(threads)

    deg = re.compile("polynomial deg.*?(\d+)").search(st).group(1)
    print("deg " + deg)
    deg = int(deg)

    lb = re.compile("lmin ([-+E.\d]+).*?lmax.*?([-+E.\d]+)", re.S).search(st)
    lambda_min = lb.group(1)
    lambda_max = lb.group(2)
    print("lambda_min ", lambda_min)
    print("lambda_max ", lambda_max)
    lambda_min = float(lambda_min)
    lambda_max = float(lambda_max)

    tot_time = re.compile("Iteration time.*?([\d.]+)").search(st).group(1)
    print("tot_time " + tot_time)
    tot_time = float(tot_time)

    Av = re.compile("Pol\(A\)\*v.*?([\d.]+).*?([\d]+).*?([\d.]+)").search(st)
    it = Av.group(2)
    Av_time = Av.group(3)
    print("it " + it)
    print("Av_time " + Av_time)
    it = int(it)
    Av_time = float(Av_time)

    rev_M_v_time= re.compile("Solve with B.*?([\d.]+).*?([\d]+).*?([\d.]+)").search(st).group(3)
    print("rev_M_v_time " + rev_M_v_time)
    rev_M_v_time = float(rev_M_v_time)

    Mv_time = re.compile("Matvec in ChebIter.*?([\d.]+).*?([\d]+).*?([\d.]+)").search(st).group(3)
    print("Mv_time " + Mv_time)
    Mv_time = float(Mv_time)

    num_eigs = re.compile("Row\D*?(\d+?)\D*?[\d.E+-]*?\D*?Transform", re.S).search(st).group(1)
    print("num_eigs " + num_eigs)
    num_eigs = int(num_eigs)
    return {
        "meshname": meshname,
        "mpisize": mpisize,
        "lower_freq": lower_freq,
        "upper_freq": upper_freq,
        "elements": elements,
        "vertices": vertices,
        "threads": threads,
        "deg": deg,
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
    ans = parse_output(filename)
    print(ans)