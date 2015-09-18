import sublime
import sublime_plugin


def all_regions(view, reserve=False):
    whole_region = sublime.Region(0, view.size())
    regions = view.lines(whole_region)
    if reserve:
        regions.reverse()
    return regions


def strip(input_str):
    return input_str.strip(" \s\t")


def cal_len(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    return int((utf8_length - length) / 2 + length)
