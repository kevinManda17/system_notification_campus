import re
from datetime import datetime

# Email Descriptor
class EmailDescriptor:
    """
    Valide les adresses e-mail personnelles.
    Se base sur un pattern standard RFC5322 simplifié.
    """
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('_email_perso', instance.email_perso_db)

    def __set__(self, instance, value):
        if not value:
            raise ValueError("L'email personnel ne peut pas être vide.")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError(f"Email invalide: {value}")
        instance.__dict__['_email_perso'] = value



# Phone Descriptor
class PhoneDescriptor:
    """
    Valide le format des numéros de téléphone internationaux.
    Ex : +243970000000 (10 à 15 chiffres après le +)
    """
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('_phone', instance.phone_db)

    def __set__(self, instance, value):
        if not value:
            raise ValueError("Le numéro de téléphone ne peut pas être vide.")
        if not re.match(r'^\+\d{10,15}$', value):
            raise ValueError(f"Numéro de téléphone invalide: {value}")
        instance.__dict__['_phone'] = value


#Priority Descriptor
class PriorityDescriptor:
    """
    Gère la priorité d'une notification.
    Valeurs possibles : LOW, MEDIUM, HIGH, URGENT.
    """
    VALID_PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT']

    def __init__(self, default='LOW'):
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('_priority', getattr(instance, 'priority', self.default))

    def __set__(self, instance, value):
        if value not in self.VALID_PRIORITIES:
            raise ValueError(f"Priorité invalide: {value}. Attendu: {', '.join(self.VALID_PRIORITIES)}")
        instance.__dict__['_priority'] = value



#Time Window Descriptor
class TimeWindowDescriptor:
    """
    Gère une fenêtre temporelle de validité de la notification.
    Attendu : un tuple (start_datetime, end_datetime).
    """
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('_time_window', (
            getattr(instance, 'time_window_start', None),
            getattr(instance, 'time_window_end', None)
        ))

    def __set__(self, instance, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Time window invalide : attendre un tuple (start, end)")

        start, end = value
        if not (isinstance(start, datetime) and isinstance(end, datetime)):
            raise ValueError("Les deux valeurs de la fenêtre doivent être des objets datetime.")
        if end <= start:
            raise ValueError("La date de fin doit être postérieure à la date de début.")

        instance.__dict__['_time_window'] = (start, end)


# class PriorityDescriptor:
#     VALID_PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'URGENT']

#     def __init__(self, default='LOW'):
#         self.default = default

#     def __get__(self, instance, owner):
#         if instance is None:
#             return self
#         # On ne cherche QUE dans __dict__
#         return instance.__dict__.get('_priority', self.default)

#     def __set__(self, instance, value):
#         if value not in self.VALID_PRIORITIES:
#             raise ValueError(f"Priorité invalide: {value}")
#         instance.__dict__['_priority'] = value


# class TimeWindowDescriptor:
#     def __get__(self, instance, owner):
#         if instance is None:
#             return self
#         return instance.__dict__.get('_time_window', (
#             getattr(instance, 'time_window_start', None),
#             getattr(instance, 'time_window_end', None)
#         ))

#     def __set__(self, instance, value):
#         if not isinstance(value, tuple) or len(value) != 2:
#             raise ValueError("Time window invalide : attendre un tuple (start, end)")

#         start, end = value

#         from datetime import datetime
#         if not isinstance(start, datetime) or not isinstance(end, datetime):
#             raise ValueError("Les deux valeurs doivent être des datetime")

#         if end <= start:
#             raise ValueError("La fin doit être après le début")

#         instance.__dict__['_time_window'] = (start, end)
