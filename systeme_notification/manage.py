import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'systeme_notification.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "impossible d'importer Django. Assurez-vous qu'il est installé et "
            "disponible sur votre PYTHONPATH environment variable. "
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
