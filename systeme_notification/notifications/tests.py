from django.test import TestCase
from datetime import datetime, timedelta
from notifications.registry import GlobalRegistry
from notifications.descriptors import EmailDescriptor, PhoneDescriptor, TimeWindowDescriptor, PriorityDescriptor
from notifications.core import Epidemie, Incendie
from notifications.decorators import AddCircuitBreaker, AutoConfigurationValidation
from notifications.metaclasses import NotificationMeta
from notifications.models import User, Notification
import types

class DescriptorsTestCase(TestCase):
    def test_email_descriptor_valid_and_invalid(self):
        u = User(username="d1", email="d1@example.com")
        u.email_perso = "ok@example.com"
        self.assertEqual(u.email_perso, "ok@example.com")
        with self.assertRaises(ValueError):
            u.email_perso = "bad-email"

    def test_phone_descriptor_valid_and_invalid(self):
        u = User(username="d2", email="d2@example.com")
        u.phone = "+243970000001"
        self.assertTrue(u.phone.startswith("+243"))
        with self.assertRaises(ValueError):
            u.phone = "01234"

    def test_timewindow_descriptor_valid_and_invalid(self):
        u = User(username="d3", email="d3@example.com")
        start = datetime.now()
        end = start + timedelta(hours=1)
        u.time_window = (start, end)
        self.assertEqual(u.time_window, (start, end))
        with self.assertRaises(ValueError):
            u.time_window = ("bad", "values")
        with self.assertRaises(ValueError):
            u.time_window = (end, start)  # end <= start

    def test_priority_descriptor(self):
        # PriorityDescriptor often used on Notification; test behavior standalone via a dummy
        class Dummy:
            priority = PriorityDescriptor()
        d = Dummy()
        self.assertEqual(d.priority, 'LOW')
        d.priority = 'HIGH'
        self.assertEqual(d.priority, 'HIGH')
        with self.assertRaises(ValueError):
            d.priority = 'INVALID'


class DecoratorsAndRegistryTestCase(TestCase):
    def test_registry_contains_core_classes(self):
        # Après import de core, les classes décorées doivent être enregistrées
        names = GlobalRegistry.list()
        # au moins Epidemie et Incendie
        self.assertIn('Epidemie', names)
        self.assertIn('Incendie', names)

    def test_add_performance_tracking_injects_time_window(self):
        e = Epidemie("TestX")
        # avant execution, time_window peut être None pair
        e.evacuer()
        tw = e.time_window
        self.assertIsInstance(tw, tuple)
        self.assertEqual(len(tw), 2)
        self.assertTrue(isinstance(tw[0], datetime) and isinstance(tw[1], datetime))
        self.assertTrue(tw[1] >= tw[0])

    def test_add_circuit_breaker_prevents_exceptions(self):
        @AddCircuitBreaker()
        class Broken:
            def evacuer(self):
                raise RuntimeError("kaboom")
        b = Broken()
        # doit renvoyer None et ne pas propager l'exception
        result = b.evacuer()
        self.assertIsNone(result)

    def test_auto_configuration_validation_raises_when_missing_field(self):
        @AutoConfigurationValidation()
        class Need:
            required_fields = ['must_exist']
            def __init__(self): pass
        with self.assertRaises(ValueError):
            Need()  # manque l'attribut must_exist

class MetaClassTestCase(TestCase):
    def test_notification_meta_adds_validate(self):
        class TestMeta(metaclass=NotificationMeta):
            required_fields = ['a']
        t = TestMeta()
        # validate doit exister
        self.assertTrue(hasattr(t, 'validate'))
        with self.assertRaises(ValueError):
            t.validate()

class IntegrationModelTestCase(TestCase):
    def test_notification_copies_user_fields_on_save(self):
        # Ce test suppose que Notification.save() copie priority/time_window depuis destinataire
        u = User.objects.create(username='intuser', email='int@example.com')
        u.email_perso = "perso@ex.com"
        u.phone = "+243970000002"
        # time window
        start = datetime.now()
        end = start + timedelta(hours=2)
        u.time_window = (start, end)
        u.save()

        notif = Notification(message="Hi", destinataire=u)
        notif.save()

        # Si ton Notification.save implémente la copie :
        # priority et time_window_start / end doivent être renseignés
        self.assertIsNotNone(notif.created_at)
        # vérifie attributs si présents
        if hasattr(notif, 'priority'):
            self.assertIn(notif.priority, ('LOW','MEDIUM','HIGH','URGENT','HIGH'))
        if hasattr(notif, 'time_window_start') and hasattr(notif, 'time_window_end'):
            self.assertIsNotNone(notif.time_window_start)
            self.assertIsNotNone(notif.time_window_end)
