# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 08:32:49 2024

@author: TCartwright
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
os.chdir(r"C:\Users\tcartwright\Documents\Data Science Notes\Python")
from tcc_formulas import data_view
from BIH import yield_2023
from scipy import stats


#Data for the Climate in Kinston
os.chdir(r"C:\Users\tcartwright\Documents")
kin_clim = pd.read_csv("Kinston Temperatures.csv")
data_view(kin_clim)
kin_clim["Date"] = pd.to_datetime(kin_clim["Date"])
kin_clim.set_index("Date", inplace = True)
kin_clim["Temp Avg"].dtype
kin_clim.head()
#Graph for temperature
temp_only = kin_clim.plot(y = "Temp Avg", kind = 'line', color = 'orange') ; plt.title('Average Temperature from Aug 2023 to Apr 2024')
slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(kin_clim)), kin_clim["Temp Avg"])
temp_trend = slope * np.arange(len(kin_clim)) + intercept
plt.plot(kin_clim.index, temp_trend, color='orange', linestyle='--', label='Temp Avg Trend')
#Graph for humidity
hum_only = kin_clim.plot(y = "Hum Avg", kind = 'line', color = 'red') ; plt.title('Average Humidity from Aug 2023 to Apr 2024')
slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(kin_clim)), kin_clim["Hum Avg"])
hum_trend = slope * np.arange(len(kin_clim)) + intercept
plt.plot(kin_clim.index, hum_trend, color='red', linestyle='--', label='Hum Avg Trend')
#Both together
kin_clim_plot = kin_clim.plot(y = ["Temp Avg", "Hum Avg"], kind = 'line', color = ['orange', 'red']) ; plt.title('Average Temperature and Humidity from Aug 2023 to Apr 2024')
slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(kin_clim)), kin_clim["Hum Avg"])
hum_trend = slope * np.arange(len(kin_clim)) + intercept
plt.plot(kin_clim.index, hum_trend, color='red', linestyle='--', label='Hum Avg Trend')
slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(kin_clim)), kin_clim["Temp Avg"])
temp_trend = slope * np.arange(len(kin_clim)) + intercept
plt.plot(kin_clim.index, temp_trend, color='orange', linestyle='--', label='Temp Avg Trend')
plt.show()
#Gather the dates and convert to weekly dates ending on Sunday
weekly_kin_clim_avg = kin_clim.resample("W-SUN").mean()
print(weekly_kin_clim_avg)

#Imported dataframe from BIH.py
yield_2023.head()
yield_2023["Date"] = pd.to_datetime((yield_2023["Date"]))
dummy_table = kin_clim.merge(yield_2023, on = "Date")
dummy_table.head()
print(yield_2023)
start_date = '2023-08-20'
end_date = '2024-04-28'
kin_clim_slice = weekly_kin_clim_avg.loc[start_date:end_date]
yield_2023 = yield_2023.drop(1)
print(yield_2023.columns)
yield_2023_2 = yield_2023.copy()
print(yield_2023_2)
yield_2023['Yield'] = yield_2023["Yield"].str.replace('%', '') ; pd.to_numeric(yield_2023["Yield"], errors= 'coerce')
print(yield_2023.columns)
yield_slice = yield_2023[["Date", "Yield"]]
print(yield_slice)
temp_and_hum_slice = kin_clim_slice[["Temp Avg", "Hum Avg"]]
print(temp_and_hum_slice)
temp_and_hum_slice_reset = temp_and_hum_slice.reset_index(drop = True)
yield_slice_reset = yield_slice.reset_index(drop = True)
temp_hum_yield = pd.concat([temp_and_hum_slice_reset, yield_slice_reset], axis = 1) ; temp_hum_yield.set_index("Date", inplace = True)
temp_hum_yield_2 = temp_hum_yield.copy()
temp_hum_yield_2.sort_values(by = "Yield", ascending = True)
temp_hum_yield_2["Yield"] = pd.to_numeric(temp_hum_yield_2["Yield"], errors='coerce')
print(temp_hum_yield_2)
temp_hum_yield_2["Yield"] = temp_hum_yield_2["Yield"].astype(int)
print(temp_hum_yield_2)
print(temp_hum_yield.head())

#Create scatterplot for temperature, humidity, and yield
temp_yield_plot = plt.scatter(temp_hum_yield_2.index, temp_hum_yield_2["Yield"], label = 'Yield (%)', color = 'black')
plt.scatter(temp_hum_yield_2.index, temp_hum_yield_2["Temp Avg"], label = "Temperature (F)", color = 'orange')
plt.scatter(temp_hum_yield.index, temp_hum_yield["Hum Avg"], color = 'red')
plt.legend(["Yield (%)", "Temp Avg (F)", "Hum Avg (%)"])
slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(temp_hum_yield)), temp_hum_yield["Hum Avg"])
trendline_y = slope * np.arange(len(temp_hum_yield)) + intercept
plt.plot(temp_hum_yield.index, trendline_y, color='red', linestyle='--', label='Hum Avg Trend')
plt.xticks(rotation = 30)
plt.tight_layout()
plt.title("Kinston Humidity, Temperature and Yield")
plt.show()

#Correlation for temps and hum over yield
correlation_matrix = temp_hum_yield.corr()
temp_yield = correlation_matrix.loc["Temp Avg", "Yield"]
print(temp_yield)
hum_yield = correlation_matrix.loc["Hum Avg", "Yield"]
print(hum_yield)


#Individual graph for yield
yield_plot = plt.plot(temp_hum_yield_2.index, temp_hum_yield_2["Yield"], color = 'black')
slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(len(temp_hum_yield_2)), temp_hum_yield_2["Yield"])
yield_trend = slope * np.arange(len(temp_hum_yield_2)) + intercept
plt.plot(temp_hum_yield_2.index, yield_trend, color='black', linestyle='--', label='Yield Avg Trend')
plt.xticks(rotation = 45)
plt.title("Yield from Aug 2023 to Apr 2024")
plt.show()
