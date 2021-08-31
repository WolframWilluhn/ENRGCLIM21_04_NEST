import pandas as pd
import matplotlib.pyplot as plt

PATH_TO_INPUT = "../SolAce/solace_data.csv"
PATH_TO_OUTPUT = "../SolAce/solace_data_engineered.csv"

# read data
df = pd.read_csv( PATH_TO_INPUT)
df.set_index( "time", inplace=True)
df.index = pd.to_datetime( df.index)

# prepare data

def is_weekend( day_of_week):
    if day_of_week < 5:
        return 0 #'r'
    else:
        return 1 #'g'

def dayofweek_filter( dayofweek):
    return dayofweek >= 5

def rad_room( irrad, blinds_height_F1, blinds_height_F2, blinds_height_F3, blinds_height_F4, hour):
	if hour < 11 or hour > 17:
		return 0
	else:
		return irrad * (blinds_height_F1 + blinds_height_F2 + blinds_height_F3 + blinds_height_F4) / 400.0

def praes_room( praes_meeting, praes_office):
	if praes_meeting == 1 or praes_office == 1:
		return 1
	else:
		return 0

df[ "day_of_week"] = df.index.dayofweek
df[ "is_weekend"] = df[ "day_of_week"].apply( is_weekend)
df[ "hour"] = df.index.hour

df[ "temp_room"] = (df.temp_meeting + df.temp_office) / 2.0
df[ "setp_room"] = (df.setp_meeting + df.setp_office) / 2.0
df[ "temp_diff"] = df.temp_amb - df.temp_room

df[ "rad_room"] = df.apply( lambda x: rad_room( x["irrad"], x["blinds_height_F1"], x["blinds_height_F2"], x["blinds_height_F3"], x["blinds_height_F4"], x["hour"]), axis = 1)
df[ "praes_room"] = df.apply( lambda x: praes_room( x["praes_meeting"], x["praes_office"]), axis = 1)

df[ "net_power"] = df.heating_power - df.cooling_power

df = df.round({'temp_room': 2, 'setp_room': 2, 'temp_diff': 2})

df.to_csv( PATH_TO_OUTPUT)

df = df.resample("h").mean() # "h" "15T"

# plot data
subplot_rows = 4

plt.subplot(subplot_rows, 1, 1)

plt.plot( df.index, df.temp_amb, color='red')
plt.plot( df.index, df.temp_room, color='blue')
#plt.plot( df.index, df.setp_room, color='green')
plt.plot( df.index, df.temp_diff, color='yellow')

plt.title( 'Temperatures')
plt.xlabel( 'Time')
plt.ylabel( 'Temperatur')

plt.subplot(subplot_rows, 1, 2)

plt.plot( df.index, df.heating_power, color='red')
plt.plot( df.index, df.cooling_power, color='blue')
#plt.plot( df.index, df.net_power, color='yellow')

plt.subplot(subplot_rows, 1, 3)

plt.scatter( df.temp_amb, df.heating_power, s=1)

plt.subplot(subplot_rows, 1, 4)

plt.scatter( df.temp_diff, df.heating_power, s=1)


plt.show()
