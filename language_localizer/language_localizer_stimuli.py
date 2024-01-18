
import csv
import pkg_resources
from psychopy.visual import ImageStim

class LanguageLocalizerSentenceStimSet():
     """"""

     def __init__(self, complete_path: str = None) -> None:
         self.complete_path = complete_path

     def load(self, run_nr: int, set_nr: int) -> list:
        """Loads the sentences from a stimulus set.
        
        parameters
        ----------
        run_nr : int
            Run number to identify the correct stimulus set. 
        set_nr: int
            Set number to identify the correct stimulus set. 
        complete_path: str
            Instead of using one of the standard stimulus sets the complete path can be provided. 
        """
        if self.complete_path is None: 
            stim_set_path = pkg_resources.resource_filename(__name__, f"stimuli/langloc_fmri_run{run_nr}_stim_set{set_nr}.csv")
            using = f"Using stimulus set: langloc_fmri_run{run_nr}_stim_set{set_nr}.csv"
        else:
            stim_set_path = self.complete_path
            using = f"Using stimulus set: {self.complete_path}"
        print(using)

        # Load sentences from csv file
        sentences = []
        with open (stim_set_path, "r", newline="") as f:
            csv_reader = csv.reader(f, delimiter=",")
            next(csv_reader) # skip header
            for row in csv_reader:
                sentences += [row] 
        return sentences


class LanguageLocalizerAttentionCheckStim():
    """"""

    def __init__(self, complete_path: str = None) -> None:
        self.complete_path = complete_path

    def load(self):
        if self.complete_path is None: 
            img_path = pkg_resources.resource_filename(__name__, f"stimuli/hand-press-button-4.jpeg")
        else:
            img_path = self.complete_path
        return img_path
    