# Contains the LanguageLocalizerSession class, which is used to run a localizer session.

from datetime import datetime
from exptools2.core.eyetracker import PylinkEyetrackerSession
from functools import reduce
import pkg_resources

from language_localizer.language_localizer_trials import LanguageLocalizerFixationTrial, LanguageLocalizerAttentionTrial, LanguageLocalizerSentenceTrial
from language_localizer.language_localizer_stimuli import LanguageLocalizerSentenceStimSet, LanguageLocalizerAttentionCheckStim


class LanguageLocalizerEyeTrackerSession(PylinkEyetrackerSession):
    """LanguageLocalizer session class."""

    def __init__(self,
                 subj_nr: int,
                 run_nr: int,
                 set_nr: int,
                 settings_file: str = pkg_resources.resource_filename(__name__, f"pkg_resources/settings/settings.yml"),
                 output_dir: str="logs",
                 sentence_stim_set = LanguageLocalizerSentenceStimSet(),
                 attention_check_stim = LanguageLocalizerAttentionCheckStim(),
                 eyetracker_on: bool=False):
        """Initialize the LanguageLocalizerSession object.

        parameters
        ----------
        output_str : str
            Name for output-files. Defaults to current time + 'language_localizer'.
        output_dir : str
             Path to output-directory. Default: $PWD/logs.
        settings_file : str
            Path to the settings file. If None, exptools2's default_settings.yml is used.
        """

        # Set subject info
        self.subj_nr = subj_nr
        self.run_nr = run_nr
        self.set_nr = set_nr
        
        # Initialize super class
        output_str = self.set_output_str()
        try:
            super().__init__(output_str=output_str, 
                             output_dir=output_dir, 
                             settings_file=settings_file,
                             eyetracker_on=eyetracker_on)
        except Exception as e:
            print(f"Couldnt initialize session due to error in super().__init__: {e}")
        
        # Validate settings
        self.validate_settings()

        # Load stimuli and create trials
        self.sentences = sentence_stim_set.load(run_nr, set_nr)
        self.attention_check = attention_check_stim.load()
        self.create_trials()
    
    def set_output_str(self):
        """Set the output_str."""

        current_time = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        return f"language_localizer_{self.subj_nr}_{self.run_nr}_{self.set_nr}_{current_time}"

    def create_trials(self):
        """Creates the trials for the language localizer session."""

        self.trials = [
            LanguageLocalizerFixationTrial(session=self, trial_nr=0)
        ]

        trial_nr = 1
        sentence_trials = 0
        # Add all sentences as trials
        for sentence in self.sentences:
            words = sentence[1:-1] # omit first element (number) and last element (condition)
            condition = sentence[-1] # S=Words or N=Nonwords
            self.trials.append(
                LanguageLocalizerSentenceTrial(session=self, trial_nr=trial_nr, words=words, condition=condition)
            )
            sentence_trials += 1
            # Add attention reminder after each sentence
            self.trials.append(
                LanguageLocalizerAttentionTrial(session=self, trial_nr=trial_nr+1)
            )
            trial_nr += 2 # increase trial number by 2 (sentence + attention reminder)
            # After every 12 trials, add a fixation trial
            if sentence_trials%12 == 0:
                self.trials.append(
                    LanguageLocalizerFixationTrial(session=self, trial_nr=trial_nr)
                )
                trial_nr += 1 # increase trial number by 1 (fixation trial)
    
    def validate_settings(self):
        required_keys = [
            'language_localizer.responses.attention_check',
            'language_localizer.responses.escape',
            'language_localizer.stimuli.phase_name_blank',
            'language_localizer.stimuli.phase_name_word',
            'language_localizer.stimuli.phase_name_attention',
            'language_localizer.stimuli.phase_name_fix',
            'language_localizer.stimuli.phase_duration_blank',
            'language_localizer.stimuli.phase_duration_word',
            'language_localizer.stimuli.phase_duration_attention',
            'language_localizer.stimuli.phase_duration_fix',
            'language_localizer.stimuli.timing_attention_trial',
            'language_localizer.stimuli.timing_sentence_trial',
            'language_localizer.stimuli.timing_fixation_trial',
            'language_localizer.stimuli.text_color',
            'language_localizer.stimuli.fix_color',
            'mri.sync',
        ]

        for i, key in enumerate(required_keys):
            try:
                reduce(dict.get, key.split('.'), self.settings)
            except Exception as e:
                print("""
                      Some required settings are not set in your settings.yml
                      \nRemember to set values for the following keys:
                        \n- 'language_localizer.responses.attention_check',
                        \n- 'language_localizer.responses.escape',
                        \n- 'language_localizer.stimuli.phase_name_blank',
                        \n- 'language_localizer.stimuli.phase_name_word',
                        \n- 'language_localizer.stimuli.phase_name_attention',
                        \n- 'language_localizer.stimuli.phase_name_fix',
                        \n- 'language_localizer.stimuli.phase_duration_blank',
                        \n- 'language_localizer.stimuli.phase_duration_word',
                        \n- 'language_localizer.stimuli.phase_duration_attention',
                        \n- 'language_localizer.stimuli.phase_duration_fix',
                        \n- 'language_localizer.stimuli.timing_attention_trial',
                        \n- 'language_localizer.stimuli.timing_sentence_trial',
                        \n- 'language_localizer.stimuli.timing_fixation_trial',
                        \n- 'language_localizer.stimuli.text_color',
                        \n- 'language_localizer.stimuli.fix_color',
                        \n- 'mri.sync'
                      """)

    def run(self):
        """Run the session."""

        # Calibrate eye tracker
        # TODO: calibrate only first session?
        if self.run_nr == 1:
            if self.eyetracker_on:
                self.calibrate_eyetracker()

        # Instructions
        self.display_text(
            f"""In this task, you will read sentences or sequences of word-like nonwords (like “blicket” or “florp”). 
            \nThe materials will be shown one word/nonword at a time.
            \nYour task is to read the materials attentively as they appear. 
            \n\n(Press {self.settings["language_localizer"]["responses"]["attention_check"]} to continue)""",
            keys=self.settings["language_localizer"]["responses"]["attention_check"], 
            color=self.settings["language_localizer"]["stimuli"]["text_color"])  
        
        self.display_text(
            f"""Please read silently to yourself, as you would when reading a book. 
            \nDon’t be stressed if the words/nonwords seem to be appearing too quickly at first – 
            you will get used to the presentation speed after a few trials. 
            \n\n(Press {self.settings["language_localizer"]["responses"]["attention_check"]} to continue)""",
            keys=self.settings["language_localizer"]["responses"]["attention_check"], 
            color=self.settings["language_localizer"]["stimuli"]["text_color"])  
        
        self.display_text(
            f"""At the end of each sentence / nonword sequence, you'll see a picture of a finger pressing a button; 
            \nwhenever you see that picture, please press {self.settings["language_localizer"]["responses"]["attention_check"]}. 
            \n\n(Press {self.settings["language_localizer"]["responses"]["attention_check"]} to continue)""",
            keys=self.settings["language_localizer"]["responses"]["attention_check"], 
            color=self.settings["language_localizer"]["stimuli"]["text_color"])  
        
        self.display_text(
            f"""This task is included to help you stay alert throughout the task. 
            \nYour main task is to read attentively.
            \n\n(Press {self.settings["language_localizer"]["responses"]["attention_check"]} to start the experiment)""",
            keys=self.settings["language_localizer"]["responses"]["attention_check"], 
            color=self.settings["language_localizer"]["stimuli"]["text_color"])  

        # Start eye tracker
        if self.eyetracker_on:
            self.start_recording_eyetracker()

        # Wait for fMRI trigger
        self.display_text(
            "Waiting for scanner ...",
            keys=self.settings["mri"]["sync"],
            color=self.settings["language_localizer"]["stimuli"]["text_color"]
            )

        # Start the experiment
        self.start_experiment()

        # Run trials	
        for trial in self.trials:
            trial.run()

            # Listen for escape key
            if trial.last_resp == self.settings["language_localizer"]["responses"]["escape"]:
                break

        # Gracefully close the session and create log
        self.close()
