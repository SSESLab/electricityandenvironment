# PECT: Power Externality Correlation Tool
Quantifying the environmental impacts of electricity purchased from the grid

License: LGPL

Version: 1.2.0.0

*New!* Google Colaboratory Option: https://colab.research.google.com/drive/1UWDTphLkr8tja5R0HPN9nE66_8kPPYCx
       
*New!* Read the paper (open access): https://doi.org/10.1016/j.softx.2018.12.001

This script can be used to model the water consumption, water withdrawal, CO2 emissions, NOx emissions and SO2 emissions attributed to the power generation fuel mix within a specific location over a specified time frame. If the PECT.ipynb file is used in google colaboratory then there are no software requirments for running the script and obtaining outputs. However, it is best to use Google Chrome. Other browsers such as Firefox throw Network Errors when the script attempts to download the results file.

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

Instructions (Colaboratory Notebook):
1) Click on the link provided here: https://colab.research.google.com/drive/1UWDTphLkr8tja5R0HPN9nE66_8kPPYCx
2) Run each cell and provide user inputs as directed
3) Results file should be downloaded through your internet browser

Instructions (Python File):
1) Download the electricityandenvironment zip file
2) Run the Power_Ex.py or Power_Ex.ipynb file if using a jupyter notebook file with the necessary dependancies (Python3, urllib, numpy, pandas)
   Note: The FindEmission_Rates.py or FindEmission_Rates.ipynb file must be located in the same folder
3) Follow the command prompts to input the necessary information corresponding to your desired data output
4) The output file will be located in the same directory as the Power_Ex.py file. It will be named Results.xlsx

Cite: Plewe, K. & Smith, A. D. PECT: A tool for computing the temporal and spatial variation of externalities related to power generation in the United States. SoftwareX 9, 61–67 (2019). doi:10.1016/j.softx.2018.12.001
