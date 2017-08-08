######################
#Kaden Plewe
#08/06/2017
######################
#This function reads the eGRID Database file and produces emission rates coresponding to US balancing authorities
#for each fuel


import pandas as pd
import numpy as np
import math

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

    PLNT14 = pd.read_excel('eGRID2014_Data_v2_Emission_Factors.xlsm', sheetname='PLNT14', skiprows=1)
    raw_len = len(PLNT14['BACODE'])

    #print(PLNT14['BACODE'])



    #Create array of ba codes to be used in parsing data
    BA_Data = {}
    for i in range(0, raw_len):
        try: x = BA_Data[str(PLNT14['BACODE'][i])]
        except:
            BA_Data[PLNT14['BACODE'][i]] = EF()

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
            if PLNT14['BACODE'][i] == key and PLNT14['PLFUELCT'][i] == 'COAL':
                if np.isnan(PLNT14['PLNGENAN'][i]) == 0:
                    COAL_CO2_Den += PLNT14['PLNGENAN'][i]
                    COAL_NOx_Den += PLNT14['PLNGENAN'][i]
                    COAL_SO2_Den += PLNT14['PLNGENAN'][i]

                    if np.isnan(PLNT14['PLCO2RTA'][i]) == 0: COAL_CO2_Num += PLNT14['PLCO2RTA'][i]*PLNT14['PLNGENAN'][i]
                    if np.isnan(PLNT14['PLNOXRTA'][i]) == 0: COAL_NOx_Num += PLNT14['PLNOXRTA'][i]*PLNT14['PLNGENAN'][i]
                    if np.isnan(PLNT14['PLSO2RTA'][i]) == 0: COAL_SO2_Num += PLNT14['PLSO2RTA'][i]*PLNT14['PLNGENAN'][i]

        # calculate gas emission factors for each balancing authority
        for i in range(0, raw_len):
            if PLNT14['BACODE'][i] == key and PLNT14['PLFUELCT'][i] == 'GAS':
                if np.isnan(PLNT14['PLNGENAN'][i]) == 0:
                    GAS_CO2_Den += PLNT14['PLNGENAN'][i]
                    GAS_NOx_Den += PLNT14['PLNGENAN'][i]
                    GAS_SO2_Den += PLNT14['PLNGENAN'][i]

                    if np.isnan(PLNT14['PLCO2RTA'][i]) == 0: GAS_CO2_Num += PLNT14['PLCO2RTA'][i]*PLNT14['PLNGENAN'][i]
                    if np.isnan(PLNT14['PLNOXRTA'][i]) == 0: GAS_NOx_Num += PLNT14['PLNOXRTA'][i]*PLNT14['PLNGENAN'][i]
                    if np.isnan(PLNT14['PLSO2RTA'][i]) == 0: GAS_SO2_Num += PLNT14['PLSO2RTA'][i]*PLNT14['PLNGENAN'][i]

        # calculate biomass emission factors for each balancing authority
        for i in range(0, raw_len):
            if PLNT14['BACODE'][i] == key and PLNT14['PLFUELCT'][i] == 'BIOMASS':
                if np.isnan(PLNT14['PLNGENAN'][i]) == 0:
                    BIOMASS_CO2_Den += PLNT14['PLNGENAN'][i]
                    BIOMASS_NOx_Den += PLNT14['PLNGENAN'][i]
                    BIOMASS_SO2_Den += PLNT14['PLNGENAN'][i]

                    if np.isnan(PLNT14['PLCO2RTA'][i]) == 0: BIOMASS_CO2_Num += PLNT14['PLCO2RTA'][i]*PLNT14['PLNGENAN'][i]
                    if np.isnan(PLNT14['PLNOXRTA'][i]) == 0: BIOMASS_NOx_Num += PLNT14['PLNOXRTA'][i]*PLNT14['PLNGENAN'][i]
                    if np.isnan(PLNT14['PLSO2RTA'][i]) == 0: BIOMASS_SO2_Num += PLNT14['PLSO2RTA'][i]*PLNT14['PLNGENAN'][i]

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