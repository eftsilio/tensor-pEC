
from src.processEvents import InputEvent
from src.processSimpleFluents import SimpleFluent

declarations = {('appear',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('disappear',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('active',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('inactive',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('walking',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('running',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('abrupt',):

                    {'type': InputEvent, 'index': (3,), 'args': (), 'Ndim': 1, 'library': 'scipy'},

                ('close_leaveDist', 'true'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_fightDist', 'true'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_fightDist', 'false'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_meetDist', 'true'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_meetDist', 'false'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_moveDist', 'true'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_moveDist', 'false'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('close_interactDist', 'true'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('orientation', 'true'):

                    {'type': InputEvent, 'index': (4, 5), 'Ndim': 2, 'library': 'scipy'},

                ('person', 'true'):

                    {'type': SimpleFluent, 'Ndim': 1, 'library': 'scipy'},

                ('fighting', 'true'):

                    {'type': SimpleFluent, 'Ndim': 2, 'library': 'sparse'},

                ('meeting', 'true'):

                    {'type': SimpleFluent, 'Ndim': 2, 'library': 'sparse'},

                ('moving', 'true'):

                    {'type': SimpleFluent, 'Ndim': 2, 'library': 'sparse'},

                ('leaving_object', 'true'):

                    {'type': SimpleFluent, 'Ndim': 2, 'library': 'sparse'},

                }
