from django.test import TestCase
from algorithms import models


class TestScenarios(TestCase):

    def test_scenario_0(self):
        days_of_power = models.get_days_of_power_3_loans(
            R1=1000,
            D1=3,
            R2=500,
            D2=10,
            R3=1500,
            D3=7,
            K=21000)
        self.assertEqual(days_of_power, 10)

    def test_scenario_1(self):
        days_of_power = models.get_days_of_power_3_loans(
            R1=3000, D1=3, R2=500, D2=10, R3=1500, D3=7, K=700000)
        self.assertEqual(days_of_power, 141)

    def test_scenario_2(self):
        days_of_power = models.get_days_of_power_3_loans(
            R1=500, D1=3, R2=500, D2=10, R3=500, D3=7, K=21000)
        self.assertEqual(days_of_power, 17)

    def test_scenario_3(self):
        days_of_power = models.get_days_of_power_3_loans(
            R1=1300, D1=0, R2=500, D2=0, R3=1500, D3=7, K=10000)
        self.assertEqual(days_of_power, 5)

    def test_scenario_4(self):
        days_of_power = models.get_days_of_power_3_loans(
            R1=10000, D1=3, R2=500, D2=10, R3=1500, D3=7, K=11000)
        self.assertEqual(days_of_power, 1)
