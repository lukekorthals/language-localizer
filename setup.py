from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Language Localizer',
    url='https://github.com/lukekorthals/language-localizer',
    author='Luke Korthals',
    author_email='luke-korthals@outlook.de',
    packages=['language_localizer'],
    install_requires=[
        'exptools2 @ git+ssh://github.com/VU-Cog-Sci/exptools2/'
        ],
    package_data={
        "language_localizer": ["stimuli/hand-press-button-4.jpg",
                               "stimuli/langloc_fmri_run1_stim_set1.csv",
                               "stimuli/langloc_fmri_run1_stim_set2.csv",
                               "stimuli/langloc_fmri_run1_stim_set3.csv",
                               "stimuli/langloc_fmri_run1_stim_set4.csv",
                               "stimuli/langloc_fmri_run1_stim_set5.csv",
                               "stimuli/langloc_fmri_run2_stim_set1.csv",
                               "stimuli/langloc_fmri_run2_stim_set2.csv",
                               "stimuli/langloc_fmri_run2_stim_set3.csv",
                               "stimuli/langloc_fmri_run2_stim_set4.csv",
                               "stimuli/langloc_fmri_run2_stim_set5.csv"]

    },
    version='0.1',
    license='MIT',
    description='A python implementation of the language localizer developed by Fedorenko et al. (2010)',
    long_description=open('README.md').read(),
)