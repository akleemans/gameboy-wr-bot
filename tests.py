#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from fetch import get_readable_time


class Tests(unittest.TestCase):

    def test_duration_seconds(self):
        self.assertEqual('34s 550ms', get_readable_time('PT34.550S'))
        self.assertEqual('37s 403ms', get_readable_time('PT37.403S'))
        self.assertEqual('2s 190ms', get_readable_time('PT2.190S'))

    def test_duration_minutes(self):
        self.assertEqual('2m 8s 470ms', get_readable_time('PT2M8.470S'))
        self.assertEqual('43m 14s', get_readable_time('PT43M14S'))
        self.assertEqual('1m 17s 530ms', get_readable_time('PT1M17.530S'))
        self.assertEqual('26m 56s 274ms', get_readable_time('PT26M56.274S'))
        self.assertEqual('27m 1s 682ms', get_readable_time('PT27M1.682S'))
        self.assertEqual('4m 12s', get_readable_time('PT4M12S'))
        self.assertEqual('55m 33s', get_readable_time('PT55M33S'))

    def test_duration_hours(self):
        self.assertEqual('1h 17m 50s 100ms',
                         get_readable_time('PT1H17M50.100S'))
        self.assertEqual('3h 11m 28s', get_readable_time('PT3H11M28S'))
