# %% Import
import json
import pandas as pd
import plotly.express as plx
import numpy as np

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])


    def find_peaks(self):
        ekg_peaks_indices = []
        ekg_peaks = []
        threshold = 0.9
        ekg_max_value = self.df['Messwerte in mV'].max()

        for i in range(1, len(self.df) -1, 1):
            if (self.df['Messwerte in mV'][i] > self.df['Messwerte in mV'][i - 1] and
                self.df['Messwerte in mV'][i] > self.df['Messwerte in mV'][i + 1] and
                self.df['Messwerte in mV'][i] > threshold * ekg_max_value):
                ekg_peaks_indices.append(i)
                ekg_peaks.append(self.df['Messwerte in mV'][i])

        self.ekg_peaks_indices = ekg_peaks_indices
        self.ekg_peaks = ekg_peaks
        self.df_peaks = pd.DataFrame({
            "Index": self.ekg_peaks_indices,
            "Peakwert": self.ekg_peaks
        })

    def estimate_hr(self):
        peak_intervals = []

        for i in range(0, len(self.ekg_peaks_indices) -1, 1):
            # Berechne die Zeitdifferenz zwischen den Peaks
            interval = self.ekg_peaks_indices[i + 1] - self.ekg_peaks_indices[i]
            peak_intervals.append(interval)

        # Berechne die durchschnittliche Zeit zwischen den Peaks
        avg_peak_interval = sum(peak_intervals) / len(peak_intervals)
        # Berechne die Herzrate in Schlägen pro Minute
        
        hr = 60000 / avg_peak_interval
            
        self.hr = hr

    def plot_time_series(self):
        # Nur die ersten 2000 Datenpunkte verwenden
        df_subset = self.df.head(2000)

        # Linienplot aus df_subset
        self.fig = plx.line(df_subset, x="Zeit in ms", y="Messwerte in mV")
        plx.defaults.width = 600
        plx.defaults.height = 400

        # Gültige Peak-Indizes innerhalb der 2000 Datenpunkte
        valid_indices = []
        for i in self.ekg_peaks_indices:
            if i < 2000:
                valid_indices.append(i)
        print(valid_indices)

        # Peak-Zeiten & Werte direkt aus df_subset
        peak_times_ms = df_subset.iloc[valid_indices]["Zeit in ms"].values
        peak_values = df_subset.iloc[valid_indices]["Messwerte in mV"].values
        peak_times_min = peak_times_ms / 60000

        # Peaks einzeichnen
        self.fig.add_scatter(
            x=peak_times_min,
            y=peak_values,
            mode='markers',
            marker=dict(color='red', size=10),
            name='Peaks'
        )

        self.fig.show()
        self.fig



if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    ekg.find_peaks()
    ekg.estimate_hr()
    print(ekg.hr)
    ekg.plot_time_series()
    print(ekg.df_peaks)
# %%
