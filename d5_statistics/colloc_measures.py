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
    # return 1 - f_s1*f_s2/f_s1s2


def dice_coeff(f_s1, f_s2, f_s1s2, *misc):
    return 2*f_s1s2/(f_s1 + f_s2)


def chi_sq(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    f_u = f_s1
    f_0u = total - f_u
    f_v = f_s2
    f_0v = total - f_v
    f_u_v = f_s1s2
    f_0u_v = sum(pairs[k] for k in pairs if s1 != k[0] and s2 == k[1])
    f_u_0v = sum(pairs[k] for k in pairs if s1 == k[0] and s2 != k[1])
    f_0u_0v = sum(pairs[k] for k in pairs if s1 != k[0] and s2 != k[1])

    return (f_u_v - f_u*f_v)**2/f_u*f_v + (f_u_0v - f_u*f_0v)**2/f_u*f_0v \
            + (f_0u_v-f_0u*f_v)**2/f_0u*f_v + (f_0u_0v-f_0u*f_0v)**2/f_0u*f_0v


def rel_risk(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    a = f_s1s2
    b = max(sum(pairs[k] for k in pairs if s1 == k[0] and s2 != k[1]), 1)
    c = max(sum(pairs[k] for k in pairs if s1 != k[0] and s2 == k[1]), 1)
    d = max(sum(pairs[k] for k in pairs if s1 != k[0] and s2 != k[1]), 1)

    rr = (a/(a+b))/(c/(c+d))
    ci = rel_risk_ci(a, b, c, d, rr)

    return rr, ci


def odds_ratio(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    a = f_s1s2
    b = max(sum(pairs[k] for k in pairs if s1 == k[0] and s2 != k[1]), 1)
    c = max(sum(pairs[k] for k in pairs if s1 != k[0] and s2 == k[1]), 1)
    d = max(sum(pairs[k] for k in pairs if s1 != k[0] and s2 != k[1]), 1)
    condp_s2_s1 = a/(a + b)
    condp_s2_nots1 = c/(c + d)

    return (condp_s2_s1/(1-condp_s2_s1))/(condp_s2_nots1/(1-condp_s2_nots1))


def rel_risk_ci(a, b, c, d, rr):
    stand_err = math.sqrt(1/a + 1/b + 1/c + 1/d)
    ci_r = math.log(rr) + 1.96*stand_err
    ci_l = math.log(rr) - 1.96*stand_err

    return math.exp(ci_l), math.exp(ci_r)
