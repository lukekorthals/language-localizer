# language-localizer
Python replication of language localizer originally written in Matlab by Fedorenko et al. (2010) to be used with [psychopy](https://psychopy.org/) (Peirce et al., 2019) and [exptools2](https://github.com/VU-Cog-Sci/exptools2).

# Installation
Create new conda (or python venv) environment and install exptools and its dependencies.

```
conda create -n languagelocalizer python=3.9
conda activate languagelocalizer
conda install numpy scipy matplotlib pandas pyopengl pillow lxml openpyxl configobj pyyaml gevent greenlet msgpack-python psutil pytables requests[security] cffi seaborn cython pyzmq pyserial qt pyqt
conda install -c conda-forge pyglet pysoundfile python-bidi moviepy pyosf
pip install zmq json-tricks pyparallel sounddevice pygame pysoundcard psychopy_ext psychopy psychopy-sounddevice psychopy-mri-emulator
pip install git+https://github.com/VU-Cog-Sci/exptools2/
```

# References
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S., & Kanwisher, N. (2010). New method for fMRI investigations of language: Defining ROIs functionally in individual subjects. Journal of Neurophysiology, 104(2), 1177–1194. https://doi.org/10.1152/jn.00032.2010
- Peirce, J. W., Gray, J. R., Simpson, S., MacAskill, M. R., Höchenberger, R., Sogo, H., Kastman, E., Lindeløv, J. (2019). PsychoPy2: experiments in behavior made easy. Behavior Research Methods. 10.3758/s13428-018-01193-y Titel anhand dieser DOI in Citavi-Projekt übernehmen

