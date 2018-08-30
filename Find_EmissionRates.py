######################
#Kaden Plewe
#08/06/2017
######################
#This function reads the eGRID Database file and produces emission rates coresponding to US balancing authorities
#for each fuel


import pandas as pd
import numpy as np
import math
import glob
import re

#Define the class for storing emission factors
class EF:
    def __init__(self):
        self.COAL = {'CO2': 0, 'NOx': 0, 'SO2': 0}
        self.GAS = {'CO2': 0, 'NOx': 0, 'SO2': 0}
        self.BIOMASS = {'CO2': 0, 'NOx': 0, 'SO2': 0}

    def add_COAL(self, CO2, NOx, SO2):
        self.COAL['CO2'] = CO2
        self.COAL['NOx'] = NOx
        self.COAL['SO2'] = SO2

    def add_GAS(self, CO2, NOx, SO2):
        self.GAS['CO2'] = CO2
        self.GAS['NOx'] = NOx
        self.GAS['SO2'] = SO2

    def add_BIOMASS(self, CO2, NOx, SO2):
        self.BIOMASS['CO2'] = CO2
        self.BIOMASS['NOx'] = NOx
        self.BIOMASS['SO2'] = SO2

def import_emission_factors():
    #import excel data file

    #regular expression for finding sheetname
    eGRID_yr_re = re.compile('(?<=20)[0-9]*')

    #query all eGRID filenames in current folder
    filename = glob.glob('[Ee][Gg][Rr][Ii][Dd]*')
    #print(filename)

    #creat an array of all years for the eGRID files that were found
    eGRID_yr = eGRID_yr_re.findall(str(filename))
    #print(eGRID_yr)

    max_yr = np.argmax([int(i) for i in eGRID_yr])

    #make sheet name for most recent filename
    sn = 'PLNT' + eGRID_yr[max_yr]

    #query data for most recent eGRID data set in folder
    PLNT = pd.read_excel(filename[max_yr], sheetname=sn, skiprows=1)
    raw_len = len(PLNT['BACODE'])

    #print(PLNT['BACODE'])


    #Create array of ba codes to be used in parsing data
    BA_Data = {}
    for i in range(0, raw_len):
        try: x = BA_Data[str(PLNT['BACODE'][i])]
        except:
            BA_Data[PLNT['BACODE'][i]] = EF()

    #print(BA_Data)

    #Parse through data to fill BA_Data
    for key, val in list(BA_Data.items()):
        COAL_CO2_Num = 0
        COAL_CO2_Den = 0
        COAL_NOx_Num = 0
        COAL_NOx_Den = 0
        COAL_SO2_Num = 0
        COAL_SO2_Den = 0
        GAS_CO2_Num = 0
        GAS_CO2_Den = 0
        GAS_NOx_Num = 0
        GAS_NOx_Den = 0
        GAS_SO2_Num = 0
        GAS_SO2_Den = 0
        BIOMASS_CO2_Num = 0
        BIOMASS_CO2_Den = 0
        BIOMASS_NOx_Num = 0
        BIOMASS_NOx_Den = 0
        BIOMASS_SO2_Num = 0
        BIOMASS_SO2_Den = 0

        #calculate coal emission factors for each balancing authority
        for i in range(0, raw_len):
            if PLNT['BACODE'][i] == key and PLNT['PLFUELCT'][i] == 'COAL':
                if np.isnan(PLNT['PLNGENAN'][i]) == 0:
                    COAL_CO2_Den += PLNT['PLNGENAN'][i]
                    COAL_NOx_Den += PLNT['PLNGENAN'][i]
                    COAL_SO2_Den += PLNT['PLNGENAN'][i]

                    if np.isnan(PLNT['PLCO2RTA'][i]) == 0: COAL_CO2_Num += PLNT['PLCO2RTA'][i]*PLNT['PLNGENAN'][i]
                    if np.isnan(PLNT['PLNOXRTA'][i]) == 0: COAL_NOx_Num += PLNT['PLNOXRTA'][i]*PLNT['PLNGENAN'][i]
                    if np.isnan(PLNT['PLSO2RTA'][i]) == 0: COAL_SO2_Num += PLNT['PLSO2RTA'][i]*PLNT['PLNGENAN'][i]

        # calculate gas emission factors for each balancing authority
        for i in range(0, raw_len):
            if PLNT['BACODE'][i] == key and PLNT['PLFUELCT'][i] == 'GAS':
                if np.isnan(PLNT['PLNGENAN'][i]) == 0:
                    GAS_CO2_Den += PLNT['PLNGENAN'][i]
                    GAS_NOx_Den += PLNT['PLNGENAN'][i]
                    GAS_SO2_Den += PLNT['PLNGENAN'][i]

                    if np.isnan(PLNT['PLCO2RTA'][i]) == 0: GAS_CO2_Num += PLNT['PLCO2RTA'][i]*PLNT['PLNGENAN'][i]
                    if np.isnan(PLNT['PLNOXRTA'][i]) == 0: GAS_NOx_Num += PLNT['PLNOXRTA'][i]*PLNT['PLNGENAN'][i]
                    if np.isnan(PLNT['PLSO2RTA'][i]) == 0: GAS_SO2_Num += PLNT['PLSO2RTA'][i]*PLNT['PLNGENAN'][i]

        # calculate biomass emission factors for each balancing authority
        for i in range(0, raw_len):
            if PLNT['BACODE'][i] == key and PLNT['PLFUELCT'][i] == 'BIOMASS':
                if np.isnan(PLNT['PLNGENAN'][i]) == 0:
                    BIOMASS_CO2_Den += PLNT['PLNGENAN'][i]
                    BIOMASS_NOx_Den += PLNT['PLNGENAN'][i]
                    BIOMASS_SO2_Den += PLNT['PLNGENAN'][i]

                    if np.isnan(PLNT['PLCO2RTA'][i]) == 0: BIOMASS_CO2_Num += PLNT['PLCO2RTA'][i]*PLNT['PLNGENAN'][i]
                    if np.isnan(PLNT['PLNOXRTA'][i]) == 0: BIOMASS_NOx_Num += PLNT['PLNOXRTA'][i]*PLNT['PLNGENAN'][i]
                    if np.isnan(PLNT['PLSO2RTA'][i]) == 0: BIOMASS_SO2_Num += PLNT['PLSO2RTA'][i]*PLNT['PLNGENAN'][i]

        #import emission factors
        try:
            BA_Data[key].add_COAL(COAL_CO2_Num/COAL_CO2_Den, COAL_NOx_Num/COAL_NOx_Den, COAL_SO2_Num/COAL_SO2_Den)
            BA_Data[key].add_GAS(GAS_CO2_Num / GAS_CO2_Den, GAS_NOx_Num / GAS_NOx_Den, GAS_SO2_Num / GAS_SO2_Den)
            BA_Data[key].add_BIOMASS(BIOMASS_CO2_Num / BIOMASS_CO2_Den, BIOMASS_NOx_Num / BIOMASS_NOx_Den,
                                     BIOMASS_SO2_Num / BIOMASS_SO2_Den)
        except:
            pass

    return BA_Data

#BA_Data = import_emission_factors()
#print(BA_Data['MISO'].COAL)
