'''
Input file follows the following format. All lines are
mandatory. No comments can be made within the file.
Must be followed strictly.
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import os, sys, copy
import numpy as np

from pylab import rcParams
rcParams['legend.numpoints'] = 1
rcParams['font.family']='sans'
rcParams['axes.titlepad'] = 20 
mpl.style.use('ggplot')
# plt.rcParams['axes.facecolor']='binary'

colors = [ '#C95F63', '#516EA9', '#F1AD32', '#3B8320']
#'#292DF4'红色 '#292DF4'亮蓝
# #
line_styles = ['--', ':', '-.', '-']
marker_types = ['o', 's', '^', '*']

# This lists out all the variables that you can control
# A copy of this dictionary will be generated (deepcopy),
# in case the default values are lost
var_map_ORIGINAL = {
    'fontname' : "Times New Roman",     # Windows and Linux systems are missing some fonts
    #'fontname' : "Times New Roman",
    'line_length' : 40,
    'title' : 'Graph Title',
    'file_name' : 'Image',
    'plot_type' : 'line',       # line = line, scatter = scatter, both = line + intervaled marker
    'xlabel' : 'X Label',
    'xtype' : 'normal'   ,      # normal, log
    'xlabeldetail' : (),        # (axis start value, interval) minor axis will divide main by 3
    'x_range' : 'auto'   ,      # auto, 0 100
    'ylabel' : 'Y Label',
    'ytype' : 'normal',         # normal or log
    'ylabeldetail' : (),        # see xlabeldetail
    'y_range' : 'auto',
    'minor' : False,            # Turn on minor axis on both axis
    'markersize' : 10,
    'linewidth' : 6,
    'title_size' : 10,
    'loc' : 4,                  # location of legend, see online documentation
    'label_starter' : '###LABEL_STARTER###',
    'data_starter' : '###DATA_STARTER###',
    'every' : 1,                # Display marker every n points
    'markevery': 1,             # Display marker every x positions (depends on display)
    'labels': [],               # Legend lines
    'xdata': [],
    'ydata': [],
    'skip_data':[],             # Skip certain columns of data. [1, 1, 0, 1] skips 3rd column
    'subplot': '',
    'subplot_loc': [0, 0, 0, 0],
    'label_fontsize':20
    #x,y1,y2
}

# Save a copy of var_map for iterating through multiple files
var_map_NOTOUCH = copy.deepcopy(var_map_ORIGINAL)


def split_line (line):

    want = False
    splitted = False
    result = ''
    accumulated = 0
    for i in range(len(line)):
        accumulated += 1
        if accumulated % var_map['line_length'] == 0 and i > 0:
            want = True
        if want and line[i] == ' ':
            result += '\n'
            want = False
            splitted = True
            accumulated = 0
        else:
            result += line[i]

    return result, splitted

def process_variable(line):

    global var_map

    splits = line.split('=')
    varname = splits[0]
    line = '='.join(splits[1:]).strip()

    if isinstance(var_map[varname], str):
        var_map[varname] = line
        if varname == 'title':
            var_map[varname] = split_line(line)[0]
    else:
        var_map[varname] = eval(line)


def parse_file(f, var_map):
    lines = f.readlines()

    data_count = 0
    mode = 'variables'
    for i in range(len(lines)):

        # Comment line
        if lines[i].startswith('//'):
            continue

        if var_map['data_starter'] in lines[i]:
            mode = 'data'
            continue
        elif var_map['label_starter'] in lines[i]:
            mode = 'label'
            continue

        if mode == 'variables':
            process_variable(lines[i])
        elif mode == 'data':
            splits = lines[i].strip().split(' ')
            if data_count % var_map['every'] == 0:
                var_map['xdata'].append(eval(splits[0]))

                for i in range(1, len(splits)):
                    if len(var_map['ydata']) < i:
                        var_map['ydata'].append([eval(splits[i])])
                    else:
                        var_map['ydata'][i- 1].append(eval(splits[i]))
            data_count += 1

        elif mode == 'label':
            var_map['labels'].append(lines[i].strip())


    # This data columns that you do not wish to show in the graph
    if len(var_map['skip_data']) > 0:
        labels = []
        ydata = []
        for i in range(len(var_map['skip_data'])):
            v = var_map['skip_data'][i]
            if v or v == 1 or v == '1':
                labels.append(var_map['labels'][i])
                ydata.append(var_map['ydata'][i])

        var_map['labels'] = labels
        var_map['ydata'] = ydata

    return var_map


def generate_plot(ax, var_map, is_sub=False):
    '''
    We create a function for creating plot so that we can
    put sub-plots within a plot
    '''

    if not is_sub:
        ax.set_title(var_map['title'], fontsize=var_map['title_size'], fontweight='heavy')

        ax.set_xlabel(var_map['xlabel'], fontsize=var_map['label_fontsize'])
        ax.set_ylabel(var_map['ylabel'], fontsize=var_map['label_fontsize'])
    ax.tick_params(axis='both', which='major', labelsize=var_map['label_fontsize'])
    plt.xticks(fontname=var_map['fontname'])
    plt.yticks(fontname=var_map['fontname'])

    if var_map['xlabeldetail'] != ():
        max_val = var_map['xlabeldetail'][0] + 10 *var_map['xlabeldetail'][1]
        major_ticks = np.arange(var_map['xlabeldetail'][0], max_val, var_map['xlabeldetail'][1])
        ax.set_xticks(major_ticks)
        if var_map['minor']:
            minor_ticks = np.arange(var_map['xlabeldetail'][0], max_val, var_map['xlabeldetail'][1] / 3)
            ax.set_xticks(minor_ticks, minor=True)
    elif var_map['minor']:
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))

    # if is_sub:
    #     ax.xaxis.set_major_locator(MultipleLocator(500))
    #     ax.yaxis.set_major_locator(MultipleLocator(2))

    if var_map['ylabeldetail'] != ():
        max_val = var_map['ylabeldetail'][0] + 10 *var_map['ylabeldetail'][1]
        major_ticks = np.arange(var_map['ylabeldetail'][0], max_val, var_map['ylabeldetail'][1])
        ax.set_yticks(major_ticks)
        if var_map['minor']:
            minor_ticks = np.arange(var_map['ylabeldetail'][0], max_val, var_map['ylabeldetail'][1] / 3)
            ax.set_yticks(minor_ticks, minor=True)
    elif var_map['minor']:
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    for i in range(len(var_map['labels'])):
        print(i)
        # print(var_map['ydata'][i])
        if var_map['plot_type'] == 'line':
            ax.plot(var_map['xdata'], var_map['ydata'][i], \
                    line_styles[i % len(line_styles)], marker=marker_types[i % len(marker_types)], markersize=var_map['markersize'], \
                    color=colors[i % len(colors)], label=var_map['labels'][i], linewidth=var_map['linewidth'])
        elif var_map['plot_type'] == 'both':
            ax.plot(var_map['xdata'], var_map['ydata'][i], \
                    line_styles[i % len(line_styles)], marker=marker_types[i % len(marker_types)], markersize=var_map['markersize'], markevery=var_map['markevery'], \
                    color=colors[i % len(colors)], label=var_map['labels'][i], linewidth=var_map['linewidth'])
        else:
            ax.scatter(var_map['xdata'], var_map['ydata'][i], marker=marker_types[i % len(marker_types)], s=[var_map['markersize'] * 10 for n in range(len(var_map['xdata']))], \
                        color=colors[i % len(colors)], label=var_map['labels'][i],)

    if var_map['xtype'] == 'log':
        ax.set_xscale('log')
    if var_map['ytype'] == 'log':
        ax.set_yscale('log')


    if var_map['x_range'] != 'auto':
        ax.set_xlim([eval(var_map['x_range'].split()[0]), eval(var_map['x_range'].split()[1])])
    if var_map['y_range'] != 'auto':
        ax.set_ylim([eval(var_map['y_range'].split()[0]), eval(var_map['y_range'].split()[1])])
    #ax.axis([120, 300, 708, 710])

    #plt.legend()
    if var_map['plot_type'] == 'line' or var_map['plot_type'] == 'both':
        markerscale = 1.
    else:
        markerscale = 2.

    if not is_sub:
        L = plt.legend(loc=6, bbox_to_anchor=(0.52, 0.35), fontsize=18, markerscale=markerscale, frameon=True, shadow=True)
        plt.setp(L.texts)

    plt.grid(b=True, which='major', axis='both', alpha=0.6, linestyle='-.', linewidth=2)# 
    if var_map['minor']:
        print('minor')
        plt.grid(b=True, which='minor', axis='both', alpha=0.3,linewidth=1)#, linestyle='-.'
    plt.facecolor=(0.1843, 0.3098, 0.3098)

def add_subplot_axes(ax,rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    rect = [0.51,0.55,0.47,0.3]
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= 0.1
    y_labelsize *= 0.1
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax


if __name__ == '__main__':

    for i in range(1, len(sys.argv)):
#~
        filename = sys.argv[i] + '.data'
        var_map = copy.deepcopy(var_map_NOTOUCH)

        with open(filename, 'r', encoding='utf-8') as f:
            var_map = parse_file(f, var_map)

        ########### Plot the Figure ##############
        fig = plt.figure(facecolor='white', figsize=(8, 7))

        ax = fig.add_subplot(111)
        generate_plot(ax, var_map)

        while var_map['subplot'] != '0':
            subplot_loc = var_map['subplot_loc']
            with open('svhn_eps=0.1_del=1e-4_sub.data', 'r') as f:
                var_map = copy.deepcopy(var_map_NOTOUCH)
                var_map = parse_file(f, var_map)
            #ax = ax.add_axes(var_map['subplot_loc'])
            ax =  add_subplot_axes(ax, subplot_loc)
            generate_plot(ax, var_map, True)
#~

        plt.savefig(var_map['file_name'])
        plt.show()

