from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Language Localizer',
    url='https://github.com/lukekorthals/language-localizer',
    author='Luke Korthals',
    author_email='luke-korthals@outlook.de',
    packages=['language_localizer'],
    install_requires=[
        'exptools2 @ git+https://github.com/VU-Cog-Sci/exptools2/',
        'psychopy-mri-emulator'
        ],
    package_data={
        "language_localizer": ["pkg_resources/stimuli/*",
                               "pkg_resources/settings/*"]

    },
    version='0.1',
    license='MIT',
    description='A python implementation of the language localizer developed by Fedorenko et al. (2010)',
    long_description=open('README.md').read(),
)