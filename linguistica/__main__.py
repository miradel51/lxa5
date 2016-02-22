#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import sys
import os

import linguistica as lxa
from linguistica.gui import main as gui_main

version = lxa.__version__

# ------------------------------------------------------------------------------
# ensure lxa_mode is one of the modes in MODES

MODES = {'cmd', 'gui'}

try:
    lxa_mode = sys.argv[1].lower()
except IndexError:
    lxa_mode = None
    error_msg_template = 'Error: mode not specified for running Linguistica.' \
                         '\n\nRun one of the following:\n\n{}'
    command_template = 'python3 -m linguistica {}'

    sys.exit(error_msg_template.format('\n'.join([command_template.format(mode)
                                                  for mode in sorted(MODES)])))

if lxa_mode not in MODES:
    sys.exit('Unrecognized mode: ' + sys.argv[1])

# ------------------------------------------------------------------------------
# GUI mode

if lxa_mode == 'gui':
    print('Running the graphical user interface of Linguistica {}...'
          .format(version))
    gui_main()

# ------------------------------------------------------------------------------
# command line mode

if lxa_mode == 'cmd':
    print('\nWelcome to Linguistica {}!'.format(version))

    # --------------------------------------------------------------------------
    # determine if file is a wordlist or a corpus text

    use_wordlist_response = None
    while use_wordlist_response is None:
        use_wordlist_response = input('\nAre you using a wordlist file? [N/y] ')

    if use_wordlist_response and use_wordlist_response[0].lower() == 'y':
        use_wordlist = True
    else:
        use_wordlist = False

    # --------------------------------------------------------------------------
    # get file path

    file_abspath = None
    while file_abspath is None:
        file_path = input('\nPath to your file: ')

        if sys.platform.startswith('win'):
            file_path = file_path.replace('/', os.sep)
        else:
            file_path = file_path.replace('\\', os.sep)

        file_abspath = os.path.abspath(file_path)

        if not os.path.isfile(file_abspath):
            print('Invalid file path!')
            file_abspath = None

    print('\nFull file path:\n{}'.format(file_abspath))

    # --------------------------------------------------------------------------
    # determine output directory

    output_dir = os.path.join(os.path.dirname(file_abspath), 'lxa_outputs')

    print('\nDefault output directory:\n{}'.format(output_dir))

    change_dir_response = None
    while change_dir_response is None:
        change_dir_response = input('Change it? [N/y] ')

    if change_dir_response and change_dir_response[0].lower() == 'y':
        new_output_dir = None
        while new_output_dir is None:
            new_output_dir = input('Specify output directory: ')

            if sys.platform.startswith('win'):
                new_output_dir = new_output_dir.replace('/', os.sep)
            else:
                new_output_dir = new_output_dir.replace('\\', os.sep)

            new_output_dir = os.path.abspath(new_output_dir)

            if not os.path.isdir(new_output_dir):
                try:
                    os.mkdir(new_output_dir)
                except FileNotFoundError:
                    print('Cannot make a new directory in a non-existing one!')
                    new_output_dir = None

        output_dir = new_output_dir

    # --------------------------------------------------------------------------
    # create the Linguistica object

    if use_wordlist:
        lxa_object = lxa.read_wordlist(file_abspath)
    else:
        lxa_object = lxa.read_corpus(file_abspath)

    # --------------------------------------------------------------------------
    # change parameters, if instructed

    # TODO

    # --------------------------------------------------------------------------
    # run all Linguistica modules on the given file

    print('\nRunning all Linguistica modules on the given file:')

    lxa_object.run_all_modules(verbose=True)

    print('\nDone!')

    # --------------------------------------------------------------------------
    # output results as files

    # TODO
