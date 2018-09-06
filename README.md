# electricityandenvironment
Quantifying the environmental impacts of electricity purchased from the grid

License: LGPL

This script can be used to model the water consumption, water withdrawal, CO2 emissions, NOx emissions and SO2 emissions attributed to the power generation fuel mix within a specific location over a specified time frame.

NOTE: The emissions factors used in this script are calculated with the eGRID excel database included in this repository. This database is updated every two years. The most recent database can be found here: https://www.epa.gov/energy/emissions-generation-resource-integrated-database-egrid. The most recent database should be downloaded and included in the working directory for best results. The FindEmission_Rates script will automatically use the most recent database in the directory as long as it contains egrid in the name.

User Inputs:
1) Location: The location for which the numbers will correlate to (city, state, etc.)
2) Time Frame: The start and end data/time from which data will be pulled
3) WattTime Credentials: Username and password for a valid WattTime API account

Outputs:
1) Time Array
2) Generation for each fuel type
3) Water Consumption
4) Water Withdrawal
5) COs, NOx and SO2 emissions
6) Emission factors for each fuel type
7) Water consumption and withdrawal factors for each fuel type

Instructions:
1) Download the electricityandenvironment zip file
2) Run the Power_Ex.py or Power_Ex.ipynb file if using a jupyter notebook file with the necessary dependancies (Python3, urllib, numpy, pandas)
   Note: The FindEmission_Rates.py or FindEmission_Rates.ipynb file must be located in the same folder
3) Follow the command prompts to input the necessary information corresponding to your desired data output
4) The output file will be located in the same directory as the Power_Ex.py file. It will be named Results.xlsx
