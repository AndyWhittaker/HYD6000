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
<p>We now need a cheap USB to RS485 (which is a two wire interface) to allow us to connect to our Raspberry Pi. Note RS485 is completely different from RS232, do not attempt to use the wrong interface. log-on to eBay and search for RS422 interfaces and you will have one in your possession within a few days. If you would like to read up about the differences between RS232, RS422 and RS485, please have a short Google search for them. RS422 and RS485 are similar, just full-duplex verses half-duplex.</p>
<p><img src="https://www.andywhittaker.com/img/RS485-Interface01.jpg" alt="RS485 Interface"></p>
<p>Link the interface up with the inverter with a length of CAT5 pair of wire. Be sure to match-up the + and - connections on either end. In my case, TX- connects to D- and TX+ connects to D+.</p>
<h2 id="setting-up-the-raspberry-pi">Setting up the Raspberry Pi</h2>
<h3 id="emonpi">EmonPi</h3>
<p>The guys over at <a href="https://openenergymonitor.org/">openenergymonitor.org</a> have created a really easy guide to have your Raspberry Pi up and running with emoncms in no time. If you would like to use <a href="https://github.com/openenergymonitor/emonpi/wiki/emonSD-pre-built-SD-card-Download-&amp;-Change-Log#emonsd-17oct19-stable">emonpi</a> head along to their <a href="https://github.com/openenergymonitor/emonpi">GitHub repository</a> and follow the instructions.</p>
<p>Don’t forget to do the usual</p>
<pre><code>sudo apt update &amp;&amp; sudo apt full-update
</code></pre>
<p>afterwards to ensure your Pi is up to date. While you are setting up, make sure you enable SSH access so that you don’t have to connect a monitor and keyboard while you set the whole thing up.</p>
<h3 id="usb-interface">USB Interface</h3>
<p>Plug the USB RS485 interface into a spare USB port and reboot the Pi. SSH back in and type</p>
<pre><code>dmesg | grep tty
</code></pre>
<p>dmesg is a copy of the Pi’s boot log and grep does a search through it for anything that matches tty. This will give you the port number that your interface is attached to (look for ttyUSB0 or similar).</p>
<p>If you look at the top of the <a href="http://sofar.py">sofar.py</a> file, you’ll see some import statements</p>

