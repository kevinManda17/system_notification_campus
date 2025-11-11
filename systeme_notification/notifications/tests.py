from django.test import TestCase
from .core import Epidemie, Incendie, Innondation, Securite

class UrgenceTests(TestCase):
    def test_epidemie_evacuer(self):
        e = Epidemie()
        e.evacuer()

    def test_incendie_evacuer(self):
        i = Incendie()
        i.evacuer()

    def test_innondation_evacuer(self):
        n = Innondation()
        n.evacuer()

    def test_securite_evacuer(self):
        s = Securite()
        s.evacuer()
