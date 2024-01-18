# Contains the LanguageLocalizerSession class, which is used to run a localizer session.

from datetime import datetime
from exptools2.core.eyetracker import PylinkEyetrackerSession
from language_localizer.language_localizer_trials import LLFixationTrial, LLAttentionTrial, LLSentenceTrial
from language_localizer.language_localizer_stimuli import LanguageLocalizerSentenceStimSet, LanguageLocalizerAttentionCheckStim


class LanguageLocalizerEyeTrackerSession(PylinkEyetrackerSession):
    """LanguageLocalizer session class."""

    def __init__(self,
                 subj_nr: int,
                 run_nr: int,
                 set_nr: int,
                 output_dir: str="logs",
                 settings_file: str =None,
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
            LLFixationTrial(session=self, trial_nr=0)
        ]

        trial_nr = 1
        sentence_trials = 0
        # Add all sentences as trials
        for sentence in self.sentences:
            words = sentence[1:-1] # omit first element (number) and last element (condition)
            condition = sentence[-1] # S=Words or N=Nonwords
            self.trials.append(
                LLSentenceTrial(session=self, trial_nr=trial_nr, words=words, condition=condition)
            )
            sentence_trials += 1
            # Add attention reminder after each sentence
            self.trials.append(
                LLAttentionTrial(session=self, trial_nr=trial_nr+1)
            )
            trial_nr += 2 # increase trial number by 2 (sentence + attention reminder)
            # After every 12 trials, add a fixation trial
            if sentence_trials%12 == 0:
                self.trials.append(
                    LLFixationTrial(session=self, trial_nr=trial_nr)
                )
                trial_nr += 1 # increase trial number by 1 (fixation trial)

    def run(self):
        """Run the session."""

        # Calibrate eye tracker
        # TODO: calibrate only first session?
        if self.run_nr == 1:
            if self.eyetracker_on:
                self.calibrate_eyetracker()

        # Instructions
        # TODO: add instructions
        self.display_text(
            "This is the instruction", 
            keys=self.settings["responses"]["press"], 
            color=self.settings["stimuli"]["text_color"])  

        # Start eye tracker
        if self.eyetracker_on:
            self.start_recording_eyetracker()

        # Wait for fMRI trigger
        self.display_text("Waiting for scanner...",
                          keys=self.settings['mri'].get('sync', 't'),
                          color=self.settings["stimuli"]["text_color"])

        # Start the experiment
        self.start_experiment()

        # Run trials	
        for trial in self.trials:
            trial.run()

            # Listen for escape key
            if trial.last_resp == self.settings['design']['escape_resp']:
                break

        # Gracefully close the session and create log
        self.close()
