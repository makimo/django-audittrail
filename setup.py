from setuptools import setup, find_packages

setup(
    name             = 'django-audittrail',
    version          = '1.0.0',
    license          = 'MIT License',
    requires         = ['python (>= 3.6)', 'django (>= 2.0)'],
    provides         = ['audittrail'],
    description      = 'Module for logging user actions in Django.',
    url              = 'https://github.com/makimo/django-audittrail/',
    packages         = find_packages(),
    maintainer       = 'Kamil Kucharski',
    maintainer_email = 'kamil.kucharski@makimo.pl',

    classifiers  = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: System :: Logging',
    ],
)
