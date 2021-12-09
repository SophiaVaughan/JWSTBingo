import sys, getopt
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from textwrap import fill

def main(argv):

    ### Dealing with inputs to the code ###

    opts, args = getopt.getopt(argv,"hds:n:", ["savepath", "filename"])

    ### Set some defaults ###

    dt = False
    save=False
    name = 'JWSTBingocard.png'

    ### update defaults based on user input ###

    for opt, arg in opts:
        if opt == '-h':
            print('JWST Bingo Card Maker!')
            print('Options include:')
            print('-d :draws options only from the darktimeline list, unplayable but funny.')
            print('-s --savepath: a path to which to save the card. \n (If not specifed, output will not be saved. It will be shown although it may not look the same)')
            print('-n --filename: a name to save the card as. \n (If not specifed, it will be saved as JWSTBingocard.png)')
            print('')
            print('Example:')
            print("python3 JWSTBingo.py -s . -n mycard.png")

            if all([True for opt, arg in opts if opt == '-h']): sys.exit(2)

        elif opt in ["-d", "--distance"]: dt=True
        elif opt in ["-s", "--savepath"]: save=True; savepath = str(arg)
        elif opt in ["-n", "--filename"]: name = str(arg)

    global radius ; radius = 10
    global normalopt ; normalopt = []
    global dtopt ; dtopt = []

    with open("normalopt.txt", "r") as f:
        for line in f:
            normalopt.append(str(line.strip()))

    with open("darktimelineopt.txt", "r") as f:
        for line in f:
            dtopt.append(str(line.strip()))

    opt = _gopt(dt=dt)

    fig, ax = plt.subplots(figsize=(20,20))
    plt.axis('off')
    ax.set_xlim(-45, 45)
    ax.set_ylim(-45, 45)

    ### Make Hexagon Background
    _mirror_grid(lambda x, y, mn : ax.add_patch(_mirror(x,y)))

    ### Add text
    _mirror_grid(lambda x, y, mn : ax.text(x, y, fill(opt[mn], 16), fontsize=20, ma='center', ha='center', va='center'), include_center=True)
    
    if save==False: plt.show()
    else: plt.savefig(savepath + '/' + name, dpi=fig.dpi)
    plt.close()

def _mirror(x, y):
    return RegularPolygon((x,y), 6, radius=radius, orientation=30/180*np.pi, facecolor='y', edgecolor='k')

def _mirror_grid(func, include_center=False):

    s = np.sin(30/180*np.pi); c = np.cos(30/180*np.pi)

    ### middle column
    for i in range(-2,3,1):
        if (include_center==True) or (include_center==False and i!=0): func(0,2*c*radius*i, i+2)
    ### 2 columns of 4
    for i in range(-1,3,1):
        func((s+1)*radius,2*c*radius*(i-1/2), i+6)
        func(-(s+1)*radius,2*c*radius*(i-1/2), i+10)
    ### outer columns (3)
    for i in range(-1,2,1):
        func(2*(s+1)*radius,2*c*radius*i, i+14)
        func(-2*(s+1)*radius,2*c*radius*i, i+17)

def _gopt(dt=False):

    ### shuffle options
    np.random.shuffle(dtopt)
    if dt==False: np.random.shuffle(normalopt)

    ### Select options
    if dt==True: opt = dtopt[:18]
    else: opt = normalopt[:14] + dtopt[:4]; np.random.shuffle(opt)
    
    ### Add free space
    opt.insert(2, 'FREE SPACE \n everything is fine')

    return opt

if __name__ == "__main__":
   main(sys.argv[1:])



