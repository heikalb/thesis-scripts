"""
Implementation of various measures of association.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""

import math


def get_freq(s1, s2, pairs):
    """
    Get the frequencies in a contingency table for a collocate pair.
    :param s1: the first suffix
    :param s2: the second suffix
    :param pairs: the collocate pair
    :return: frequencies in a contingency table
    """
    a = max(sum(pairs[k] for k in pairs if s1 == k[0] and s2 == k[1]), 0.5)
    b = max(sum(pairs[k] for k in pairs if s1 == k[0] and s2 != k[1]), 0.5)
    c = max(sum(pairs[k] for k in pairs if s1 != k[0] and s2 == k[1]), 0.5)
    d = max(sum(pairs[k] for k in pairs if s1 != k[0] and s2 != k[1]), 0.5)

    return a, b, c, d


def get_freq_(f_s1, f_s2, f_s1s2, total):
    """
    Get the frequencies in a contingency table for a collocate pair (alternative
    method).
    :param s1: the first suffix
    :param s2: the second suffix
    :param pairs: the collocate pair
    :return: frequencies in a contingency table
    """
    a = f_s1s2
    b = max(f_s1 - f_s1s2, 0.5)
    c = max(f_s2 - f_s1s2, 0.5)
    d = max(total - a - b - c, 0.5)

    return a, b, c, d


def mutual_info(f_s1, f_s2, f_s1s2, total, *misc):
    """
    Get the mutual information of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :param total: total number of suffixes in the corpus
    :return: mutual information of the collocate pair
    """
    p_1 = float(f_s1) / float(total)
    p_2 = float(f_s2) / float(total)
    p_1_2 = float(f_s1s2) / float(total)

    return math.log(p_1_2 / (p_1 * p_2), 2)


def t_score(f_s1, f_s2, f_s1s2, total, *misc):
    """
    Get the t-score of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :param total: total number of suffixes in the corpus
    :return: t-score of the collocate pair
    """
    x_bar = float(f_s1s2) / float(total)
    p_1 = float(f_s1) / float(total)
    p_2 = float(f_s2) / float(total)
    mu = p_1*p_2
    s_sq = x_bar*(1-x_bar)

    return (x_bar - mu)/math.sqrt(s_sq/total)


def dice_coeff(f_s1, f_s2, f_s1s2, *misc):
    """
    Get the Dice coefficient of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :return: Dice coefficient of the collocate pair
    """
    return 2*f_s1s2/(f_s1 + f_s2)


def chi_sq(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    """
    Get the chi-squared of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :param total: total number of suffixes in the corpus
    :param s1: the first suffix
    :param s2: the second suffix
    :param pairs: the collocate pair
    :return: chi-squared of the collocate pair
    """
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


def risk_ratio(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    """
    Get the risk ratio of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :param total: total number of suffixes in the corpus
    :param s1: the first suffix
    :param s2: the second suffix
    :param pairs: the collocate pair
    :return: risk ratio of the collocate pair
    """
    a, b, c, d = get_freq(s1, s2, pairs)
    rr = (a / (a + b)) / (c / (c + d))
    ci = risk_ratio_ci(a, b, c, d, rr)

    return rr, ci, (b == 0.5 or c == 0.5 or d == 0.5)


def risk_ratio_reverse(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    """
    Get the risk ratio reverse of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :param total: total number of suffixes in the corpus
    :param s1: the first suffix
    :param s2: the second suffix
    :param pairs: the collocate pair
    :return: risk ratio reverse of the collocate pair
    """
    a, b, c, d = get_freq(s1, s2, pairs)
    rr = (a / (a + c)) / (b / (b + d))
    ci = risk_ratio_ci(a, b, c, d, rr)

    return rr, ci


def risk_ratio_ci(a, b, c, d, rr):
    """
    Get the risk ratio of a confidence interval value.
    :param a: the upper left cell of the contingency table
    :param b: the lower left cell of the contingency table
    :param c: the upper right cell of the contingency table
    :param d: the lower right cell of the contingency table
    :param rr: the risk ratio value
    :return: lower and upper bounds of the confidence intervals
    """
    stand_err = math.sqrt(1/a + 1/b + 1/c + 1/d)
    ci_r = math.log(rr) + 1.96*stand_err
    ci_l = math.log(rr) - 1.96*stand_err

    return math.exp(ci_l), math.exp(ci_r)


def odds_ratio(f_s1, f_s2, f_s1s2, total, s1, s2, pairs):
    """
    Get the odds-ratio of a collocate pair.
    :param f_s1: frequency of the first suffix
    :param f_s2: frequency of the second suffix
    :param f_s1s2: frequency of the two suffixes together
    :param total: total number of suffixes in the corpus
    :param s1: the first suffix
    :param s2: the second suffix
    :param pairs: the collocate pair
    :return: odds ratio of the collocate pair
    """
    a, b, c, d = get_freq(s1, s2, pairs)
    condp_s2_s1 = a/(a + b)
    condp_s2_nots1 = c/(c + d)

    return (condp_s2_s1/(1-condp_s2_s1))/(condp_s2_nots1/(1-condp_s2_nots1))
