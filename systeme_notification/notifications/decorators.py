import time
from datetime import datetime
from .descriptors import TimeWindowDescriptor
from .registry import GlobalRegistry


# Décorateur de méthode simple
def message(func):
    """
    Décorateur de méthode classique.
    Trace les appels avant et après exécution.
    """
    def wrapper(self, *args, **kwargs):
        print(f"[Message] → Appel de {func.__name__}()")
        result = func(self, *args, **kwargs)
        print(f"[Message] ← Fin de {func.__name__}() → {result}")
        return result
    return wrapper


# Décorateurs de classes orientés POO
class AddPerformanceTracking:
    """
    Décorateur de classe mesurant les performances de la méthode principale 'evacuer'.
    Utilise le TimeWindowDescriptor pour tracer la durée d’exécution.
    """
    def __call__(self, cls):
        if hasattr(cls, "evacuer"):
            original = cls.evacuer

            def tracked(self, *args, **kwargs):
                start = time.time()
                start_time = datetime.now()

                print(f"[Performance]  Début {cls.__name__}.evacuer à {start_time.strftime('%H:%M:%S')}")
                result = original(self, *args, **kwargs)
                end = time.time()
                end_time = datetime.now()

                # Injection dynamique de la fenêtre temporelle dans l'instance
                self.time_window = (start_time, end_time)

                print(f"[Performance]  Fin {cls.__name__}.evacuer ({end - start:.3f}s)")
                return result

            cls.evacuer = tracked
        return cls


class AutoConfigurationValidation:
    """
    Vérifie que toutes les propriétés requises existent dans la classe.
    """
    def __call__(self, cls):
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if hasattr(cls, 'required_fields'):
                for field in cls.required_fields:
                    if not hasattr(self, field):
                        raise ValueError(f"[Validation] {cls.__name__} manque le champ requis : {field}")
        cls.__init__ = new_init
        return cls


class RegisterInGlobalRegistry:
    """
    Enregistre automatiquement les classes décorées dans un registre global.
    """
    def __call__(self, cls):
        GlobalRegistry.register(cls.__name__, cls)
        print(f"[Registry] Classe enregistrée : {cls.__name__}")
        return cls



class AddCircuitBreaker:
    """
    Décorateur de classe gérant les exceptions pour éviter la panne totale du système.
    """
    def __call__(self, cls):
        if hasattr(cls, "evacuer"):
            original = cls.evacuer

            def safe(self, *args, **kwargs):
                try:
                    return original(self, *args, **kwargs)
                except Exception as e:
                    print(f"[CircuitBreaker] Erreur interceptée dans {cls.__name__} : {e}")
                    return None
            cls.evacuer = safe
        return cls
