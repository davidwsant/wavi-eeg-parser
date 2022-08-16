### Welcome to wavi_eeg_parser.py.

This program has been designed to parse the output files generated by a WAVI EEG
system into csv format. Starting from the directory designated by
the -i option, wavi_eeg_parser.py will search for subdirectories containing files
ending in '.eeg', '.art', and '.mag' and combine the information into a single
csv file containing information from all of the separate files. This program was
written to simplify the process of analyzing EEG data for labs at Noorda College
of Osteopathic Medicine and may require some optimization for your lab.

Example usage: `./wavi_eeg_parser.py -i ..`

optional arguments:
  -h, --help            

          show this help message and exit

  -i INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY

          This is the directory where wavi_eeg_parser.py will begin looking for subdirectories
          containing files ending in '.eeg', '.art', and '.mag'. By default, wavi_eeg_parser.py
          will begin with your current working directory.