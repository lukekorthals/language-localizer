# Contains all subclasses of Trial used in the language localizer.

from exptools2.core import Session, Trial
from psychopy.visual import ImageStim, TextStim
from typing import Collection


class LanguageLocalizerAttentionTrial(Trial):
    """Trial to display the hand press icon as attention check."""

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 parameters: dict = None,
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True):
        """Initialize the ImageTrial object.

        parameters
        ----------
        phase_durations : Collection[int]
            The durations of the phases in milliseconds. Defaults to (400, 100) matching
            the original language localizer by Fedorenko et al. (2010).
        phase_names : Collection[str]
            The names of the phases. Defaults to ("ll_image", "ll_blank") corresponding
            to the image signifying the attention check and a blank screen.
        timing: str
            The "units" of the phase durations. Best to keep as 'milliseconds'. 
            Refer to LanguageLocalizerTrial for more info. 
        other parameters:
            refer to language_localizer_trial.LanguageLocalizerTrial
        """

        # Load phase settings from settings.yml
        phase_duration_attention = session.settings["language_localizer"]["stimuli"]["phase_duration_attention"]
        phase_duration_blank = session.settings["language_localizer"]["stimuli"]["phase_duration_blank"]
        phase_name_attention = session.settings["language_localizer"]["stimuli"]["phase_name_attention"]
        phase_name_blank = session.settings["language_localizer"]["stimuli"]["phase_name_blank"]
        timing = session.settings["language_localizer"]["stimuli"]["timing_attention_trial"]
        
        # Set phase durations and names
        phase_durations = (phase_duration_attention, phase_duration_blank)
        phase_names = (phase_name_attention, phase_name_blank)

        super().__init__(session=session,
                         trial_nr=trial_nr,
                         phase_durations=phase_durations,
                         phase_names=phase_names,
                         parameters=parameters,
                         timing=timing,
                         load_next_during_phase=load_next_during_phase,
                         verbose=verbose,
                         draw_each_frame=draw_each_frame)

        # Create the image stimulus
        self.img_stim = ImageStim(self.session.win,
                                  image=self.session.attention_check)

    def draw(self):
        """Draw the image."""
        if self.phase == 0:
            self.img_stim.draw()
        else:
            self.session.win.flip()


class LanguageLocalizerSentenceTrial(Trial):
    """"""

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 words: Collection[str],
                 condition: str,
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True):
        """Initialize the ImageTrial object.

        parameters
        ----------
        """

        # Load phase settings from settings.yml
        phase_duration_word = session.settings["language_localizer"]["stimuli"]["phase_duration_word"]
        phase_duration_blank = session.settings["language_localizer"]["stimuli"]["phase_duration_blank"]
        phase_name_word = session.settings["language_localizer"]["stimuli"]["phase_name_word"]
        phase_name_blank = session.settings["language_localizer"]["stimuli"]["phase_name_blank"]
        timing = session.settings["language_localizer"]["stimuli"]["timing_sentence_trial"]

        # Determine phase durations and names according to number of words
        phase_durations = [phase_duration_blank]+[phase_duration_word for i in range(len(words))]
        phase_names = [phase_name_blank]+[f"{phase_name_word}_{i}" for i in range(len(words))]

        # Set log parameters
        parameters = {
            "subject_nr": session.subj_nr,
            "run_nr": session.run_nr,
            "set_nr": session.set_nr,
            "trial_nr": trial_nr,
            "condition": condition
        }

        super().__init__(session=session,
                         trial_nr=trial_nr,
                         phase_durations=phase_durations,
                         phase_names=phase_names,
                         parameters=parameters,
                         timing=timing,
                         load_next_during_phase=load_next_during_phase,
                         verbose=verbose,
                         draw_each_frame=draw_each_frame)

        # Create the text stimuli
        text_color = self.session.settings["language_localizer"]["stimuli"]["text_color"]
        self.txt_stims = [
            TextStim(self.session.win, text=word, color=text_color) for word in words]

    def draw(self):
        if self.phase > 0:
            self.txt_stims[self.phase-1].draw()


class LanguageLocalizerFixationTrial(Trial):
    """Trial to display the fixation cross."""

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 parameters: dict = None,
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True):
        """Initialize the ImageTrial object.

        parameters
        ----------
        """

        # Load phase settings from settings.yml
        phase_duration_fix= session.settings["language_localizer"]["stimuli"]["phase_duration_fix"]
        phase_name_fix = session.settings["language_localizer"]["stimuli"]["phase_name_fix"]
        timing = session.settings["language_localizer"]["stimuli"]["timing_fixation_trial"]

        # Determine phase durations and names according to number of words
        phase_durations = (phase_duration_fix, )
        phase_names = (phase_name_fix, )

        super().__init__(session=session,
                         trial_nr=trial_nr,
                         phase_durations=phase_durations,
                         phase_names=phase_names,
                         parameters=parameters,
                         timing=timing,
                         load_next_during_phase=load_next_during_phase,
                         verbose=verbose,
                         draw_each_frame=draw_each_frame)

        self.fix_stim = TextStim(
            self.session.win, text="+", color=self.session.settings["language_localizer"]["stimuli"]["fix_color"])

    def draw(self):
        """Draw the image."""
        self.fix_stim.draw()
