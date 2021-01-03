#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta

from fetch import get_readable_time
from tools import get_age, DATE_FORMAT_SRC, get_age_from_now


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

    def test_age_simple(self):
        self.assertEqual(2, get_age('2020-12-15T13:30:11Z',
                                    '2020-12-15T11:30:11Z'))

    def test_age_reverse(self):
        self.assertEqual(2, get_age('2020-12-15T11:30:11Z',
                                    '2020-12-15T13:30:11Z'))

    def test_age_rounding(self):
        self.assertEqual(2, get_age('2020-12-15T11:25:11Z',
                                    '2020-12-15T13:30:11Z'))
        self.assertEqual(2, get_age('2020-12-15T11:35:11Z',
                                    '2020-12-15T13:30:11Z'))

    def test_age_days(self):
        self.assertEqual(26, get_age('2020-12-14T11:25:11Z',
                                     '2020-12-15T13:30:11Z'))
        self.assertEqual(122, get_age('2020-12-10T11:35:11Z',
                                      '2020-12-15T13:30:11Z'))

    def test_age_from_now(self):
        five_hours_ago = datetime.now() - timedelta(hours=5, minutes=12)
        self.assertEqual(5, get_age_from_now(
            five_hours_ago.strftime(DATE_FORMAT_SRC)))

    def test_age_from_now_old(self):
        old_run = datetime.strptime("2020-04-15T01:33:55Z", DATE_FORMAT_SRC)
        age_in_hours = get_age_from_now(old_run.strftime(DATE_FORMAT_SRC))
        self.assertLess(48, age_in_hours)
