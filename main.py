
from language_localizer.language_localizer_session import LanguageLocalizerEyeTrackerSession

# Create a session object
session = LanguageLocalizerEyeTrackerSession(
    subj_nr=1, 
    run_nr=1, 
    set_nr=1, 
    settings_file="/Users/lukekorthals/Desktop/repositories/language-localizer/settings.yml",
    eyetracker_on=False)

# Run the session
session.run()
