import matplotlib.pyplot as plt


def figure(size='full', num=None):
    params = {'legend.fontsize': 16,
              'legend.linewidth': 2}
    plt.rcParams.update(params)
    if size == 'full':
        plt.figure(num, figsize=(11, 2.75), dpi=200)
    elif size == 'half':
        plt.figure(num, figsize=(5, 3), dpi=200)
    else:
        raise Exception("Invalid size used as parameter for rplt.figure\
                         function")


def save(name, left=0.08, right=0.92, bottom=0.175):
    plt.subplots_adjust(left=left, right=right, bottom=bottom)
    plt.savefig(name)


def legend(loc=1, ncol=1):
    plt.legend(loc=loc, prop={'size': 13}, labelspacing=0.25, ncol=ncol)
