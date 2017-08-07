#Kaden Plewe
#08/26/2016

#-----------------------------------------------------------------------------
#This script will be used to model the water consumption attributed to the
#power generation fuel mix within a specific location over a specified time
#frame.
#User Inputs
#----Location: The location for which the numbers will correlate to (city, state, etc.)
#Outputs
#----TBD
#-----------------------------------------------------------------------------
import Find_EmissionRates as ER
import urllib.request, urllib.parse, urllib.error
import json, csv, xlsxwriter
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display, HTML

#-----------------------------------------------------------------------------
#Power generation fuel types being included in this model are listed below

# coal: 	thermal power from coal
# natgas: 	thermal power from natural gas
# nuclear: 	thermal power from nuclear
# biogas: 	renewable energy from biogas or landfill gas
# wind: 	renewable energy from wind
# geo:		renewable energy from geothermal
# solarth:	renewable energy from solar (solar thermal)
# solarpv:	renewable energy from solar (solar photovoltaic)
# smhydro:	renewable energy from hydroelectric (small)
# biomass:	renewable energy from burning wood or other biomass

#Dictionary being used to store all retrieved data
#gen_d = {'coal': [1, 2], 'natgas': [2, 4], 'nuclear': [3, 6], 'biogas': [4, 8], 'wind': [5, 10],\
#'geo': [6, 12], 'solarth': [7, 14], 'solarpv': [8, 16], 'smhydro': [9, 18], 'biomass': [10, 20]}
gen_d = {'coal': [], 'natgas': [], 'nuclear': [], 'biogas': [], 'wind': [],\
'geo': [], 'solarth': [], 'solarpv': [], 'smhydro': [], 'biomass': []}
dat_time = []
dat_cnt = 0

#Conversion factors for water consumption, water withdrawal and emissions ([withdrawal, consumption, CO2, NOx, SO2])
convert = {'coal': [1005, 687, 0, 0, 0], 'natgas': [225, 205, 0, 0, 0], 'nuclear': [1101, 672, 0, 0, 0],\
                'biogas': [878, 235, 0, 0, 0], 'wind': [0, 0, 0, 0, 0], 'geo': [15, 15, 0, 0, 0], 'solarth': [786, 786, 0, 0, 0],\
                'solarpv': [0, 0, 0, 0, 0], 'smhydro': [0, 4491, 0, 0, 0], 'biomass': [878, 235, 0, 0, 0]}

#Declare regular expression sequences to be used in this script
time_rx = re.compile('[^-:TZ][0-9]*')

#-----------------------------------------------------------------------------
#Find the longitude and latitude of an input city using google's geocoding API

gmap_url = 'http://maps.googleapis.com/maps/api/geocode/json?'

while True:
	#Request location
    address = input('Enter Location: ')
    if len(address) < 1: break

	#Concatenate url
    geo_param = {'sensor':'false', 'address': address}
    geo_url = gmap_url + urllib.parse.urlencode(geo_param)
    print(("retrieving ", geo_url))
    print("")
    geo = urllib.request.urlopen(geo_url)
    geo_data = geo.read().decode('utf-8')
    print(geo_data)
    print("Retrieved", len(geo_data), "characters from google geocoding API")
    print("")

	#Load json output
    try: geo_js = json.loads(geo_data)
    except:
        geo_js = None
        print("==== Failure To Retrieve LAT & LON ====")
        continue

	#Convert to json format
	#print(json.dumps(geo_js, indent=4))

	#Extract latitude, longitude, and complete adress
    lat = geo_js["results"][0]["geometry"]["location"]["lat"]
    lng = geo_js["results"][0]["geometry"]["location"]["lng"]
    print("lat", lat, "lng", lng)
    location = geo_js['results'][0]['formatted_address']
    print(location)
    print("")

	#verify location
	#geo_check = input('Is this the correct location?')
	#if geo_check == 'no': break

#-----------------------------------------------------------------------------
#Use the latitude and longitude to find the balancing authority

	#url for balancing authority
    ba_url = 'https://api.watttime.org/api/v1/balancing_authorities/?'

	#loc query parameter concatenation
    ba_loc = 'loc={"type":"Point","coordinates":[%g,%g]}' %(lng, lat)
    ba_url += str(ba_loc)

	#Send request to WattTime API
    print(("retrieving ", ba_url))
    ba_open = urllib.request.urlopen(ba_url)
    ba_data = ba_open.read().decode('utf-8')
    print("retrieved ", len(ba_data), " characters from WattTime balancing authorities")
    print("")

	#Load json info
    try: ba_js = json.loads(ba_data)
    except:
        ba_js = None
        print("==== Failure To Retrieve Balancing Authority ====")
        continue

	#Convert to json format
	#print(json.dumps(ba_js, indent=4))

	#Extract all of the attributes that will be used in the data query
    ba_count = len(ba_js)
    ba_name = []																			#name attribute - full name of balancing authority
    ba_urls = []																			#url attribute - location on WattTime balancing authority page
    ba_abbrev = []																			#abbrev attribute - abbreviation for balancing authority

    for i in range(0, ba_count):
        ba_name.append(str(ba_js[i]["name"]))
        ba_urls.append(str(ba_js[i]["url"]))
        ba_abbrev.append(str(ba_js[i]["abbrev"]))

    print(ba_count, "balancing authority/s found for this location")
    print("Name/s: ", ba_name)
    print("Url/s: ", ba_urls)
    print("Abbreviation/s: ", ba_abbrev)
    print("")

	#Validate for data retrieval
	#ba_check = input('Would you like to retrieve fuel mix data for these balancing authorities?')
	#if ba_check == 'no': break

#-----------------------------------------------------------------------------
#Use balancing authority lists to retrieve fuel mix data for input location

	#Input WattTime API username and p-word to obtain access key
    #print("Please provide a username and password for a valid WattTime account.")
    #u_name = input('Username: ')
    #p_word = input('Password: ')
    u_name = 'kaden.plewe'
    p_word = 'WasatchMnt66^'

	#Select start and end time for data interval
    #print("Please indicate the start and end time for the data collection interval")
    #start_time = input('Start Time (ex. 2016-8-25T00:00:00): ')
    #end_time = input('End Time (ex. 2016-8-25T23:59:00): ')
    #print("")
    start_time = '2016-8-19T00:00:00'
    end_time = '2016-8-26T23:59:00'

	#Url for token retrieval
    auth_url = 'https://api.watttime.org/api/v1/obtain-token-auth/?'

	#Authentification parameter concatenation
    auth_info = urllib.parse.urlencode({'username': u_name, 'password': p_word})

	#Retrieve and format token text to be used a header
    req_token = urllib.request.urlopen(auth_url, auth_info.encode('utf-8'))
    
    #try: req_token = urllib.request.urlopen(auth_url, auth_info)
    #except:
    #    print("==== Unable to Retrieve Token ====")
    #    continue
    
    r_token = req_token.read().decode('utf-8')
    js_token = json.loads(r_token)
    token = 'Token ', js_token['token']

	#Obtain generation mix data for each balancing authority in location
    for i in range(0, ba_count):
		#Wattime url and headers
        url = 'https://api.watttime.org/api/v1/datapoints/?'
        headers = urllib.parse.urlencode({'Authorization': token, 'ba': ba_abbrev[i], \
        'start_at': start_time, 'end_at': end_time})

		#Concatenate query headers and open url
        url += headers
        print(url)
        print("")
        #input('continue with request?')
        #print("")
        try: req = urllib.request.urlopen(url)
        except:
            print("==== Unable to Open GET Request URL ====")
            break

		#Read retrieved data
        data = req.read().decode('utf-8')
        print("Retrieved ", len(data), " characters from WattTime datapoints")

		#Load data using the json library
        try: js_data = json.loads(data)
        except:
            js_data = None
            print("==== Failure to Obtain JSON Format ====")
            continue
        page = 1
        #print("Page ", page, "of request data:")
        #print("")
        #print(json.dumps(js_data, indent=4))

    	#Collect data for each generation type
    	#Note: data is retrived as MW but reduced to one hour intervals and recorded as MWh
        gen_d = {'coal': [], 'natgas': [], 'nuclear': [], 'biogas': [], 'wind': [], \
                  'geo': [], 'solarth': [], 'solarpv': [], 'smhydro': [], 'biomass': []}
        reduced_date = []
        reduced_time = []
        next_page = js_data['next']
        current_date = ['', '', '']
        current_hour = ''
        i = 0
        while next_page != None:															#Multiple pages of requested data
            len_data = len(js_data['results'])												#Number of timestamped data groups
            for j in range(0, len_data):
                mix_num = len(js_data['results'][j]['genmix'])								#Number of fuel types listed
                dat_time.append(js_data['results'][j]['timestamp'])							#Timestamp for datapoints at index dat_cnt
                time_match = time_rx.findall(dat_time[i+j])
                #print(time_match)								 							#['year', 'month', 'day', 'hour', 'minute', second']
                date = [time_match[0], time_match[1], time_match[2]]
                #print(date)
                hour = time_match[3]
                if date != current_date or hour != current_hour:
                    #print(date, "||", current_date)
                    #print(hour, "||", current_hour)
                    reduced_date.append(date[0] + "-" + date[1] + "-" + date[2])
                    reduced_time.append(hour)
                    current_date = date
                    current_hour = hour
                    #print(date, hour)
                    #print(reduced_date[dat_cnt], reduced_time[dat_cnt])
                    dat_cnt += 1															#Increment list if in new hour
                    for key, val in list(gen_d.items()): gen_d[key].append(0) 				#Append placeholder in each list for new data point if in new hour
                for k in range(0, mix_num):
                    data_freq = js_data['results'][j]['freq']
                    fuel_type = js_data['results'][j]['genmix'][k]['fuel']
                    fuel_MW = js_data['results'][j]['genmix'][k]['gen_MW']
                    if fuel_type not in list(gen_d.keys()): continue
                    else: gen_d[fuel_type][dat_cnt-1] += fuel_MW
            i += j
    		#Get next page of data
            try: next_req = urllib.request.urlopen(next_page)
            except:
                print("==== 111 Unable to retrieve subsequent pages. Data may be missing. ====")
                continue

    		#Read url data
            data = next_req.read().decode('utf-8')

    		#Load data into json format
            try:
                js_data = json.loads(data)
            except:
                js_data = None
                print("==== 222 Unable to retrieve subsequent pages. Data may be missing. ====")
                continue
            next_page = js_data['next']
            page += 1
#           print("")
#    	    print("Page ", page, "of request data:")
#    	    print("")
#    	    print(json.dumps(js_data, indent=4))


        #Display output data
        print("")
        print("coal MWh: ", gen_d['coal'])
        print("")
        print("natgas MWh: ", gen_d['natgas'])
        print("")
        print("nuclear MWh: ", gen_d['nuclear'])
        print("")
        print("biogas MWh: ", gen_d['biogas'])
        print("")
        print("wind MWh: ", gen_d['wind'])
        print("")
        print("geo MWh: ", gen_d['geo'])
        print("")
        print("solarth MWh: ", gen_d['solarth'])
        print("")
        print("solarpv MWh: ", gen_d['solarpv'])
        print("")
        print("")
        print("biomass MWh: ", gen_d['biomass'])
        print("")

        #   print("TIME: ", dat_time)
        #    total_gen = sum(gen_d.values())
        #reduced_time = [1, 2]
        #reduced_date = ['08/04', '08/04']
        print("Hourly Time: ", reduced_time)
        print("Gen Length: ", len(gen_d['biomass']))
        print("Time Tot Length: ", len(dat_time))
        print("Reduced Time Length: ", len(reduced_date))


        #-----------------------------------------------------------------------------
        #Use water an demissions factors to calculate water withdrawl, water consumption, and emissions
        gen_len = len(gen_d['biomass'])
        total_gen = np.zeros(gen_len)
        withdrawal = np.zeros(gen_len)
        consumption = np.zeros(gen_len)
        CO2 = np.zeros(gen_len)
        NOx = np.zeros(gen_len)
        SO2 = np.zeros(gen_len)

        #Import spatial emission factors
        BA_Data = ER.import_emission_factors()
        convert['coal'][2:4] = [BA_Data[ba_abbrev[i]].COAL['CO2'], BA_Data[ba_abbrev[i]].COAL['NOx'],
                                BA_Data[ba_abbrev[i]].COAL['SO2']]
        convert['natgas'][2:4] = [BA_Data[ba_abbrev[i]].GAS['CO2'], BA_Data[ba_abbrev[i]].GAS['NOx'],
                                BA_Data[ba_abbrev[i]].GAS['SO2']]
        convert['biogas'][2:4] = [BA_Data[ba_abbrev].GAS['CO2'], BA_Data[ba_abbrev[i]].GAS['NOx'],
                                BA_Data[ba_abbrev[i]].GAS['SO2']]
        convert['biomass'][2:4] = [BA_Data[ba_abbrev[i]].BIOMASS['CO2'], BA_Data[ba_abbrev[i]].BIOMASS['NOx'],
                                  BA_Data[ba_abbrev[i]].BIOMASS['SO2']]

        print(convert)

        for key, val in list(gen_d.items()):
            #print(key, ": ", val)
            withdrawal += np.multiply(val, convert[key][0])
            consumption += np.multiply(val, convert[key][1])
            CO2 += np.multiply(val, convert[key][2])
            NOx += np.multiply(val, convert[key][3])
            SO2 += np.multiply(val, convert[key][4])


        Table1 = pd.DataFrame({'Coal Produduction [MWh]': gen_d['coal'], 'Natural Gas Production [MWh]': gen_d['natgas'],\
                               'Nuclear Production [MWh]': gen_d['nuclear'], 'Bio-Gas Production [MWh]': gen_d['biogas'],\
                               'Wind Production [MWh]': gen_d['wind'], 'Geothermal Production [MWh]': gen_d['geo'],\
                               'Solar Thermal Production [MWh]': gen_d['solarth'], 'Solar PV Production [MWh]': gen_d['solarpv'],\
                               'Bio-Mass Production [MWh]': gen_d['biomass'], 'Water Withdrawal [gal]': withdrawal,\
                               'Water Consumption [gal]': consumption, 'CO2 [lbs]': CO2, 'NOx [lbs]': NOx, 'SO2 [lbs]': SO2,\
                               'Date': reduced_date, 'Time': reduced_time})
        Table2 = pd.DataFrame({})

        #-----------------------------------------------------------------------------
        #Write data to an editable excel file

        #Import the results data into the workbook
        results_writer = pd.ExcelWriter('Results.xlsx', engine='xlsxwriter')
        Table2.to_excel(results_writer, sheet_name='Metadata')
        Table1.to_excel(results_writer, sheet_name='Results')

        #Create workbook and sheets
        results_workbook = results_writer.book
        results = results_writer.sheets['Results']
        metadata = results_writer.sheets['Metadata']

        #Import metadata for this dataset
        #lat = 40.7608
        #lng = 111.8910
        #location = 'Salt Lake City, UT'
        #start_time = '2016-8-19T00:00:00'
        #end_time = '2016-8-26T23:59:00'
        #ba_name = 'Western Electricity Coordinating Council'  # name attribute - full name of balancing authority
        #ba_urls = 'https://www.wecc.biz/Pages/home.aspx'  # url attribute - location on WattTime balancing authority page
        #ba_abbrev = 'WECC'  # abbrev attribute - abbreviation for balancing authority

        metadata_output = {'Location': location, 'Latitude': lat, 'Longitude': lng, 'Start Time': start_time,\
                           'End Time': end_time, 'Balancing Authority Name': ba_name, 'Balancing Authority Abreviation':\
                           ba_abbrev, 'Balancing Authority Site': ba_urls}

        row = 0
        col = 0
        for key, val in list(metadata_output.items()):
            metadata.write(row, col, key)
            metadata.write(row, col + 1, val)
            row += 1

        #Add formating
        metadata.set_column('A:B', 35)
        results.set_column('B:O', 15)


    #-----------------------------------------------------------------------------
    #Generate Plots
    '''
    #Generation Table
    Table = pd.DataFrame(gen_d, columns = ['coal', 'natgas', 'nuclear', 'biogas', 'wind',\
                'geo', 'solarth', 'solarpv', 'smhydro', 'biomass'])

    #Generation Bar Plot
    plt.figure(1)
    N = len(gen_d['coal'])
    ind = np.arange(N)
    width = 0.35

    one = plt.bar(ind, gen_d['coal'], width, color='k')
    two = plt.bar(ind, gen_d['natgas'], width, color='g',\
    bottom=gen_d['coal'])
    three = plt.bar(ind, gen_d['nuclear'], width, color='b',\
    bottom=[i+j for i, j in zip(gen_d['coal'], gen_d['natgas'])])

    plt.ylabel('Production [MW]')
    plt.title('Fuel Mix')
    plt.xticks(ind + width/2., reduced_time)
    plt.legend(('coal', 'natgas', 'nuclear'))

    #Total Generation Pie Chart
    #	plt.figure(2)
    #   pie_labels = ['other']
    #   totals = {'other': []}
    #   for key in list(gen_d.items()):
    #       weight = sum(gen_d[key])/total_gen
    #       if weight < 0.1:
    #           totals['other'] += sum(gen_d[key])
    #       else:
    #           totals[key] = sum(gen_d[key])
    #           pie_labels.append(key)

    #  pie_labels = 'coal', 'natgas', 'nuclear', 'biogas', 'wind', 'geo', 'solarth', 'solarpv', 'smhydro', 'biomass'
    #  totals = [sum(gen_d['coal']), sum(gen_d['natgas']), sum(gen_d['nuclear']), sum(gen_d['biogas']), sum(gen_d['wind']), \
    #                sum(gen_d['geo']), sum(gen_d['solarth']), sum(gen_d['solarpv']), sum(gen_d['smhydro']), sum(gen_d['biomass'])]

    #ax1 = plt.subplots()
    #   plt.pie(totals, labels=pie_labels, shadow=False, startangle=90, autopct='%1.1f%%')
    #   plt.axis('equal')

    #Generation stacked area plot
    plt.figure(3)
    plt.stackplot(list(map(int, reduced_time)), gen_d['coal'], gen_d['natgas'], gen_d['nuclear'])
    plt.xlabel('Time [h]')
    plt.ylabel('Production [MW]')
    plt.title('Fuel Mix')

    plt.show()
    Table
    plt.pause(0.001)
    results_workbook.close()
    '''
    for key, val in list(gen_d.items()): gen_d[key] = []
					
