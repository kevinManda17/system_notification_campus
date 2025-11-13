import time
from datetime import datetime
from .descriptors import TimeWindowDescriptor

global_registry = {}

# Décorateur de méthode simple
def message(func):
    def wrapper(self, *args, **kwargs):
        print(f"[Message] → Appel de {func.__name__}()")
        result = func(self, *args, **kwargs)
        print(f"[Message] ← Fin de {func.__name__}() → {result}")
        return result
    return wrapper



# Décorateurs de classes orientés POO
class AddPerformanceTracking:
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
    registry = {}

    def __call__(self, cls):
        self.registry[cls.__name__] = cls
        print(f"[Registry] Classe enregistrée : {cls.__name__}")
        return cls


class AddCircuitBreaker:
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
