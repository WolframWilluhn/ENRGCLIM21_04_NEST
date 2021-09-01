import pandas as pd
import matplotlib.pyplot as plt

PATH_TO_INPUT = "../SolAce/solace_data.csv"
PATH_TO_OUTPUT = "../SolAce/solace_data_engineered.csv"

# read data
df = pd.read_csv( PATH_TO_OUTPUT)
df.set_index( "time", inplace=True)
df.index = pd.to_datetime( df.index)

# prepare data
df[ "Y1_meeting"] = df.Y1_meeting / 100.0
df[ "Y1_office"] = df.Y1_office / 100.0

df = df.resample("h").mean() # "d" "h" "15T"

# plot data
subplot_rows = 4

plt.subplot(subplot_rows, 1, 1)

plt.plot( df.index, df.temp_amb, color='red', label="Ambient temperature")
plt.plot( df.index, df.temp_room, color='blue', label="Room temperature")
#plt.plot( df.index, df.setp_room, color='green', label="Temperature set point")
plt.plot( df.index, df.temp_diff, color='yellow', label="Temperature difference")

plt.title( 'Temperatures')
plt.xlabel( 'Time')
plt.ylabel( 'Temperatur')
plt.legend(loc="best")

plt.subplot(subplot_rows, 1, 2)

plt.plot( df.index, df.heating_power, color='red', label="Heating power")
#plt.plot( df.index, df.cooling_power, color='blue', label="Cooling power")
#plt.plot( df.index, df.net_power, color='yellow', label="Net power")

plt.plot( df.index, df.Y1_meeting, color='orange', label="Valve living")
plt.plot( df.index, df.Y1_office, color='gray', label="Valve office")

plt.legend(loc="best")

plt.subplot(subplot_rows, 1, 3)

plt.scatter( df.temp_amb, df.heating_power, s=1)

#plt.legend(loc="best")

plt.subplot(subplot_rows, 1, 4)

plt.scatter( df.temp_diff, df.heating_power, s=1)

#plt.legend(loc="best")

plt.show()
