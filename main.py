
from language_localizer.language_localizer_session import LanguageLocalizerEyeTrackerSession
from language_localizer.language_localizer_stimuli import LanguageLocalizerSentenceStimSet, LanguageLocalizerAttentionCheckStim

# Create a session object
session = LanguageLocalizerEyeTrackerSession(
    subj_nr=1, 
    run_nr=1, 
    set_nr=1, 
    settings_file="/Users/lukekorthals/Desktop/repositories/language-localizer/settings.yml",
    sentence_stim_set=LanguageLocalizerSentenceStimSet(complete_path=None), # set complete path for custom sets
    attention_check_stim=LanguageLocalizerAttentionCheckStim(complete_path=None), # set complete path for custom image
    eyetracker_on=False)

# Run the session
session.run()
