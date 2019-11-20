import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter, NullFormatter
from numpy import format_float_scientific as format_float_scientific

plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)

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
    tb_detail = [['model', 'nn/np', 'ele', 'Ag', 't_Av', 't_Mv']]
    for model in done:
        log = model['json-log']
        tb_detail.append([log['model'],
                         "{}/{}".format(log['nn'], log['np']),
                         log['elements'],
                         log['Ag_size'],
                         log['Av_time'],
                         log['Mv_time']])
    f = open('plot/weak.table', "w")
    f.write(toTable(tb_detail, 'latex'))
    f.close()

    # plot time
    ax = plt.subplot()
    groups = [WeakDataFormat(), WeakDataFormat()]
    for model in done:
        groups[model['group']].add(model)
    ymax = 0
    for i in range(2):
        if i == 0:
            suffix = "(M1-3)"
        else:
            suffix = "(M4-6)"
        plt.plot(groups[i].nodes, groups[i].Av, '-', label="Av " + suffix, linewidth=1.5, marker='x', markersize=15)
        plt.plot(groups[i].nodes, groups[i].Mv, '-', label="Mv " + suffix, linewidth=1.5, marker='.', markerfacecolor='none', markersize=15)
        ymax = max(ymax, max(groups[i].Av), max(groups[i].Mv))
    plt.xscale('log')
    plt.xlabel("number of nodes", fontsize=20)
    plt.ylabel("time (s)", fontsize=20)
    plt.ylim(ymin=0, ymax=ymax*1.2)
    plt.grid(True, which='both')
    ax.xaxis.set_minor_formatter(x_fmt)
    ax.xaxis.set_major_formatter(x_fmt)
    plt.legend(loc='upper left', fontsize=15)
    plt.tight_layout()
    plt.savefig("plot/weak-time.{}".format(fig_extension))
    if show:
        plt.show()
    plt.close()

    # plot efficiency, assume done[0] is test M1
    ax = plt.subplot()
    for i in range(2):
        if i == 0:
            suffix = "(M1-3)"
        else:
            suffix = "(M4-6)"
        groups[i].calc_eff()
        plt.plot(groups[i].nodes, groups[i].Av_eff, '-', label="Av " + suffix, linewidth=1.5, marker='x', markersize=15)
        plt.plot(groups[i].nodes, groups[i].Mv_eff, '-', label="Mv " + suffix, linewidth=1.5, marker='.', markerfacecolor='none', markersize=15)
    plt.xscale('log')
    plt.xlabel("number of nodes", fontsize=20)
    plt.ylabel("efficiency", fontsize=20)
    ax.xaxis.set_minor_formatter(x_fmt)
    ax.xaxis.set_major_formatter(x_fmt)
    plt.grid(True, which='both')
    plt.legend(loc='lower left', fontsize=20)
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.savefig("plot/weak-eff.{}".format(fig_extension))
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
    plt.semilogx(size, deg, c='xkcd:gold', linewidth=1.5, marker='x', markersize=15)
    plt.xticks(size, size, fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('degree', fontsize = 20)
    plt.grid(True, which='both', c='xkcd:light grey')
    plt.ylim(ymin = 0, ymax = max(deg) * 1.2)
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-deg.{}".format(fig_extension))

    fig, ax = plt.subplots()
    plt.semilogx(size, it, c='xkcd:hot pink', linewidth=1.5, marker='o', markerfacecolor='none', markersize=15)
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
        plt.semilogx(size1[i], tm1[i], c='xkcd:dodger blue', linewidth=1.5, marker='o', markerfacecolor='none',  markersize=13)
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
    plt.semilogx(csize, cunify, '-', c = 'xkcd:bright orange', linewidth=1.5, marker='x', markersize=15, label = "Solid")
    plt.semilogx(esize, eunify, '-', c = 'xkcd:kelly green', linewidth=1.5, marker='o', markersize=15, markerfacecolor='none', label = "Earth")
    # not robust, but error can be found from the output figure easily
    plt.xticks([1e6, 4e6, 16e6, 64e6], [1e6, 4e6, 16e6, 64e6], fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('unified time (s)', fontsize = 20)
    plt.legend(loc='lower right', fontsize = 20)
    plt.ylim(ymin = 0, ymax = max(cunify) * 1.5)
    plt.grid(True, which='both', c='xkcd:light grey')
    ax.xaxis.set_major_formatter(f_fmt)
    ax.xaxis.set_minor_formatter(NullFormatter())
    plt.tight_layout()
    plt.savefig("plot/fix-unify-paper.{}".format(fig_extension))


    fig, ax = plt.subplots()
    for i in range(2):
        plt.semilogx(size1[i], unify[i], c = "xkcd:bluish purple", linewidth=1.5, marker='o', markersize=15, markerfacecolor='none', label="Mars" if i == 0 else "")
    plt.semilogx([size1[0][2], size1[1][0]], [unify[0][2], unify[1][0]], c = "xkcd:bluish purple", linestyle = (0, (5, 10)), linewidth=1.5)
    # not robust, but error can be found from the output figure easily
    plt.xticks(size, size, fontsize = 18)
    plt.xlabel('problem size', fontsize = 20)
    plt.yticks(fontsize = 18)
    plt.ylabel('unified time (s)', fontsize = 20)
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
    C3_av = [0.003398, 0.001741, 0.000687, 0.000357]
    C3_aeff = [x / C3_av[0] for x in C3_av]
    C3_tm = [6854.54, 3247.78, 1779.14, 1259.08]
    C3_eff = [1.0, 1.1, 0.96, 0.68]
    E3_nn = [4, 8, 16]
    E3_np = [192, 384, 768]
    E3_av = [0.007920, 0.004901, 0.003778]
    E3_aeff = [x / E3_av[0] for x in E3_av]
    E3_tm = [34319.28, 16570.22, 10071.56]
    E3_eff = [1.0, 1.0, 0.85]
    M_nn = [[], []]
    M_np = [[], []]
    M_av = [[], []]
    M_aeff = [[], []]
    M_tm = [[], []]
    M_eff = [[], []]
    # assume done[0] is the first exp
    tb_detail  = [['nn/np', 'T-Av (s)', 'Av-eff', 'T-Mv (s)', 'T-M^{-1}v (s)', 'total (s)', 'eff.']]
    div = [None, None]
    diva = [None, None]
    for model in done:
        log = model["json-log"]
        if div[model['group']] is None:
            div[model['group']] = log['tot_time'] * log['nn'] # NOTE np should be the total thread?
            diva[model['group']] = log['Av_time'] * log['nn'] 
        eff = div[model['group']] / (log['tot_time'] * log['nn'])
        effa = diva[model['group']] / (log['Av_time'] * log['nn'])
        tb_detail.append([
            "{}/{}".format(log['nn'], log['nn']),
            log['Av_time'],
            effa,
            log['Mv_time'],
            log['rev_M_v_time'],
            log['tot_time'],
            eff
        ])
        M_nn[model['group']].append(log['nn'])
        M_np[model['group']].append(log['np'])
        M_av[model['group']].append(log['Av_time'])
        M_aeff[model['group']].append(effa)
        M_tm[model['group']].append(log['tot_time'])
        M_eff[model['group']].append(eff)

    f = open("plot/strong.table", "w")
    f.write(toTable(tb_detail, 'latex'))
    f.close()

    fig, ax = plt.subplots()
    ax.semilogx(C3_nn, C3_tm, "-", label="C3 (time)", linewidth=1.5, marker='x', markersize=15, c='xkcd:red')
    ax.semilogx(E3_nn, E3_tm, "-", label="E3 (time)", linewidth=1.5, marker='o', markerfacecolor='none', markersize=15, c='xkcd:red')
    ax.set_ylabel("time (s)", fontsize = 20)
    ax.set_ylim(ymin = 0)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    ax.legend(loc='upper left', fontsize = 15)
    bx = ax.twinx()
    bx.semilogx(C3_nn, C3_eff, "-", label="C3 (eff)", linewidth=1.5, marker='x', markersize=15, c='xkcd:light green')
    bx.semilogx(E3_nn, E3_eff, "-", label="E3 (eff)", linewidth=1.5, marker='o', markerfacecolor='none', markersize=15, c='xkcd:light green')
    bx.set_ylabel("efficiency", fontsize = 20)
    bx.set_ylim(ymin = 0, ymax = 1.5)
    bx.xaxis.set_minor_formatter(NullFormatter())
    bx.xaxis.set_major_formatter(x_fmt)
    bx.legend(loc='upper right', fontsize = 15)
    plt.xlabel("number of nodes", fontsize = 20)
    plt.xticks(C3_nn, C3_nn, fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.tight_layout()
    plt.savefig("plot/strong-total-paper.{}".format(fig_extension))


    fig, ax = plt.subplots()
    ax.semilogx(C3_nn, C3_av, "-", label="C3 (time)", linewidth=1.5, marker='x', markersize=15, c='xkcd:red')
    ax.semilogx(E3_nn, E3_av, "-", label="E3 (time)", linewidth=1.5, marker='o', markerfacecolor='none', markersize=15, c='xkcd:red')
    plt.xlabel("number of nodes", fontsize = 20)
    ax.set_ylabel("time (s)", fontsize = 20)
    ax.set_ylim(ymin = 0)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    ax.legend(loc='upper left', fontsize = 15)
    bx = ax.twinx()
    bx.semilogx(C3_nn, C3_aeff, "-", label="C3 (eff)", linewidth=1.5, marker='x', markersize=15, c='xkcd:light green')
    bx.semilogx(E3_nn, E3_aeff, "-", label="E3 (eff)", linewidth=1.5, marker='o', markerfacecolor='none', markersize=15, c='xkcd:light green')
    bx.set_ylabel("efficiency", fontsize = 20)
    bx.set_ylim(ymin = 0, ymax = 1.5)
    bx.xaxis.set_minor_formatter(NullFormatter())
    bx.xaxis.set_major_formatter(x_fmt)
    bx.legend(loc='upper right', fontsize = 15)
    plt.xticks(C3_nn, C3_nn, fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.tight_layout()
    plt.savefig("plot/strong-av-paper.{}".format(fig_extension))

    fig, ax = plt.subplots()
    ax.semilogx(M_nn[0], M_tm[0], "-", label="M2 (time)", linewidth=1.5, marker='^', markersize=15, markerfacecolor='none', c='xkcd:violet')
    ax.semilogx(M_nn[1], M_tm[1], "-", label="M3 (time)", linewidth=1.5, marker='v', markerfacecolor='none', markersize=15, c='xkcd:violet')
    ax.set_ylabel("time (s)", fontsize = 20)
    ax.set_ylim(ymin = 0)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    ax.legend(loc='upper left', fontsize = 15)
    bx = ax.twinx()
    bx.semilogx(M_nn[0], M_eff[0], "-", label="M2 (eff)", linewidth=1.5, marker='^', markersize=15, markerfacecolor='none', c='xkcd:pale rose')
    bx.semilogx(M_nn[1], M_eff[1], "-", label="M3 (eff)", linewidth=1.5, marker='v', markerfacecolor='none', markersize=15, c='xkcd:pale rose')
    bx.set_ylabel("efficiency", fontsize = 20)
    bx.set_ylim(ymin = 0, ymax = 1.5)
    bx.xaxis.set_minor_formatter(NullFormatter())
    bx.xaxis.set_major_formatter(x_fmt)
    bx.legend(loc='upper right', fontsize = 15)
    plt.xlabel("number of nodes", fontsize = 20)
    plt.xticks(M_nn[0], M_nn[0], fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.tight_layout()
    plt.savefig("plot/strong-total-ours.{}".format(fig_extension))


    fig, ax = plt.subplots()
    ax.semilogx(M_nn[0], M_av[0], "-", label="M2 (time)", linewidth=1.5, marker='^', markersize=15, markerfacecolor='none', c='xkcd:violet')
    ax.semilogx(M_nn[1], M_av[1], "-", label="M3 (time)", linewidth=1.5, marker='v', markerfacecolor='none', markersize=15, c='xkcd:violet')
    ax.set_ylabel("time (s)", fontsize = 20)
    ax.set_ylim(ymin = 0)
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(x_fmt)
    ax.legend(loc='upper left', fontsize = 15)
    bx = ax.twinx()
    bx.semilogx(M_nn[0], M_aeff[0], "-", label="M2 (eff)", linewidth=1.5, marker='^', markersize=15, markerfacecolor='none', c='xkcd:pale rose')
    bx.semilogx(M_nn[1], M_aeff[1], "-", label="M3 (eff)", linewidth=1.5, marker='v', markerfacecolor='none', markersize=15, c='xkcd:pale rose')
    bx.set_ylabel("efficiency", fontsize = 20)
    bx.set_ylim(ymin = 0, ymax = 1.5)
    bx.xaxis.set_minor_formatter(NullFormatter())
    bx.xaxis.set_major_formatter(x_fmt)
    bx.legend(loc='upper right', fontsize = 15)
    plt.xlabel("number of nodes", fontsize = 20)
    plt.xticks(M_nn[0], M_nn[0], fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.tight_layout()
    plt.savefig("plot/strong-av-ours.{}".format(fig_extension))
