#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import argparse

sys.path.append(os.getcwd())

def main(args):
    """Run administrative tasks."""
    env = 'project.settings.production' if args.env == 'production' else 'project.settings.development'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', env)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Django manage.py command")
    parser.add_argument("--env", help="Enviroment: development (default) or production", default="development")
    args = parser.parse_args()
    main(args)
