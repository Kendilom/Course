import unittest
from unittest import TestCase

from homeworks import *


class Test(TestCase):
    def test_total_sum(self):
        expected_result = 100

        actual_result = total_sum("25,50,15,10")
        self.assertEqual(actual_result, expected_result)

    def test_get_area(self):
        valid_params = [(4, 6), (8, 8)]
        expected_result = (24, 64)
        for width, height in valid_params: #поигрался с тестами валидных значений хотя тут и не обязательноad
            with (self.subTest(f'{height}, {width}')):
                actual_side1 = width
                actual_side2 = height
                self.assertGreater(actual_side1, 0)
                self.assertGreater(actual_side2, 0)
        for width, height in valid_params:
            actual_result = get_area(width, height)
            self.assertIn(actual_result, expected_result)

    def test_get_perimeter(self):
        test_width, test_height, = 13, 10
        expected_result = 46

        actual_result = get_perimeter(test_width, test_height)
        self.assertEqual(actual_result, expected_result)


    def test_unique_symb_check(self):
        test_string = 'positive_10+_symb_string'
        expected_result = True

        actual_result = unique_symb_check(test_string)
        self.assertEqual(actual_result, expected_result)

    def test_find_str(self): #принимает лист с чем угодно и возвращает только стринги
        test_list = ['666666', True, 'Cat', 41, ("triangle", 50), 20]
        expected_result = ['666666', 'Cat']

        actual_result = find_str(test_list)
        self.assertEqual(actual_result, expected_result)

    def test_the_longest(self): #принимает лист из str и выводит самый длинный
        test_list = ['Кофта', 'Колодец', 'Тетраедр', 'Муха']
        expected_result = 'Тетраедр'

        actual_result = the_longest(test_list)
        self.assertEqual(actual_result, expected_result)

    def test_tipa_reverse(self): #принимает стрингу и реверсит
        test_string = 'Vlad'
        expected_result = 'dalV'

        actual_result = tipa_reverse(test_string)
        self.assertEqual(actual_result, expected_result)

    def test_serednie_arifmet(self):
        test_list = [10, 20, 30]
        expected_result = 20

        actual_result = serednie_arifmet(test_list)
        self.assertEqual(actual_result, expected_result)

    def test_validate_password(self): #функция клода, возвращает пустой список если нет проблем с паролем
        valid_password = 'DfBw[p6tR'
        expected_result = []

        actual_result = validate_password(valid_password)
        self.assertEqual(actual_result, expected_result)

    def test_is_palindorme(self):
        valid_word = 'ded'
        expected_result = 'Is palindrome'

        actual_result = is_palindrome(valid_word)
        self.assertEqual(actual_result, expected_result)
if __name__ == '__main__':
    unittest.main()