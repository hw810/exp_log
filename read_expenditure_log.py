#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
import re
from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.dates import WeekdayLocator, SATURDAY, DayLocator, DateFormatter


class DayLog():

    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.items_collection = defaultdict(int)

        def add_item(self, item_name, item_price):
            self.items_collection[item_name] += item_price

        def remove_item(self, item_name):
            if item_name in self.items_collection.keys:
                self.items_collection.pop(item_name)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def day_log_iterator(f):

    d_log = None
    for l in f:
        line = l.strip()
        if not line:
            continue
        if get_h_num(line) == 1:  # week start
            pass
        elif get_h_num(line) == 2:  # day start
            if d_log:
                yield d_log

            str_timestamp = parse_square_bracket(line)
            if str_timestamp:
                dt_timestamp = dt.strptime(str_timestamp, '%Y-%m-%d')
                d_log = DayLog(dt_timestamp)
        elif get_h_num(line) == 0 and d_log:  # normal text
            bl = line.split('|')[1:-1]
            if len(bl) < 3:
                continue
            elif not is_number(bl[2]):
                d_log.items_collection[bl[2]] += float(bl[0])

    if d_log:
        yield d_log


def get_h_num(one_string):
    """
    :param one_string:
    :return: heading number e.g. 1 for heading 1; 2 for heading 2
    """
    token = one_string.split(' ')[0]
    if re.match('^\*+$', token):
        return len(token)
    else:
        return 0


def parse_square_bracket(one_string):
    """
    @one_string: string input to detect the pattern on
    @return: the substring that satisfy the pattern, otherwise None
    """
    str_in_between = re.search('\[([0-9]{4}-[0-9]{2}-[0-9]{2}) \w+\]', one_string)
    if str_in_between:
        return str_in_between.group(1)
    else:
        return None


if __name__ == '__main__':
    fname = os.path.join(os.path.expanduser('~'), 'Dropbox/Org/SavingLog.org')
    f_log = open(fname)
    total_expenditure = defaultdict(int)
    for d in day_log_iterator(f_log):
        total_expenditure[d.timestamp] = sum([i for i in d.items_collection.values()])

    total_keys = total_expenditure.keys()
    total_keys.sort()
    total_values = []
    for k in total_keys:
        #     print k.strftime('%Y-%m-%d'), total_expenditure[k]
        total_values.append(total_expenditure[k])
    f_log.close()

    cum_values = [np.sum(total_values[:i+1]) for i in xrange(len(total_values))]
    daily_budget = 100.0 / 7
    x = np.array(range(1, len(total_keys)+1))
    cum_budget = x * daily_budget
    print 'Total spending: {0:.1f}'.format(cum_values[-1])
    print 'Total budget:   {0:.1f}'.format(cum_budget[-1])

    # plot

    fig = plt.figure()
    fig.suptitle('Save to thrive', fontsize=20)
    ax = fig.add_subplot(111)
    # ax.plot(total_keys, total_values, 'g-')
    ax.bar(total_keys, total_values, edgecolor='none', align='center', color='green')
    avg = [np.mean(total_values[:i+1]) for i in xrange(len(total_values))]
    ax.plot(total_keys, avg, 'g-o', markeredgecolor='none', markerfacecolor='white', linewidth=2)
    for tl in ax.get_yticklabels():
        tl.set_color('green')
    # fig.autofmt_xdate()
    ax.xaxis.set_major_locator(WeekdayLocator(SATURDAY))  # major ticks on Saturdays
    ax.xaxis.set_minor_locator(DayLocator())  # minor ticks on every days
    week_formatter = DateFormatter('%y %b %d')
    ax.xaxis.set_major_formatter(week_formatter)
    ax.grid(True)
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    ax2 = ax.twinx()
    ax2.plot(total_keys, cum_values, 'r-', linewidth=2)
    for tl in ax2.get_yticklabels():
        tl.set_color('red')
    ax2.plot(total_keys, cum_budget, 'r--', linewidth=2)
    ax2.xaxis.set_major_locator(WeekdayLocator(SATURDAY))  # major ticks on Saturdays
    ax2.xaxis.set_minor_locator(DayLocator())  # minor ticks on every days
    week_formatter = DateFormatter('%y %b %d')
    ax2.xaxis.set_major_formatter(week_formatter)
    ax2.grid(True)
    ax2.xaxis_date()
    ax2.autoscale_view()
    plt.setp(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.show()

