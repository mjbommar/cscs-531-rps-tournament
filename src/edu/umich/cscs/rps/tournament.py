'''
@date 20131005
@author: mjbommar
'''

# Load standard packages
import os
import sys

# Load our agents module
import edu.umich.cscs.rps.agents


def load_entrants(path):
    '''
    Load all tournament entrants from a given path.
    '''

    # Initialize player list
    player_list = []

    # Add path to the system path
    sys.path.append(path)

    # Load all the files in path
    for file_name in os.listdir(path):
        # Skip non-py files
        if not file_name.lower().endswith('.py'):
            continue

        # Get module name
        module_name = os.path.basename(file_name).replace(".py", "")

        # Import the module
        __import__(module_name, globals(), locals(), ['*'])

        # Now iterate over module contents.
        for object_name in dir(sys.modules[module_name]):
            object_value = getattr(sys.modules[module_name], object_name)
            try:
                # Instantiate.
                object_instance = object_value()

                # If the variable matches the Player class type, include.
                if isinstance(object_instance,
                              edu.umich.cscs.rps.agents.Player):
                    player_list.append(object_instance)
            except Exception, E:
                pass

    # Return the player list
    return player_list

