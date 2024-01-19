# language-localizer
Python replication of language localizer originally written in Matlab by Fedorenko et al. (2010) to be used with [psychopy](https://psychopy.org/) (Peirce et al., 2019) and [exptools2](https://github.com/VU-Cog-Sci/exptools2).

# Installation
On macOS you need to install `wxPython` and `gevent` seperately. The remaining requirements will be installed when you install the language-localizer package.

On Windows, simply using `pip install git+https://github.com/lukekorthals/language-localizer` may work. 

```
conda create -n language-localizer python=3.9
conda activate language-localizer
conda install conda-forge::wxpython
conda install gevent
pip install git+https://github.com/lukekorthals/language-localizer
```

# Quickstart
Make sure your settings.yml includes the following parameters to define stimuli settings and key presses.
Unless you change any values, the text and fixation cross will be black and are displayed for the same durations as in the original experiment by Fedorenko et al. (2010). 
You can use the following keys. 
- Press `space` to start when "This is the instruction text" is displayed. 
- Press `t` to simulate the mri sync when "Waiting for scanner ..." is displayed. 
- Press `space` whenever the attention check image is being displayed
- Press `escape` to gracefully exit the session early.

```yaml
language_localizer:
  responses:
    attention_check: space
    escape: escape
  stimuli: 
    phase_name_blank: ll_blank
    phase_name_word: ll_word
    phase_name_attention: ll_attention
    phase_name_fix: ll_fix
    phase_duration_blank: 100
    phase_duration_word: 450
    phase_duration_attention: 400
    phase_duration_fix: 1400
    text_color: [-1, -1, -1]
    fix_color: [-1, -1, -1]
    win_color: [1, 1, 1]
  mri:
    sync: t
  text:
    instructions: This is the instruction text
    awaiting_scanner: Waiting for scanner ...
```

To run a simple example use the following code. 

```python
from language_localizer.language_localizer_session import LanguageLocalizerEyeTrackerSession
from language_localizer.language_localizer_stimuli import LanguageLocalizerSentenceStimSet, LanguageLocalizerAttentionCheckStim

# Create a session object
session = LanguageLocalizerEyeTrackerSession(
  subj_nr=1,
  run_nr=1, 
  set_nr=1, 
  settings_file="<PATH TO YOUR SETTINGS FILE>",
  output_dir: str="logs"
  )

# Run the session
session.run()
```

# Important Settings
All important settings should be defined in the settings.yml with the highest order key being "language_localizer".

**Responses**
Keys used during the experiment. 
- `attention_check`: starts the experiment after the instruction and should be pressed when seeing the attention check image
- `escape`: close the experiment gracefully early

```yaml
responses:
    attention_check: space
    escape: escape
```

**Stimuli**
All settings related to stimuli. 
- `phase_name_...`: phase names included in the log file
- `phase_duration_...`: phase durations defined in milliseconds to determine how long each stimulus is presented
- `text_color`: color of the (non-)words
- `fix_color`: color of fixation cross
- `win_color`: background color of the screen


```yaml
stimuli: 
    phase_name_blank: ll_blank
    phase_name_word: ll_word
    phase_name_attention: ll_attention
    phase_name_fix: ll_fix
    phase_duration_blank: 100
    phase_duration_word: 450
    phase_duration_attention: 400
    phase_duration_fix: 1400
    text_color: [-1, -1, -1]
    fix_color: [-1, -1, -1]
    win_color: [1, 1, 1]
```

**MRI**
Settings concerning the mri scanner. 
- `sync`: flag representing the sync signal

```yaml
mri:
    sync: t
```

**Text**
All non stimuli texts used in the experiment.
- `instructions`: displayed at the begining of the experiment
- `awaiting_scanner`: displayed when waiting for a scanner signal

```yaml
text:
    instructions: This is the instruction text
    awaiting_scanner: Waiting for scanner ...
```

# Documentation
## LanguageLocalizerEyeTrackerSession
This is the main class of the language localizer. It inherits from `exptools2.core.Session` and `exptools2.core.EyeTrackerSession` and runs the experiment.

It also loads the stimuli used during the experiment. The default uses the same stimulus sets as Fedorenko et al. (2010) which are determined by the run and set numbers. However, it is also possible to supply paths to custom stimuli using the complete_path parameter in LanguageLocalizerSentenceStimSet and LanguageLocalizerAttentionCheckStim.

Parameters:
- `subj_nr`: int, subject number
- `run_nr`: int, run number, determines which stimulus file to use
- `set_nr`: int, set number, determines which stimulus file to use
- `settings_file`: str, path to the settings.yml commonly used for experiments implemented in exptools2
- `sentence_stim_set`: LanguageLocalizerSentenceStimSet, LanguageLocalizerSentenceStimSet object which either loads standard stimuli from the package resources or a custom stimuli file according to the complete_path parameter
- `attention_check_stim`: LanguageLocalizerAttentionCheckStim, LanguageLocalizerAttentionCheckStim object which either loads the standard attention check image from the package resources or a custom image file according to the complete_path parameter
- `eyetracker_on`: bool, whether to use the eyetracker or not

## LanguageLocalizerSentenceStimSet
This class is used to load the sentences from a standard sentence stim set according to the run and set numbers and provide it to the session class. Alternatively, the `complete_path` parameter can be used to load a custom sentence stim set instead.

Parameters:
- `complete_path`: str, path to a custom stimulus file. 

When using a custom stimulus file, it should have 14 columns and include a header. 
Some columns are technically not used, but are included to match the file fornmat used by Fedorenko et al. (2010).
- Column `1` is irrelevant.
- Columns `2-13` each contain a (non-)word included in a twelve-word sentence.
- Column `14` indicates whether a sentence includes words (S) or non-words (N). This information is logged in the output file.

```csv
stim1,stim2,stim3,stim4,stim5,stim6,stim7,stim8,stim9,stim10,stim11,stim12,stim13,stim14
1,JUST,THE,BAREST,SUGGESTION,OF,A,HEEL,IS,FOUND,ON,TEENAGE,PUMPS,S
2,TO,THE,DIRECTORS,THE,PROBLEM,APPEARED,A,MATTER,OF,INTRIGUE,OR,DIPLOMACY,S
3,THERE,WAS,LITTLE,LIKELIHOOD,OF,ANY,CUSTOMERS,WALKING,IN,AT,THAT,HOUR,S
1,POME,OY,REE,HOLILY,SHOURN,NE,SLEOMING,WHIMP,REE,RERE,OS,OFUKE,N
2,OT,MOMP,VO,DETLERENCE,FROT,MOGS,ELIBONCE,POLVED,RO,OP,UMMOSITE,COMBLISION,N
3,CHITMENTS,OY,ORLS,TROR,WENDERT,COONGLIES,COURN,MOMICONLY,NE,SOOZED,AR,CONTROGOME,N
4,E,WOSE,RO,SPEONT,REE,INTLOSSION,OY,O,COMBOUSE,FUMS,OY,CHIGSHEN,N
```

## LanguageLocalizerAttentionCheckStim
This class is used to provide the path to the standard attention check image to the session class. Alternatively, the `complete_path` parameter can be used to provide the path to a custom image instead. 

Parameters:
- `complete_path`: str, path to a custom image file. 

**Default Image**

<img src="language_localizer/stimuli/hand-press-button-4.jpeg" alt="hand-press-button-4.jpeg" width="300" height="auto">


## LanguageLocalizerTrial
Superclass for all trials used in the language localizer. Inherites from `exptools2.core.Trial`. 

Importantly, in contrast to `exptools2.core.Trial`, it expects phase_durations to be defined in milliseconds 
which are then transformed into frames according to the actual framerate. This behaviour is inherited by all subclasses. 

Parameters:
- `session`: LanguageLocalizerEyeTrackerSession, the main session object documented above
- `timing`: str, Units of the phase durations. Should be set to "milliseconds" so that frames are calculated according to the actual frame rate.
- `phase_durations` array like, remember to set these in milliseconds. 
- other parameters: refer to exptools2.core.Trial

The following code chunk illustrates how phase durations are calculated.
```python
class LanguageLocalizerTrial(Trial):

  def __init__(...):
    # ...
    if timing == "milliseconds":
      actual_framerate = session.actual_framerate
      phase_durations = [int(duration/1000 * actual_framerate) for duration in phase_durations]
      timing = "frames"  
    # ...
```

## LanguageLocalizerAttentionTrial
Trial class to display the attention check image. Inherites from `language_localizer.LanguageLocalizerTrial`. 

Loads the image supplied by `LanguageLocalizerAttentionCheckStim` to `LanguageLocalizerEyeTrackerSession`. 
Displays the image stimulus according to the `phase_durations` using the `draw()` method.

## LanguageLocalizerSentenceTrial
Trial class to display each (non-)word of a sentence. Inherites from `language_localizer.LanguageLocalizerTrial`. 

Loads the (non-)words supplied by `LanguageLocalizerSentenceStimSet`to `LanguageLocalizerEyeTrackerSession`. 
Displays each word according to the `phase_durations` using the `draw()` method.

## LanguageLocalizerFixationTrial
Trial class to display a fixation cross. Inherites from `language_localizer.LanguageLocalizerTrial`. 

Displays a + sign used as a fixation cross according to the `phase_durations` using the `draw()` method.


# References
- Fedorenko, E., Hsieh, P.-J., Nieto-Castañón, A., Whitfield-Gabrieli, S., & Kanwisher, N. (2010). New method for fMRI investigations of language: Defining ROIs functionally in individual subjects. Journal of Neurophysiology, 104(2), 1177–1194. https://doi.org/10.1152/jn.00032.2010
- Peirce, J. W., Gray, J. R., Simpson, S., MacAskill, M. R., Höchenberger, R., Sogo, H., Kastman, E., Lindeløv, J. (2019). PsychoPy2: experiments in behavior made easy. Behavior Research Methods. 10.3758/s13428-018-01193-y Titel anhand dieser DOI in Citavi-Projekt übernehmen
