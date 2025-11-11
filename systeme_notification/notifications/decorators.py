import time

global_registry = {}

# Décorateur méthode
def message(func):
    def wrapper(self, *args, **kwargs):
        print(f"[Message] {func.__name__} appelé")
        result = func(self, *args, **kwargs)
        print(f"[Message] {func.__name__} retourné {result}")
        return result
    return wrapper

# Décorateur classe - suivi des performances
def add_performance_tracking(cls):
    original_evacuer = cls.evacuer
    def tracked_evacuer(self, *args, **kwargs):
        start = time.time()
        result = original_evacuer(self, *args, **kwargs)
        end = time.time()
        print(f"[Performance] {cls.__name__}.evacuer a pris {end-start:.3f}s")
        return result
    cls.evacuer = tracked_evacuer
    global_registry[cls.__name__] = cls
    return cls

# Décorateur classe - validation configuration
# def auto_configuration_validation(cls):
#     if hasattr(cls, 'required_fields'):
#         for field in cls.required_fields:
#             if not hasattr(cls, field):
#                 raise ValueError(f"{cls.__name__} manque le champ requis: {field}")
#     return cls
# Décorateur classe - validation configuration corrigé
def auto_configuration_validation(cls):
    """
    Valide que toutes les instances auront les attributs requis.
    Au lieu de vérifier à la création de la classe, on injecte une vérification dans __init__.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if hasattr(cls, 'required_fields'):
            for field in cls.required_fields:
                if not hasattr(self, field):
                    raise ValueError(f"{cls.__name__} instance manque le champ requis: {field}")

    cls.__init__ = new_init
    return cls



# Décorateur classe - enregistrement global
def register_in_global_registry(cls):
    global_registry[cls.__name__] = cls
    return cls

# Décorateur classe - circuit breaker simplifié
def add_circuit_breaker(cls):
    original_evacuer = cls.evacuer
    def safe_evacuer(self, *args, **kwargs):
        try:
            return original_evacuer(self, *args, **kwargs)
        except Exception as e:
            print(f"[Circuit Breaker] Erreur lors de l'évacuation: {e}")
            return None
    cls.evacuer = safe_evacuer
    return cls
