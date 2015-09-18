import sublime
import sublime_plugin
from .common import *


def do_trim(view, edit, reg):
    regions = view.find_all(reg)
    regions.reverse()
    for region in regions:
        s = view.substr(region)
        view.replace(edit, region, strip(s))


def remove_leading(view, edit):
    do_trim(view, edit, "^(\s|\t)+")


def remove_trailing(view, edit):
    do_trim(view, edit, "(\s|\t)+$")


class RemoveCommand(sublime_plugin.TextCommand):
    # 0 both, 1 left, 2 right
    def run(self, edit, trim_type=0):
        view = self.view
        if trim_type == 1 or trim_type == 0:
            remove_leading(view, edit)
        if trim_type == 2 or trim_type == 0:
            remove_trailing(view, edit)


class RemoveBlankLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        regions = all_regions(view, True)
        for region in regions:
            s = strip(view.substr(region))
            if len(s) == 0:
                view.erase(edit, sublime.Region(region.a, region.a + 1))
