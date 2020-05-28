---
title: Sofar-HYD6000-ES-ModbusRead
author: Andy Whittaker
tags: 'Modbus, Node-RED, Emon, RS422, Sofar Inverter, Hybrid, HYD6000-ES'
categories: Solar PV
date: '2020-05-28'

---

<h1 id="sofar-hyd6000-es-modbusread">Sofar-HYD6000-ES-ModbusRead</h1>
<p>This is a very badly written Python Script to Request and Read Data from the HYD6000 Inverter RS485 Port and Write To EmonCMS (or EmonPi).</p>
<p>Since we require the script to be called at regular intervals, I have also included a very simple Node-RED script to call the Python code (currently) at 30 second intervals.</p>
<h2 id="interfacing-with-the-hyd6000">Interfacing with the HYD6000</h2>
<p>We require to interface between the Raspberry Pi and the Sofar HYD6000 inverter via RS485. On the bottom of the HYD6000 you can find the interface connections.</p>
<p><img src="https://www.andywhittaker.com/img/HYD6000-RS485-01.jpg" alt="Sofar HYD6000 Interfaces"></p>
<p>The CAN/485m connection goes off to the batteries. However, the next interface available is the RS485s connection, Sofar even gives you the correct connector to plug-in (it looks to me like a Phoenix/ Weidmüller Type).</p>

