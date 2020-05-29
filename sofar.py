import minimalmodbus
# import socket
import serial
import time
# import urlparse # obvious!

###		PROGRAM FLOW:
###			- Collect Data from Sofar HYD6000-ES inverter
###			- Convert to individual bytes
###			- Construct 2 messages 
###				- KWH Totals only sent when inverter is running, so they are not reset to zero
###				- All other 'live' data set to zero when inverter shuts down
###			- Send Packets to EMONHUB
###	
###		EmonHub Node IDs:
###			- NodeID 3: All time energy KWH	/ Today KWH (not sent overnight)
###			- NodeID 4: Live Data Readings - Zeros sent overnight 


### COLLECT DATA FROM SOFAR HYD6000 INVERTER ###

# Base url
ubase = 'http://emonpi/input/post?node=emontx&fulljson={' # URL of your emon device
emon_apikey = "e5fe98dec735e5fa17139805d902517e" # add your key here for RW access

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address 

instrument.serial.baudrate = 9600   # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.5   # seconds

# while True:
success = False # Intialise Success/Failure Flag to ensure full data is only uploaded if all data is received.

Inverter_Freq = instrument.read_register(0x20c, 0, functioncode=3, signed=False) / 100.0 # read inverter frequency

Battery_ChargeDischargePwr = instrument.read_register(0x20d, 0, functioncode=3, signed=True) * 10.0 # read battery charge discharge pwr
Battery_Cycles = instrument.read_register(0x22c, 0, functioncode=3, signed=False) # read times batteries have been cycled
Battery_ChrgLevel = instrument.read_register(0x210, 0, functioncode=3, signed=False) # read battery charge level
Battery_Temp = instrument.read_register(0X211, 0, functioncode=3, signed=True) #Read Battery Temperature as Signed 16-Bit

Grid_IO_Pwr = instrument.read_register(0x212, 0, functioncode=3, signed=True) * 10.0 # read total grid pwr

House_Consumption_Pwr = instrument.read_register(0x213, 0, functioncode=3, signed=False) * 10.0 # read load pwr

Internal_IO_Pwr = instrument.read_register(0x214, 0, functioncode=3, signed=True) * 10.0 # read internal system I/O pwr

PV_Generation_Pwr = instrument.read_register(0x215, 0, functioncode=3, signed=False) * 10.0 # read SolarPV Generation Pwr

EPS_Output_V = instrument.read_register(0x216, 0, functioncode=3, signed=False) / 10.0 # read EPS Output volts
EPS_Output_Pwr = instrument.read_register(0x217, 0, functioncode=3, signed=False) * 10.0 # read EPS Output pwr

TodayGeneratedSolar_Wh = instrument.read_register(0x218, 0, functioncode=3, signed=False) * 10.0 # read Today's generation Wh
TodaySoldSolar_Wh = instrument.read_register(0x219, 0, functioncode=3, signed=False) * 10.0 # read Today's Generation sold Wh
TodayBoughtGrid_Wh = instrument.read_register(0x21a, 0, functioncode=3, signed=False) * 10.0 # read Today's Power bought Wh
TodayConsumption_Wh = instrument.read_register(0x21b, 0, functioncode=3, signed=False) * 10.0 # read Today's consumption bought Wh

TotalLoadConsumptionH = instrument.read_register(0x222, 0, functioncode=3, signed=False) * 0xffff # Total Load Consumption kWh HighByte
TotalLoadConsumption = TotalLoadConsumptionH + instrument.read_register(0x223, 0, functioncode=3, signed=False) # Total Load Consumption kWh LowByte

InverterInternalTemp = instrument.read_register(0x238, 0, functioncode=3, signed=False) # Inverter Internal Temperature
InverterHeatsinkTemp = instrument.read_register(0x239, 0, functioncode=3, signed=False) # Inverter Heatsink Temperature

    # try:

    ##Flag to stream all data to EmonHub
success = True

    # except:
        ##EXCEPTION WILL OCCUR WHEN INVERTER SHUTS DOWN WHEN PANELS ARE OFF

        ##Flag to stream restricted data to EmonHub

    ### END COLLECT DATA FROM SOFAR INVERTER ###

    # Add the variables into the URL
Grid_PwrStr = str(Grid_IO_Pwr)
House_Consumption_PwrStr = str(House_Consumption_Pwr)
Internal_IO_PwrStr = str(Internal_IO_Pwr)
PV_Generation_PwrStr = str(PV_Generation_Pwr)
EPS_Output_VStr = str(EPS_Output_V)
EPS_Output_PwrStr = str(EPS_Output_Pwr)
TodayGenerated_WhStr = str(TodayGeneratedSolar_Wh)
TodaySold_WhStr = str(TodaySoldSolar_Wh)
TodayBought_WhStr = str(TodayBoughtGrid_Wh)
TodayConsumption_WhStr = str(TodayConsumption_Wh)
Battery_ChargeDischargePwrStr = str(Battery_ChargeDischargePwr)
Battery_CyclesStr = str(Battery_Cycles)
Battery_ChrgLevelStr = str(Battery_ChrgLevel)
InverterInternalTempStr = str(InverterInternalTemp)
InverterHeatsinkTempStr = str(InverterHeatsinkTemp)
Inverter_FreqStr = str(float("{:.1f}".format(Inverter_Freq)))

#    print("Grid Power " + Grid_PwrStr + "W")
#    print("House Consumption " + House_Consumption_PwrStr + "W")
#    print("Solar PV Generation " + PV_Generation_PwrStr + "W")
#    print("Internal I/O Power " + Internal_IO_PwrStr + "W")
#    print("EPS Output Volts " + EPS_Output_VStr + "V")
#    print("EPS Output Power " + EPS_Output_PwrStr + "W")
#    print("Today's Generation " + TodayGenerated_WhStr + "Wh")
#    print("Today's Sold " + TodaySold_WhStr + "Wh")
#    print("Today's Bought " + TodayBought_WhStr + "Wh")
#    print("Today's Consumption " + TodayConsumption_WhStr + "Wh")
    # print("All time Consumption " + str(TotalLoadConsumption) + "kW")

#    print("Battery Charge/Discharge Power " + Battery_ChargeDischargePwrStr + "W")
#    print("Battery Cycles " + Battery_CyclesStr)
#    print("Battery Charge Level " + Battery_ChrgLevelStr + "%")
#    print("Inverter Internal Temp " + InverterInternalTempStr + "C")
#    print("Inverter Heatsink Temp " + InverterHeatsinkTempStr + "C")
#   print("Grid Frequency " + Inverter_FreqStr + "Hz")

    ### STREAM RESULT TO EMONHUB ###
from urlparse import urlparse
    # from urlparse import urljoin

    # Component URL parts
str1 = "\"Grid Power\":" + Grid_PwrStr + ","
str2 = "\"House Consumption\":" + House_Consumption_PwrStr + ","
str3 = "\"Internal I/O Power\":" + Internal_IO_PwrStr + ","
str4 = "\"SolarPV Generation\":" + PV_Generation_PwrStr + ","
str5 = "\"EPS Output Volts\":" + EPS_Output_VStr + ","
str6 = "\"EPS Output Power\":" + EPS_Output_PwrStr + ","
str7 = "\"Today's Generation\":" + TodayGenerated_WhStr + ","
str8 = "\"Today's Sold\":" + TodaySold_WhStr + ","
str9 = "\"Today's Bought\":" + TodayBought_WhStr + ","
str10 = "\"Today's Consumption\":" + TodayConsumption_WhStr + ","
str11 = "\"Battery Charge/Discharge Power\":" + Battery_ChargeDischargePwrStr + ","
str12 = "\"Battery Cycles\":" + Battery_CyclesStr + ","
str13 = "\"Battery Charge Level\":" + Battery_ChrgLevelStr + ","
str14 = "\"Inverter Internal Temp\":" + InverterInternalTempStr + ","
str15 = "\"Inverter Heatsink Temp\":" + InverterHeatsinkTempStr + ","
str16 = "\"Grid Frequency\":" + Inverter_FreqStr

    # Add the final part of the URL plus API key
strend = "}" + "&apikey=" + emon_apikey

    # Construct the final URL
strTot = ubase + str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 + str11 + str12 + str13 + str14 + str15 + str16 + strend

udata = urlparse(strTot)
    # print(udata.geturl())
import requests
    # Think about using payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
    # r = requests.get('https://httpbin.org/get', params=payload)
requests.put(udata.geturl())

    ## NOT SENT WHEN INVERTER TURNS OFF
    # if success == True:
    # header = "input/post?node=emontx&fulljson={"
    # content = 
    # s.sendall(header + content)
    # + str(B1) + ' ' + str(B2) + ' ' + str(B3) + ' ' + str(B4) + ' ' + str(C1) + ' ' + str(C2) + '\r\n')

    # s.sendall('04 ' + str(A1) + ' ' + str(A2) + ' ' + str(A3) + ' ' + str(A4) + ' ' + str(D1) + ' ' + str(D2) + ' ' + str(E1) + ' ' + str(E2) + ' # ' + str(F1) + ' ' + str(F2) + ' ' + str(G1) + ' ' + str(G2) + ' ' + str(H1) + ' ' + str(H2) + ' ' + str(I1) + ' ' + str(I2) + '\r\n')
    # s.close()
    ### END SEND TO EMON HUB #
#    print("Sleeping...")
#    time.sleep(10)
