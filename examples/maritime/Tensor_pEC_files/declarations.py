
from src.processEvents import InputEvent
from src.processSimpleFluents import SimpleFluent

declarations = {('velocity_GrHcNCMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_LtHcNCMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_GrMovMin_LtMin',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_GrMin_LtMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_GrMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_LtMovMin',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_GrTugMin_LeTugMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_GrTugMax',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('velocity_LtTugMin',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_fishing',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_nearCoast',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_nearCoast5k',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('entersArea_nearPorts',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_fishing',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_nearCoast',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_nearCoast5k',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('leavesArea_nearPorts',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('change_in_speed_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('change_in_speed_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('change_in_heading',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('stop_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('stop_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('slow_motion_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('slow_motion_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('gap_start',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('gap_end',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('gap', 'nearPorts'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('gap', 'farFromPorts'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('stopped', 'nearPorts'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('stopped', 'farFromPorts'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('lowSpeed', 'true'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'fishing', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'nearCoast', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'nearCoast5k', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('withinArea', 'nearPorts', 'true'):

                    {'type': SimpleFluent, 'index': ('vessel', 'areaType'), 'Ndim': 1, 'library': 'scipy'},

                ('changingSpeed', 'true'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('highSpeedNearCoast', 'true'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('movingSpeed', 'below'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('movingSpeed', 'normal'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('movingSpeed', 'above'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('tuggingSpeed', 'true'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},
                }
