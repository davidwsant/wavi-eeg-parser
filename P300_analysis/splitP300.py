import numpy as np
import pandas as pd

class SplitP300():
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame # this will require that it be a df from a csv file created by Dave's wavi-parser
        self.lead_names = self.dataFrame.columns[1:20]
        self.artifact_names = self.dataFrame.columns[23:]
        self.normal_tone_starts = []
        self.normal_tone_accidental_click_starts = []
        self.normal_tone_clicks = []
        self.oddball_no_click_starts = []
        self.oddball_starts = []
        self.oddball_clicks = []
        
    def split(self):
        
        def label_start_positions(input_df):
            previous_event = None
            before_previous_event = None
            previous_event_index = None
            before_previous_event_index = None
            normal_tone_starts = []
            normal_tone_accidental_click_starts = []
            normal_tone_clicks = []
            oddball_no_click_starts = []
            oddball_starts = []
            oddball_clicks = []

            for index, event in enumerate(input_df.Event.values):
                if event == 1:
                    normal_tone_starts.append(index)
                    if previous_event == 2:
                        oddball_no_click_starts.append(previous_event_index)
                    before_previous_event = previous_event
                    previous_event = 1
                    before_previous_event_index = previous_event_index
                    previous_event_index = index
                elif event == 2:
                    before_previous_event = previous_event
                    previous_event = 2
                    before_previous_event_index = previous_event_index
                    previous_event_index = index
                elif event == 3:
                    if previous_event == 2:
                        oddball_clicks.append(index)
                        oddball_starts.append(previous_event_index)
                    if previous_event == 1:
                        normal_tone_accidental_click_starts.append(previous_event_index)
                        normal_tone_clicks.append(index)
                        if previous_event_index in normal_tone_starts:
                            normal_tone_starts.remove(previous_event_index)
                    before_previous_event = previous_event
                    previous_event = 3
                    before_previous_event_index = previous_event_index
                    previous_event_index = index

            if len(oddball_starts) != len(oddball_clicks):
                print()
                print("Somehow the number of oddball starts and the number of oddball clicks is not the same.")
                print("You probably want to look at the output and self.oddball_starts, self.oddball_clicks before moving on.")
                print()
            return normal_tone_starts, normal_tone_accidental_click_starts, normal_tone_clicks, oddball_no_click_starts, oddball_starts, oddball_clicks
        
        # Now run the label_start_positions funcition
        self.normal_tone_starts, self.normal_tone_accidental_click_starts, self.normal_tone_clicks, self.oddball_no_click_starts, self.oddball_starts, self.oddball_clicks = label_start_positions(self.dataFrame)
        def build_dictionaries(self):
            self.normal_tones = {}
            self.normal_tone_plus_click = {}
            self.oddball = {}
            self.oddball_no_click = {}
            end = len(self.dataFrame)
            def get_ranges(tone, end):
                previous_5_range = range(tone-5, tone)
                if tone <= 5:
                    previous_5_range = range(0, tone)

                tone_range = range(tone, tone+250)
                if tone+250 >= end:
                    tone_range = range(tone, end)
                return (previous_5_range, tone_range)

            
            def process_no_clicks(output_dictionary, input_list):
                for tone in input_list:
                    output_dictionary[tone] = {}
                    previous_5_range, tone_range = get_ranges(tone, end)
                    for lead in self.lead_names:
                        output_dictionary[tone][lead] = {}
                        previous_5_readings = self.dataFrame[lead].values[previous_5_range].tolist()
                        previous_5_art = self.dataFrame[lead+'_Artifact'].values[previous_5_range].tolist()
                        voltage_readings = self.dataFrame[lead].values[tone_range].tolist()
                        voltage_art = self.dataFrame[lead+'_Artifact'].values[tone_range].tolist()
                        output_dictionary[tone][lead]['previous_5_readings'] = previous_5_readings
                        output_dictionary[tone][lead]['previous_5_art'] = previous_5_art
                        output_dictionary[tone][lead]['voltage_readings'] = voltage_readings
                        output_dictionary[tone][lead]['art'] = voltage_art
                        avg_previous_5 = np.mean(previous_5_readings)
                        normalized_voltages = []
                        for voltage in voltage_readings:
                            normalized_voltages.append(voltage-avg_previous_5)
                        output_dictionary[tone][lead]['normalized_voltages'] = normalized_voltages
            
            process_no_clicks(self.normal_tones, self.normal_tone_starts)
            process_no_clicks(self.oddball_no_click, self.oddball_no_click_starts)
            
            def process_with_clicks(output_dictionary, input_list, input_click_list):
                for tone, click in zip(input_list, input_click_list):
                    output_dictionary[tone] = {}
                    output_dictionary[tone]['click_raw'] = click
                    output_dictionary[tone]['click'] = click - tone
                    previous_5_range, tone_range = get_ranges(tone, end)
                    for lead in self.lead_names:
                        output_dictionary[tone][lead] = {}
                        previous_5_readings = self.dataFrame[lead].values[previous_5_range].tolist()
                        previous_5_art = self.dataFrame[lead+'_Artifact'].values[previous_5_range].tolist()
                        voltage_readings = self.dataFrame[lead].values[tone_range].tolist()
                        voltage_art = self.dataFrame[lead+'_Artifact'].values[tone_range].tolist()
                        output_dictionary[tone][lead]['previous_5_readings'] = previous_5_readings
                        output_dictionary[tone][lead]['previous_5_art'] = previous_5_art
                        output_dictionary[tone][lead]['voltage_readings'] = voltage_readings
                        output_dictionary[tone][lead]['art'] = voltage_art
                        avg_previous_5 = np.mean(previous_5_readings)
                        normalized_voltages = []
                        for voltage in voltage_readings:
                            normalized_voltages.append(voltage-avg_previous_5)
                        output_dictionary[tone][lead]['normalized_voltages'] = normalized_voltages
                        
            process_with_clicks(self.normal_tone_plus_click, self.normal_tone_accidental_click_starts, self.normal_tone_clicks)
            process_with_clicks(self.oddball, self.oddball_starts, self.oddball_clicks)
        
        build_dictionaries(self)