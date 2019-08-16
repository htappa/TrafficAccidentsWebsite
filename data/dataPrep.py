# this python script cleans the data and converts the "raw" csv file into 3 "clean"
# csv files: one for visualizations, and two that are needed for the sankey diagram
# (the sankey diagram requires linking two identical csv's in Tableau with UNION ALL operator)

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# import pandas and read in csv
import pandas as pd
data = pd.read_csv('traffic_accidents_raw.csv')

# drop unnecessary columns
data = data.drop(['INCIDENT_ID', 'OFFENSE_ID', 'OFFENSE_CODE', 'OFFENSE_CODE_EXTENSION',
                  'LAST_OCCURRENCE_DATE', 'REPORTED_DATE', 'INCIDENT_ADDRESS', 'GEO_X',
                  'GEO_Y', 'DISTRICT_ID', 'PRECINCT_ID', 'BICYCLE_IND', 'PEDESTRIAN_IND',
                  'INCIDENT_ID', 'OFFENSE_ID', 'OFFENSE_CODE', 'OFFENSE_CODE_EXTENSION',
                  'LAST_OCCURRENCE_DATE', 'REPORTED_DATE', 'INCIDENT_ADDRESS', 'GEO_X',
                  'GEO_Y', 'DISTRICT_ID', 'PRECINCT_ID', 'BICYCLE_IND', 'PEDESTRIAN_IND',
                  'HARMFUL_EVENT_SEQ_3', 'ROAD_CONTOUR', 'TU1_TRAVEL_DIRECTION',
                  'TU1_VEHICLE_MOVEMENT', 'TU2_TRAVEL_DIRECTION', 'TU2_VEHICLE_MOVEMENT',
                  'FATALITY_MODE_1', 'FATALITY_MODE_2', 'SERIOUSLY_INJURED_MODE_1',
                  'SERIOUSLY_INJURED_MODE_2'], axis=1)

# rename columns
data = data.rename(columns={'OBJECTID_1': 'OBJECT_ID', 'FIRST_OCCURRENCE_DATE': 'OCCURRENCE_DATE',
                            'HARMFUL_EVENT_SEQ_1': 'CRASH_SEQUENCE_1', 'HARMFUL_EVENT_SEQ_2':
                            'CRASH_SEQUENCE_2', 'TU1_VEHICLE_TYPE': 'VEHICLE_TYPE', 'TU1_DRIVER_ACTION':
                            'DRIVER_ACTION', 'TU1_DRIVER_HUMANCONTRIBFACTOR': 'CONTRIBUTING_FACTOR',
                            'TU1_PEDESTRIAN_ACTION': 'PEDESTRIAN_ACTION', 'TU2_VEHICLE_TYPE':
                            '2ND_VEHICLE_TYPE', 'TU2_DRIVER_ACTION': '2ND_DRIVER_ACTION',
                            'TU2_DRIVER_HUMANCONTRIBFACTOR': '2ND_DRIVER_CONTRIBUTING_FACTOR',
                            'TU2_PEDESTRIAN_ACTION': '2ND_PEDESTRIAN_ACTION'})

# filter for 2015-2018 data only
data = data[(data['OCCURRENCE_DATE'] >= '2015-01-01') &
            (data['OCCURRENCE_DATE'] <= '2018-12-31')]

# sort by occurrence date
data = data.sort_values(by=['OCCURRENCE_DATE'])

# remove rows with null values in Longitude and Latitude
data = data[data.GEO_LON.notnull()]
data = data[data.GEO_LAT.notnull()]

# convert dataframe into csv files
#data.to_csv('traffic_accidents_clean.csv', index=False)

data = data.drop(['OCCURRENCE_DATE', 'GEO_LON', 'GEO_LAT', 'NEIGHBORHOOD_ID', 'CRASH_SEQUENCE_1',
                  'CRASH_SEQUENCE_2', 'ROAD_LOCATION', 'ROAD_DESCRIPTION', 'ROAD_CONDITION',
                  'LIGHT_CONDITION', 'VEHICLE_TYPE', 'CONTRIBUTING_FACTOR', 'PEDESTRIAN_ACTION',
                  '2ND_VEHICLE_TYPE', '2ND_DRIVER_ACTION', '2ND_DRIVER_CONTRIBUTING_FACTOR',
                  '2ND_PEDESTRIAN_ACTION', 'SERIOUSLY_INJURED', 'FATALITIES'], axis=1)

data['TOP_TRAFFIC_ACCIDENT_OFFENSE'] = data['TOP_TRAFFIC_ACCIDENT_OFFENSE'].replace('TRAF - ACCIDENT               ', 'ACCIDENT')
data['TOP_TRAFFIC_ACCIDENT_OFFENSE'] = data['TOP_TRAFFIC_ACCIDENT_OFFENSE'].replace('TRAF - ACCIDENT - DUI/DUID    ', 'DUI/DUID')
data['TOP_TRAFFIC_ACCIDENT_OFFENSE'] = data['TOP_TRAFFIC_ACCIDENT_OFFENSE'].replace('TRAF - ACCIDENT - FATAL       ', 'FATAL')
data['TOP_TRAFFIC_ACCIDENT_OFFENSE'] = data['TOP_TRAFFIC_ACCIDENT_OFFENSE'].replace('TRAF - ACCIDENT - HIT & RUN   ', 'HIT & RUN')
data['TOP_TRAFFIC_ACCIDENT_OFFENSE'] = data['TOP_TRAFFIC_ACCIDENT_OFFENSE'].replace('TRAF - ACCIDENT - POLICE      ', 'POLICE')
data['TOP_TRAFFIC_ACCIDENT_OFFENSE'] = data['TOP_TRAFFIC_ACCIDENT_OFFENSE'].replace('TRAF - ACCIDENT - SBI         ', 'SBI')

data.to_csv('sankey/driver_action.csv', index=False)
data.to_csv('sankey/offense.csv', index=False)

print("csv files created")
