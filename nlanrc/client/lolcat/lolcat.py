#!/usr/bin/env python
#
# "THE BEER-WARE LICENSE" (Revision 43~maze)
#
# <maze@pyth0n.org> wrote these files. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.

from __future__ import print_function

import atexit
import math
import optparse
import os
import re
import sys
import time
from signal import SIG_DFL, SIGPIPE, signal

PY3 = sys.version_info >= (3,)

# override default handler so no exceptions on SIGPIPE
signal(SIGPIPE, SIG_DFL)


# Reset terminal colors at exit
def reset():
    sys.stdout.write("\x1b[0m")
    sys.stdout.flush()


atexit.register(reset)


STRIP_ANSI = re.compile(r"\x1b\[(\d+)(;\d+)?(;\d+)?[m|K]")
COLOR_ANSI = (
    (0x00, 0x00, 0x00),
    (0xCD, 0x00, 0x00),
    (0x00, 0xCD, 0x00),
    (0xCD, 0xCD, 0x00),
    (0x00, 0x00, 0xEE),
    (0xCD, 0x00, 0xCD),
    (0x00, 0xCD, 0xCD),
    (0xE5, 0xE5, 0xE5),
    (0x7F, 0x7F, 0x7F),
    (0xFF, 0x00, 0x00),
    (0x00, 0xFF, 0x00),
    (0xFF, 0xFF, 0x00),
    (0x5C, 0x5C, 0xFF),
    (0xFF, 0x00, 0xFF),
    (0x00, 0xFF, 0xFF),
    (0xFF, 0xFF, 0xFF),
)


class LolCat(object):
    def __init__(self, mode=256, output=sys.stdout):
        self.mode = mode
        self.output = output
        self.options = optparse.Values(
            defaults={
                "spread": 3.0,
                "freq": 0.1,
                "seed": 0,
                "animate": False,
                "duration": 12,
                "speed": 20.0,
                "force": False,
                "mode": 256,
                "charset_py2": "utf-8",
                "os": 246,
            }
        )

    def _distance(self, rgb1, rgb2):
        return sum(map(lambda c: (c[0] - c[1]) ** 2, zip(rgb1, rgb2)))

    def ansi(self, rgb):
        r, g, b = rgb

        if self.mode in (8, 16):
            colors = COLOR_ANSI[: self.mode]
            matches = [(self._distance(c, map(int, rgb)), i) for i, c in enumerate(colors)]
            matches.sort()
            color = matches[0][1]

            return "3%d" % (color,)
        else:
            gray_possible = True
            sep = 2.5

            while gray_possible:
                if r < sep or g < sep or b < sep:
                    gray = r < sep and g < sep and b < sep
                    gray_possible = False

                sep += 42.5

            if gray:
                color = 232 + int(float(sum(rgb) / 33.0))
            else:
                color = sum([16] + [int(6 * float(val) / 256) * mod for val, mod in zip(rgb, [36, 6, 1])])

            return "38;5;%d" % (color,)

    def wrap(self, *codes):
        return "\x1b[%sm" % ("".join(codes),)

    def rainbow(self, freq, i):
        r = math.sin(freq * i) * 127 + 128
        g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
        b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
        return [r, g, b]

    def cat(self, fd):
        if self.options.animate:
            self.output.write("\x1b[?25l")

        for line in fd:
            self.options.os += 1
            self.println(line, self.options)
        self.output.write("\n")

        if self.options.animate:
            self.output.write("\x1b[?25h")

    def println(self, s, options):
        s = s.rstrip()
        if options.force or self.output.isatty():
            s = STRIP_ANSI.sub("", s)

        if options.animate:
            self.println_ani(s, options)
        else:
            self.println_plain(s, options)

        # self.output.write('\n')
        self.output.flush()
        if os.name == "nt":
            self.output.println()

    def println_ani(self, s, options):
        if not s:
            return

        for i in range(1, options.duration):
            self.output.write("\x1b[%dD" % (len(s),))
            self.output.flush()
            options.os += options.spread
            self.println_plain(s, options)
            time.sleep(1.0 / options.speed)

    def println_plain(self, s, options):
        for i, c in enumerate(s if PY3 else s.decode(options.charset_py2, "replace")):
            rgb = self.rainbow(options.freq, options.os + i / options.spread)
            self.output.write(
                "".join([self.wrap(self.ansi(rgb)), c if PY3 else c.encode(options.charset_py2, "replace"),])
            )
        if os.name == "nt":
            self.output.print()


def detect_mode(term_hint="xterm-256color"):
    """
    Poor-mans color mode detection.
    """
    if "ANSICON" in os.environ:
        return 16
    elif os.environ.get("ConEmuANSI", "OFF") == "ON":
        return 256
    else:
        term = os.environ.get("TERM", term_hint)
        if term.endswith("-256color") or term in ("xterm", "screen"):
            return 256
        elif term.endswith("-color") or term in ("rxvt",):
            return 16
        else:
            return 256  # optimistic default
