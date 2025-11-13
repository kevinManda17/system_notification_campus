# notifications/registry.py

class GlobalRegistry:
    """
    Registre global unique permettant d'enregistrer
    toutes les classes décorées ou dynamiques du système.

    Utilisé par les décorateurs comme RegisterInGlobalRegistry.
    """
    _registry = {}

    @classmethod
    def register(cls, name, obj):
        """Ajoute une classe ou instance dans le registre."""
        cls._registry[name] = obj
        print(f"[Registry] {name} ajouté au registre global.")

    @classmethod
    def get(cls, name):
        """Récupère une classe enregistrée par son nom."""
        return cls._registry.get(name)

    @classmethod
    def list(cls):
        """Retourne la liste des noms enregistrés."""
        return list(cls._registry.keys())

    @classmethod
    def clear(cls):
        """Vide complètement le registre."""
        cls._registry.clear()
        print("[Registry] Registre vidé.")
