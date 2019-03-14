"""
Implementation of various measures of collocation strength
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""

import math


def mutual_info(f_s1, f_s2, f_s1s2, total, *misc):
    p_1 = float(f_s1) / float(total)
    p_2 = float(f_s2) / float(total)
    p_1_2 = float(f_s1s2) / float(total)

    return math.log(p_1_2 / (p_1 * p_2), 2)


def t_score(f_s1, f_s2, f_s1s2, total, *misc):
    x_bar = float(f_s1s2) / float(total)
    p_1 = float(f_s1) / float(total)
    p_2 = float(f_s2) / float(total)
    mu = p_1*p_2
    s_sq = x_bar*(1-x_bar)

    return (x_bar - mu)/math.sqrt(s_sq/total)
    #return 1 - f_s1*f_s2/f_s1s2


def dice_coeff(f_s1, f_s2, f_s1s2, *misc):
    return 2*f_s1s2/(f_s1 + f_s2)


def chi_squared(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    f_u = f_s1
    f_0u = total - f_u
    f_v = f_s2
    f_0v = total - f_v
    f_u_v = f_s1s2
    f_0u_v = len([k for k in pairs if s1 not in k and s2 in k])
    f_u_0v = len([k for k in pairs if s1 in k and s2 not in k])
    f_0u_0v = len([k for k in pairs if s1 not in k and s2 not in k])

    return (f_u_v - f_u*f_v)**2/f_u*f_v + (f_u_0v - f_u*f_0v)**2/f_u*f_0v \
            + (f_0u_v-f_0u*f_v)**2/f_0u*f_v + (f_0u_0v-f_0u*f_0v)**2/f_0u*f_0v


def rel_risk(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    a = f_s1s2/total
    b = len([k for k in pairs if s1 in k and s2 not in k])/total
    c = len([k for k in pairs if s1 not in k and s2 in k])/total
    d = len([k for k in pairs if s1 not in k and s2 not in k])/total
    return (a/(a+b))/(c/(c+d))
