from abc import ABCMeta
from .registry import GlobalRegistry 


class NotificationMeta(ABCMeta):  
    """Métaclasse pour valider les champs requis et enregistrer les classes."""
    def __new__(cls, name, bases, attrs):
        if 'required_fields' in attrs:
            def validate(self):
                for field in attrs['required_fields']:
                    if getattr(self, field, None) is None:
                        raise ValueError(f"Champ requis manquant: {field}")
            attrs['validate'] = validate

        # Enregistrement global dans le registre centralisé
        GlobalRegistry.register(name, cls)

        return super().__new__(cls, name, bases, attrs)


class ChannelMeta(type):
    """Ajoute automatiquement un nom de canal à chaque sous-classe (sms, email…)."""
    def __new__(cls, name, bases, attrs):
        attrs['channel_name'] = name.lower()
        return super().__new__(cls, name, bases, attrs)


class TemplateMeta(type):
    """Ajoute une méthode render_template() aux classes avec template_fields."""
    def __new__(cls, name, bases, attrs):
        if 'template_fields' in attrs:
            def render_template(self):
                return f"{name} template: {attrs['template_fields']}"
            attrs['render_template'] = render_template
        return super().__new__(cls, name, bases, attrs)


class ConfigMeta(type):
    """Valide les dictionnaires de configuration dynamiques."""
    def __new__(cls, name, bases, attrs):
        if 'config' in attrs and not isinstance(attrs['config'], dict):
            raise ValueError(f"{name} config doit être un dict")
        return super().__new__(cls, name, bases, attrs)
