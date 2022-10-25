#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from core_app.global_containers import WORKSDIR
from dtstructure.fileutils import rdir_to_tree

def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v

def dew_init():
    update_global_dict(WORKSDIR, rdir_to_tree('dtm\\works'))
    print('Works directory snapshot:', WORKSDIR)

def main():
    """Run administrative tasks."""
    dew_init()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'de_web.settings')
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
    main()
