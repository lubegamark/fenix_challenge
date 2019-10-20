from django.test import TestCase
from algorithms import models


class TestScenarios(TestCase):

    def test_scenario_1(self):
        days_of_power = models.get_days_of_power_3_loans(
            R1=1000,
            D1=3,
            R2=500,
            D2=10,
            R3=1500,
            D3=7,
            K=21000)
        self.assertEqual(days_of_power, 10)
