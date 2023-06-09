import numpy as np
import pandas as pd

class ShockAnalysis():
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame
        self.leadNames = self.dataFrame.columns[1:20]
        self.artifactNames = self.dataFrame.columns[23:]
        self.normal_tone_starts = []
        self.oddball_no_click_starts = []
        self.oddball_starts = []
        self.oddball_clicks = []
        self.out_of_place_events = []
        
    def split(self):
        
        def label_start_positions(input_df):
            previous_event = None
            before_previous_event = None
            previous_event_index = None
            before_previous_event_index = None
            number_of_oddball_tones = 0
            for index, event in enumerate(input_df.Event.values):
                if event == 1:
                    normal_tone_starts.append(index)
                    if previous_event == 2:
                        if number_of_oddball_tones < 20:
                            out_of_place_events.append(previous_event_index)
                        else:
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
                    number_of_oddball_tones += 1
                elif event == 3:
                    if previous_event == 2:
                        oddball_clicks.append(index)
                        oddball_starts.append(previous_event_index)
                    if previous_event == 1:
                        out_of_place_events.append(previous_event_index)
                        out_of_place_events.append(index)
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
            return normal_tone_starts, oddball_no_click_starts, oddball_starts, oddball_clicks, out_of_place_events
        
        # Now run the label_start_positions funcition
        self.normal_tone_starts, self.oddball_no_click_starts, self.oddball_starts, self.oddball_clicks, self.out_of_place_events = label_start_positions(self.dataFrame)
        def build_dictionaries(self):
            self.normal_tones = {}
            self.oddball_no_shock = {}
            self.oddball_with_shock = {}
            end = len(self.dataFrame)
            def get_ranges(tone, end):
                previous_5_range = range(tone-5, tone)
                if tone <= 5:
                    previous_5_range = range(0, tone)

                tone_range = range(tone, tone+250)
                if tone+250 >= end:
                    tone_range = range(tone, end)
                return (previous_5_range, tone_range)

            
            for tone in normal_tone_starts:
                self.normal_tones[tone] = {}
                previous_5_range, tone_range = get_ranges(tone, end)
                for lead in lead_names:
                    self.normal_tones[tone][lead] = {}
                    previous_5_readings = self.dataFrame[lead].values[previous_5_range].tolist()
                    voltage_readings = self.dataFrame[lead].values[tone_range].tolist()
                    self.normal_tones[tone][lead]['previous_5_readings'] = previous_5_readings
                    self.normal_tones[tone][lead]['previous_5_art'] = self.dataFrame[lead+'_Artifact'].values[previous_5_range].tolist()
                    self.normal_tones[tone][lead]['voltage_readings'] = voltage_readings
                    self.normal_tones[tone][lead]['art'] = self.dataFrame[lead+'_Artifact'].values[tone_range].tolist()
                    avg_previous_5 = np.mean(previous_5_readings)
                    normalized_voltages = []
                    for voltage in voltage_readings:
                        normalized_voltages.append(voltage-avg_previous_5)
                    self.normal_tones[tone][lead]['normalized_voltages'] = normalized_voltages
                    
            for tone in oddball_no_click_starts:
                self.oddball_no_shock[tone] = {}
                previous_5_range, tone_range = get_ranges(tone, end)
                for lead in lead_names:
                    self.oddball_no_shock[tone][lead] = {}
                    previous_5_readings = self.dataFrame[lead].values[previous_5_range].tolist()
                    voltage_readings = self.dataFrame[lead].values[tone_range].tolist()
                    self.oddball_no_shock[tone][lead]['previous_5_readings'] = previous_5_readings
                    self.oddball_no_shock[tone][lead]['previous_5_art'] = self.dataFrame[lead+'_Artifact'].values[previous_5_range].tolist()
                    self.oddball_no_shock[tone][lead]['voltage_readings'] = voltage_readings
                    self.oddball_no_shock[tone][lead]['art'] = self.dataFrame[lead+'_Artifact'].values[tone_range].tolist()
                    avg_previous_5 = np.mean(previous_5_readings)
                    normalized_voltages = []
                    for voltage in voltage_readings:
                        normalized_voltages.append(voltage-avg_previous_5)
                    self.oddball_no_shock[tone][lead]['normalized_voltages'] = normalized_voltages
                    
            for tone, click in zip(oddball_starts, oddball_clicks):
                self.oddball_with_shock[tone] = {}
                self.oddball_with_shock[tone]['click'] = click
                previous_5_range, tone_range = get_ranges(tone, end)
                for lead in lead_names:
                    self.oddball_with_shock[tone][lead] = {}
                    previous_5_readings = self.dataFrame[lead].values[previous_5_range].tolist()
                    voltage_readings = self.dataFrame[lead].values[tone_range].tolist()
                    self.oddball_with_shock[tone][lead]['previous_5_readings'] = previous_5_readings
                    self.oddball_with_shock[tone][lead]['previous_5_art'] = self.dataFrame[lead+'_Artifact'].values[previous_5_range].tolist()
                    self.oddball_with_shock[tone][lead]['voltage_readings'] = voltage_readings
                    self.oddball_with_shock[tone][lead]['art'] = self.dataFrame[lead+'_Artifact'].values[tone_range].tolist()
                    avg_previous_5 = np.mean(previous_5_readings)
                    normalized_voltages = []
                    for voltage in voltage_readings:
                        normalized_voltages.append(voltage-avg_previous_5)
                    self.oddball_with_shock[tone][lead]['normalized_voltages'] = normalized_voltages
        
        build_dictionaries(self)