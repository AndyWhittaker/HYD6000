---
title: Sofar-HYD6000-ES-ModbusRead
author: Andy Whittaker
tags: 'Modbus, Node-RED, Emon, RS422, Sofar Inverter, Hybrid, HYD6000-ES'
categories: Solar PV
date: '2020-05-28'

---

<h1 id="sofar-hyd6000-es-modbusread">Sofar-HYD6000-ES-ModbusRead</h1>
<p>This is a very badly written Python Script to Request and Read Data from the HYD6000 Inverter RS422 Port and Write To EmonCMS (or EmonPi).</p>
<p>Since we require the script to be called at regular intervals, I have also included a very simple Node-RED script to call the Python code (currently) at 30 second intervals.</p>
<h2 id="interfacing-with-the-hyd6000">Interfacing with the HYD6000</h2>
<p>We require to interface between the Raspberry Pi and the Sofar HYD6000 inverter via RS422. On the bottom of the HYD6000 you can find the interface connections.<br>
<img src="http://andywhittaker.com/img/HYD6000-RS422-01.jpg" alt="HYD6000-ES Interface Connections"></p>

