#!/usr/bin/env python
import os
import sys

import django
import pytest


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_tests'
    django.setup()

    pytest_args = []

    if len(sys.argv) > 1:
        if '--coverage' in sys.argv:
            pytest_args += ['--cov=./audittrail']

    sys.exit(pytest.main(pytest_args))
