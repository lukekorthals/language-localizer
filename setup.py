from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Language Localizer',
    url='https://github.com/lukekorthals/language-localizer',
    author='Luke Korthals',
    author_email='luke-korthals@outlook.de',
    packages=['language_localizer'],
    install_requires=[
        'psychopy>=3.0.4',
        'pyyaml',
        'pandas>=0.23.0',
        'numpy>=1.14.3',
        'msgpack_numpy',
        'exptools2 @ git+ssh://github.com/VU-Cog-Sci/exptools2/'
        ],
    version='0.1',
    license='MIT',
    description='A python implementation of the language localizer developed by Fedorenko et al. (2010)',
    long_description=open('README.md').read(),
)