# Treat selected line(s) as Markdown table
# If no selection, treat the whole document as  Markdown table (will remove other contents)
import sublime
import sublime_plugin
from .common import *


def any_point_in_selection(region, selection):
    for i in range(region.begin(), region.end() - 1):
        if selection.contains(sublime.Region(i, i + 1)):
            return True
    return False


def regions_from_selection(view, selection):
    whole_region = sublime.Region(0, view.size())
    regions = view.lines(whole_region)
    selected_regions = []
    for region in regions:
        if any_point_in_selection(region, selection):
            selected_regions.append(region)
    return selected_regions


def regions_to_list(view, regions, sep="|"):
    big_list = []
    for region in regions:
        line = strip(view.substr(region)).strip(sep)
        columns = line.split(sep)
        if len(columns) <= 1:
            continue
        small_list = []
        for column in columns:
            small_list.append(column.strip().replace("\t", "    "))
        big_list.append(small_list)
    return big_list


def list_to_content(big_list):
    row_count = len(big_list)
    column_count = len(big_list[0])
    max_len_list = []
    for y in range(0, column_count):
        column_values = []
        for x in range(0, row_count):
            column_values.append(big_list[x][y])
        max_len_list.append(cal_len(max(column_values, key=cal_len)))

    for x in range(0, row_count):
        for y in range(0, column_count):
            length = cal_len(big_list[x][y])
            big_list[x][y] += " " * (max_len_list[y] - length)
    content = ""
    for x in range(0, row_count):
        content += "|"
        for y in range(0, column_count):
            content += big_list[x][y] + "|"
        if x < row_count - 1:
            content += "\n"
    return content


class TableReformatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        regions = regions_from_selection(view, view.sel())
        if len(regions) == 0:
            regions = all_regions(view)
        big_list = regions_to_list(view, regions)
        content = list_to_content(big_list)
        # whole_region = sublime.Region(0, view.size())
        whole_region = sublime.Region(regions[0].a, regions[len(regions) - 1].b)
        view.replace(edit, whole_region, content)


class ExcelToTableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        view.run_command('remove_blank_lines')
        regions = all_regions(view)
        big_list = regions_to_list(view, regions, "\t")
        content = list_to_content(big_list)
        whole_region = sublime.Region(0, view.size())
        view.replace(edit, whole_region, content)
