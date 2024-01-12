# Contains all subclasses of Trial used in the language localizer.

from exptools2.core import Session, Trial
from psychopy.visual import ImageStim, TextStim
from typing import Collection


class LanguageLocalizerTrial(Trial):

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 phase_durations: Collection[int],
                 phase_names: Collection[str] = None,
                 parameters: dict = None,
                 timing: str = 'milliseconds',
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True):
        """Initialize the ImageTrial object.

        parameters
        ----------
        session : LanguageLocalizerSession object
            A Session object (needed for metadata)
        timing : str
            The "units" of the phase durations. Default is 'milliseconds' 
            which is not supported by exptools2 but was used in the original 
            language localizer in matlab. Milliseconds are then converted to 
            frames as this yields more accurate timing than using exptools2's 
            seconds. Alternatively 'seconds' or 'frames' may be used according to 
            exptools2's documentation.
        other parameters:
            refer to exptools2.core.Trial


        """
        # Convert phase_durations to frames according to actual framerate
        if timing == "milliseconds":
            actual_framerate = session.actual_framerate
            phase_durations = [int(duration/1000 * actual_framerate)
                               for duration in phase_durations]
            timing = "frames"  # set timing to frames for super().__init__

        super().__init__(session=session,
                         trial_nr=trial_nr,
                         phase_durations=phase_durations,
                         phase_names=phase_names,
                         parameters=parameters,
                         timing=timing,
                         load_next_during_phase=load_next_during_phase,
                         verbose=verbose,
                         draw_each_frame=draw_each_frame)


class LLHandPressTrial(LanguageLocalizerTrial):
    """Trial to display the hand press icon as attention check."""

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 phase_durations: Collection[int] = (400, 100),
                 phase_names: Collection[str] = ("ll_image", "ll_blank"),
                 parameters: dict = None,
                 timing: str = 'milliseconds',
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True,
                 img_path: str = "stimuli/hand-press-button-4.jpeg"):
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
        img_path : str
            Path to the image to be displayed. Defaults to the hand press icon.
        other parameters:
            refer to language_localizer_trial.LanguageLocalizerTrial
        """

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
                                  image=img_path)

    def draw(self):
        """Draw the image."""
        if self.phase == 0:
            self.img_stim.draw()
        else:
            self.session.win.flip()


class LLSentenceTrial(LanguageLocalizerTrial):
    """"""

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 words: Collection[str],
                 condition: str,
                 phase_duration_blank: int = 100,
                 phase_duration_word: int = 450,
                 phase_name_blank: str = "ll_blank",
                 phase_name_word: str = "ll_word",
                 timing: str = 'milliseconds',
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True):
        """Initialize the ImageTrial object.

        parameters
        ----------
        """
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
        text_color = self.session.settings["stimuli"]["text_color"]
        self.txt_stims = [
            TextStim(self.session.win, text=word, color=text_color) for word in words]

    def draw(self):
        if self.phase > 0:
            self.txt_stims[self.phase-1].draw()


class LLFixationTrial(LanguageLocalizerTrial):
    """Trial to display the fixation cross."""

    def __init__(self,
                 session: Session,
                 trial_nr: int,
                 phase_durations: Collection[int] = (1400,),
                 phase_names: Collection[str] = ("ll_fix",),
                 parameters: dict = None,
                 timing: str = 'milliseconds',
                 load_next_during_phase: int = None,
                 verbose: bool = True,
                 draw_each_frame: bool = True):
        """Initialize the ImageTrial object.

        parameters
        ----------
        """
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
            self.session.win, text="+", color=self.session.settings["stimuli"]["fix_color"])

    def draw(self):
        """Draw the image."""
        self.fix_stim.draw()
