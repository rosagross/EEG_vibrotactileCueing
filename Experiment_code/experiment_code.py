# The experiment code file
# Here the belt is connected and uses the functions file that implements the individual blocks.
# Randomization of trials happens here.
# Reads in parameters from separate parameter file.

from pybelt import classicbelt
import serial #@UnusedImport # PySerial for USB connection
import serial.tools.list_ports
from pybelt import classicbelt
import time
#import parallel
import random
import datetime
from psychopy import visual, event, data, logging, core
import vibrotactile_functions
import visual_functions
import parameter

#event.globalKeys.add(key='escape', func=core.quit)
#p = parallel.Parallel()

class Experiment():

    def __init__(self):
        print('----------------')
        print('Start Experiment')
        print('----------------\n')

        # get the vibrotactile functions
        self.belt = vibrotactile_functions.VibrationController(parameter.ankle_vibromotor, parameter.wrist_vibromotor,
                                                     parameter.waist_vibromotor_left, parameter.waist_vibromotor_right,
                                                     parameter.trial_break)
        self.screen = visual_functions.ControlScreen(parameter.color_standard, parameter.color_oddball, parameter.trial_break)

        # get the parameter from external file
        self.trials_per_block = parameter.trials
        self.repeat_blocks = parameter.identical_blocks
        self.oddball_ratio = parameter.oddball_ratio
        self.color_standard = parameter.color_standard
        self.color_oddball = parameter.color_oddball

        print("\nThe experiment includes:")
        print("Trials per block: ", self.trials_per_block)
        print("Repeats identical blocks %i times.\n" % (self.repeat_blocks))

    def start(self):
        """Function that starts the experiment"""
        # initialize belt controller
        self.belt.connect_to_USB()

        print('+++++++++++++++++++++++++++++++++++')
        print('          -BELT CONNECTED-         ')
        print('+++++++++++++++++++++++++++++++++++\n')

        # show instructions on screen
        self.screen.show_instructions()

        # All blocks are running twice.
        # Block section 1 (all blocks run once, random order)
        block_functions = [self.screen.visual_oddball, self.belt.vibrotactile_oddball_waist,
                            self.belt.vibrotactile_oddball_wrist, self.belt.vibrotactile_oddball_ankle]
        count_fingertapping = 0
        # Execute all the blocks twice. Before executed a second time,
        # all other blocks should have been run at least once.
        for _ in range(self.repeat_blocks):

            # Shuffle blocks
            random.shuffle(block_functions)
            print('Start next block section!')


            # Start new block
            for i, function in enumerate(block_functions):
                time.sleep(1.0)
                self.screen.show_ready_screen()
                self.screen.show_fixation_cross()
                print('Execute block %i out of 4' % (i+1))
                function(self.trials_per_block, self.oddball_ratio)

                # Do fingertapping task every 4 blocks
                if (i+2)%2 == 0:
                    print('-----------------------------------')
                    print('-----------FINGER TAPPING----------')
                    print('-----------------------------------\n')
                    count_fingertapping += 1
                    self.screen.start_fingertapping_screen(count_fingertapping)

                print('')


        # At the very end of the experiment, disconnect the belt
        self.belt.disconnect_belt()

        # Say good bye and thank the participants
        self.screen.show_thank_you()


def main():
    """ Starts the test application. """
    try:
        experiment = Experiment()
        experiment.start()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()