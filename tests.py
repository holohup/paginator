from unittest import TestCase

from main import Interval, Paginator, generate_ascending_numbers_list


class TestTools(TestCase):
    """Custom utils tests."""

    def test_generate_ascending_numbers_string(self):
        expected_results = {
            (1, 5): ['1', '2', '3', '4', '5'],
            (1, 0): [],
            (1, 1): ['1'],
            (-5, 0): ['-5', '-4', '-3', '-2', '-1', '0'],
        }
        for numbers, expected in expected_results.items():
            with self.subTest(numbers=numbers, expected=expected):
                self.assertEqual(
                    generate_ascending_numbers_list(Interval(*numbers)),
                    expected,
                )


class TestBorderCases(TestCase):
    """Border cases for the paginator."""

    def test_empty_paginator(self):
        self.assertEqual(Paginator(0, 0, 0, 0).get_pages(), '')

    def test_single_page_pagination(self):
        for i in range(3):
            with self.subTest(i=i):
                self.assertEqual(Paginator(1, 1, i, i).get_pages(), '1')

    def test_two_pages_pagination(self):
        self.assertEqual(Paginator(1, 2, 1, 1).get_pages(), '1 2')

    def test_two_pages_with_no_boundaries_and_around_pagination(self):
        self.assertEqual(Paginator(2, 2, 0, 0).get_pages(), '... 2')
        self.assertEqual(Paginator(1, 2, 0, 0).get_pages(), '1 ...')


class TestRegularCases(TestCase):
    """Regular cases tests."""

    def test_parametrized_regular_cases(self):
        expected_results = {
            (3, 5, 1, 1): '1 2 3 4 5',
            (5, 5, 0, 1): '... 4 5',
            (3, 5, 0, 1): '... 2 3 4 ...',
            (3, 5, 1, 0): '1 ... 3 ... 5',
            (1, 5, 1, 0): '1 ... 5',
            (1, 2, 0, 0): '1 ...',
            (2, 5, 1, 0): '1 2 ... 5',
            (2, 5, 1, 1): '1 2 3 ... 5',
            (4, 5, 1, 0): '1 ... 4 5',
            (4, 10, 2, 2): '1 2 3 4 5 6 ... 9 10',
            (4, 10, 100, 2): '1 2 3 4 5 6 7 8 9 10',
            (4, 10, 1, 100): '1 2 3 4 5 6 7 8 9 10',
        }
        for params, result in expected_results.items():
            with self.subTest(params=params, result=result):
                self.assertEqual(Paginator(*params).get_pages(), result)


class TestInvalidPaginationParametersExceptions(TestCase):
    """Tests for the expected exceptions to be raised."""

    def test_current_page_bigger_then_pages_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            Paginator(current_page=5, total_pages=3, boundaries=1, around=1)

    def test_non_integer_on_init_raises_exception(self):
        with self.assertRaises(ValueError):
            Paginator(current_page=5.0, total_pages=30, boundaries=1, around=1)
            Paginator(current_page=5, total_pages='a', boundaries=1, around=1)
            Paginator(
                current_page=5, total_pages=30, boundaries=None, around=1
            )
            Paginator(
                current_page=5, total_pages=30, boundaries=1, around=False
            )

    def test_negative_values_on_init_raise_exception(self):
        defaults = {
            'current_page': 3,
            'total_pages': 10,
            'boundaries': 1,
            'around': 1,
        }
        for field in defaults.keys():
            presets = defaults.copy()
            with self.subTest(field=field):
                presets[field] = -1
                with self.assertRaises(ValueError):
                    Paginator(**presets)
