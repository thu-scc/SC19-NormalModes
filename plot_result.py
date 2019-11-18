import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter, NullFormatter
from numpy import format_float_scientific as format_float_scientific

def f_fmt_func(x, pos):
    return '%1.1fM' % (x*1e-6)

f_fmt = FuncFormatter(f_fmt_func)
x_fmt = FormatStrFormatter('%.0f')
fig_extension = "eps"

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
    elif theme == 'latex':
        first = ''
        in_line = '\t& '
        middle = '\n'
        enter = ' \\\\\n'
        last = ''
    else:
        print("ERROR! Theme {} not support!".format(theme))
        return ""
    # TODO latex theme

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

class WeakDataFormat:
    def __init__(self):
        self.Av = []
        self.Mv = []
        self.nodes = []
        self.label = []

    def add(self, model):
        self.Av.append(model['json-log']['Av_time'])
        self.Mv.append(model['json-log']['Mv_time'])
        self.nodes.append(model['nodes'])
        self.label.append(model['label'])

    def calc_eff(self):
        self.Av_eff = [self.Av[0] / t for t in self.Av]
        self.Mv_eff = [self.Mv[0] / t for t in self.Mv]

def plot_weak(done, show=False):
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
    f.write(toTable(tb_detail, 'latex'))
    f.close()

    plt.figure(figsize = [12, 5])
    # plot time
    ax = plt.subplot(1, 2, 1)
    groups = [WeakDataFormat(), WeakDataFormat()]
    for model in done:
        groups[model['group']].add(model)
    ymax = 0
    for i in range(2):
        if i == 0:
            suffix = "(M1-3)"
        else:
            suffix = "(M4-6)"
        plt.plot(groups[i].nodes, groups[i].Av, '-', label="Av " + suffix, linewidth=0.7, marker='x', markersize=8)
        plt.plot(groups[i].nodes, groups[i].Mv, '-', label="Mv " + suffix, linewidth=0.7, marker='.', markerfacecolor='none', markersize=8)
        ymax = max(ymax, max(groups[i].Av), max(groups[i].Mv))
    plt.xscale('log')
    plt.xlabel("number of nodes")
    plt.ylabel("time (s)")
    plt.ylim(ymin=0, ymax=ymax*1.2)
    plt.grid(True, which='both')
    ax.xaxis.set_minor_formatter(x_fmt)
    ax.xaxis.set_major_formatter(x_fmt)
    plt.legend(loc='upper left')

    # plot efficiency, assume done[0] is test M1
    ax = plt.subplot(1, 2, 2)
    for i in range(2):
        groups[i].calc_eff()
        plt.plot(groups[i].nodes, groups[i].Av_eff, '-', label="Av (M1-3)", linewidth=0.7, marker='x', markersize=8)
        plt.plot(groups[i].nodes, groups[i].Mv_eff, '-', label="Mv (M4-6)", linewidth=0.7, marker='.', markerfacecolor='none', markersize=8)
    plt.xscale('log')
    plt.xlabel("number of nodes")
    plt.ylabel("efficiency")
    ax.xaxis.set_minor_formatter(x_fmt)
    ax.xaxis.set_major_formatter(x_fmt)
    plt.grid(True, which='both')
    plt.legend(loc='upper left')
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.savefig("plot/weak.{}".format(fig_extension))
    if show:
        plt.show()
    plt.close()

def plot_fix(done, show=False):
    # table
    tb_detail = [['model', '(ln, lx)', '(xi,eta)',  '(deg, #it)', '#eigs', 'total']]
    for model in done:
        log = model['json-log']
        tb_detail.append([log['model'],
                         "({},{:.3g})".format(format_float_scientific(log['lambda_min'], exp_digits=1, precision=1), log['lambda_max']),
                         "({},{})".format(format_float_scientific(log['xi'], exp_digits=1, precision=1), format_float_scientific(log['eta'], exp_digits=1, precision=1)),
                         "({},{})".format(log['deg'], log['it']),
                         log['num_eigs'],
                         "{:.2f}".format(log['tot_time'])])

    f = open('plot/fix.table', "w")
    f.write(toTable(tb_detail, 'latex'))
    f.close()

    # plot
    tb_plot = [['model', 'size', 'deg', 'it', 'time']]
    size = []
    deg = []
    it = []
    tm = []
    tm1 = [[], []]
    size1 = [[], []]
    unify = [[], []]
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
        tm1[model['group']].append(log['tot_time'])
        size1[model['group']].append(log['Ag_size'])
        unify[model['group']].append(log['tot_time'] / log['deg'] / log['it'])

    cdeg = [271, 365, 364, 649, 869, 1062, 1330, 1566]
    cit =  [652, 672, 672, 672, 672, 672, 672, 672]
    ctotal = [2143.87, 3318.60, 3247.78, 6224.22, 7731.83, 9287.05, 11104.54, 13914.11]
    csize = [1038084, 2060190, 3894783, 7954392, 15809076, 31138518, 61381362, 120336519]
    cunify = [ctotal[i]/cdeg[i]/cit[i] for i in range(8)]

    edeg = [585, 933, 1430, 1957, 2863, 3711, 4922]
    eit = [612, 632, 652, 652, 652, 652, 652]
    etotal = [5369.784, 10083.951, 16570.223, 24614.738, 37793.401, 44962.119, 63054.411]
    esize = [1086702, 2265129, 4466349, 9037671, 17579616, 34115040, 66028227]
    eunify = [etotal[i]/edeg[i]/eit[i] for i in range(7)]
    

    fig, ax = plt.subplots()
    plt.semilogx(size, deg, c='xkcd:gold', linewidth=1.5, marker='D', markersize=8)
    plt.xticks(size, size, fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('degrees', fontsize = 20)
    plt.grid(True, which='both', c='xkcd:light grey')
    plt.ylim(ymin = 0, ymax = max(deg) * 1.2)
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-deg.{}".format(fig_extension))

    fig, ax = plt.subplots()
    plt.semilogx(size, it, c='xkcd:hot pink', linewidth=1.5, marker='*', markersize=10)
    plt.xticks(size, size, fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('iterations', fontsize = 20)
    plt.grid(True, which='both', c='xkcd:light grey')
    plt.ylim(ymin = 0, ymax = max(it) * 1.2)
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-it.{}".format(fig_extension))

    fig, ax = plt.subplots()
    for i in range(2):
        plt.semilogx(size1[i], tm1[i], c='xkcd:dodger blue', linewidth=1.5, marker='^', markersize=8)
    plt.semilogx([max(size1[0]), min(size1[1])], [max(tm1[0]), min(tm1[1])], c='xkcd:dodger blue', linestyle = (0, (5, 10)), linewidth=1.5)
    # have bug if time is not increasing, but it can be easily find from the output figure
    plt.xticks(size, size, fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('total time (s)', fontsize = 20)
    plt.grid(True, which='both', c='xkcd:light grey')
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-tm.{}".format(fig_extension))

    fig, ax = plt.subplots()
    plt.semilogx(csize, cunify, '-', c = 'xkcd:bright orange', linewidth=1.5, marker='X', markersize=8, label = "solid")
    plt.semilogx(esize, eunify, '-', c = 'xkcd:kelly green', linewidth=1.5, marker='o', markersize=8, markerfacecolor='none', label = "Earth")
    # not robust, but error can be found from the output figure easily
    plt.xticks([1e6, 4e6, 16e6, 64e6], [1e6, 4e6, 16e6, 64e6], fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('unified time', fontsize = 20)
    plt.legend(loc='lower right', fontsize = 20)
    plt.ylim(ymin = 0, ymax = max(cunify) * 1.5)
    plt.grid(True, which='both', c='xkcd:light grey')
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-unify-paper.{}".format(fig_extension))


    fig, ax = plt.subplots()
    for i in range(2):
        plt.semilogx(size1[i], unify[i], 'b-', linewidth=1.5, marker='p', markersize=8, label="Moon" if i == 0 else "")
    plt.semilogx([size1[0][2], size1[1][0]], [unify[0][2], unify[1][0]], 'b-', linestyle = (0, (5, 10)), linewidth=1.5)
    # not robust, but error can be found from the output figure easily
    plt.xticks(size, size, fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('unified time', fontsize = 20)
    plt.legend(loc='lower right', fontsize = 20)
    plt.grid(True, which='both', c='xkcd:light grey')
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-unify.{}".format(fig_extension))

    if show:
        plt.show()
    plt.close()
    
def plot_strong(done, show=False):
    C3_nn = [4, 8, 16, 32]
    C3_np = [192, 384, 768, 1536]
    C3_tm = [6854.54, 3247.78, 1779.14, 1259.08]
    C3_eff = [1.0, 1.1, 0.96, 0.68]
    E3_nn = [4, 8, 16]
    E3_np = [192, 384, 768]
    E3_tm = [34319.28, 16570.22, 10071.56]
    E3_eff = [1.0, 1.0, 0.85]
    M3_nn = []
    M3_np = []
    M3_tm = []
    M3_eff = []
    # assume done[0] is the first exp
    tb_detail  = [['nn/np', 'T-Av (s)', 'T-Mv (s)', 'T-M^{-1}v (s)', 'total (s)', 'eff.']]
    div = None
    for model in done:
        log = model["json-log"]
        if div is None:
            div = log['tot_time'] * log['nn'] # NOTE np should be the total thread?
        eff = div / (log['tot_time'] * log['nn'])
        tb_detail.append([
            "{}/{}".format(log['nn'], log['nn']),
            log['Av_time'],
            log['Mv_time'],
            log['rev_M_v_time'],
            log['tot_time'],
            eff
        ])
        M3_nn.append(log['nn'])
        M3_np.append(log['np'])
        M3_tm.append(log['tot_time'])
        M3_eff.append(eff)

    f = open("plot/strong.table", "w")
    f.write(toTable(tb_detail, 'latex'))
    f.close()

    fig, ax = plt.subplots()
    plt.semilogx(C3_nn, C3_tm, "-", label="C3 (Paper)", linewidth=1.5, marker='X', markersize=8, c='xkcd:bright orange')
    plt.semilogx(E3_nn, E3_tm, "-", label="E3 (Paper)", linewidth=1.5, marker='o', markerfacecolor='none', markersize=8, c='xkcd:kelly green')
    plt.xticks(C3_nn, C3_nn, fontsize = 22)
    plt.yticks(fontsize = 22)
    plt.xlabel("number of nodes", fontsize = 25)
    plt.ylabel("time (s)", fontsize = 25)
    plt.ylim(ymin = 0)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    plt.grid(True, which='major', c='xkcd:light grey')
    plt.legend(loc='upper right', fontsize = 25)
    plt.tight_layout()
    plt.savefig("plot/strong-paper-time.{}".format(fig_extension))

    fig, ax = plt.subplots()
    plt.semilogx(C3_nn, C3_eff, "-", label="C3 (Paper)", linewidth=1.5, marker='X', markersize=8, c='xkcd:bright orange')
    plt.semilogx(E3_nn, E3_eff, "-", label="E3 (Paper)", linewidth=1.5, marker='o', markerfacecolor='none', markersize=8, c='xkcd:kelly green')
    plt.xticks(C3_nn, C3_nn, fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlabel("number of nodes", fontsize = 20)
    plt.ylabel("efficiency", fontsize = 20)
    plt.ylim(ymin = 0.6, ymax = 1.2)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    plt.grid(True, which='major', c='xkcd:light grey')
    plt.legend(loc='upper right', fontsize = 20)
    plt.tight_layout()
    plt.savefig("plot/strong-paper-eff.{}".format(fig_extension))

    fig, ax = plt.subplots()
    plt.semilogx(M3_nn, M3_tm, "b-", label = "M3 (Ours)", linewidth=1.5, marker='p', markersize=8)
    plt.xticks(M3_nn, M3_nn, fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlabel("number of nodes", fontsize = 20)
    plt.ylabel("time (s)", fontsize = 20)
    plt.ylim(ymin = 0)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    plt.grid(True, which='major', c='xkcd:light grey')
    plt.legend(loc='upper right', fontsize = 20)
    plt.tight_layout()
    plt.savefig("plot/strong-ours-time.{}".format(fig_extension))

    fig, ax = plt.subplots()
    plt.plot(M3_nn, M3_eff, "b-", label = "M3 (Ours)", linewidth=1.5, marker='p', markersize=8)
    plt.xticks(M3_nn, M3_nn, fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlabel("number of nodes", fontsize = 20)
    plt.ylabel("efficiency", fontsize = 20)
    plt.ylim(ymin = 0.6, ymax = 1.2)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    plt.grid(True, which='major', c='xkcd:light grey')
    plt.legend(loc='upper right', fontsize = 20)
    plt.tight_layout()
    plt.savefig("plot/strong-ours-eff.{}".format(fig_extension))



