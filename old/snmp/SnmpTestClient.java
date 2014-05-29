/*
 * Copyright 2012 SNMP4J.org.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.snmp4j.CommandResponder;
import org.snmp4j.CommandResponderEvent;
import org.snmp4j.CommunityTarget;
import org.snmp4j.PDU;
import org.snmp4j.Snmp;
import org.snmp4j.TransportMapping;
import org.snmp4j.event.ResponseEvent;
import org.snmp4j.mp.SnmpConstants;
import org.snmp4j.smi.Address;
import org.snmp4j.smi.OID;
import org.snmp4j.smi.OctetString;
import org.snmp4j.smi.TimeTicks;
import org.snmp4j.smi.UdpAddress;
import org.snmp4j.smi.Variable;
import org.snmp4j.smi.VariableBinding;
import org.snmp4j.transport.DefaultUdpTransportMapping;

/**
 * Details on using the Snmp client http://www.snmp4j.org/doc/org/snmp4j/Snmp.html
 *
 */
public class SnmpTestClient {

	CommandResponder trapPrinter = new CommandResponder() {
		public synchronized void processPdu(CommandResponderEvent e) {
			PDU command = e.getPDU();
			if (command != null) {
				System.out.println("trap: " + command.toString());
			}
		}
	};

	public ArrayList<String> getValues(String oid) throws IOException {

		ArrayList<String> result = new ArrayList<String>();

		TransportMapping transport = new DefaultUdpTransportMapping();
		//transport.listen();

		// Create Target Address object
		CommunityTarget comtarget = new CommunityTarget();
//		comtarget.setCommunity(new OctetString(Setting.getInstance().getValue("settings", "community")));
		comtarget.setCommunity(new OctetString("public"));
		comtarget.setVersion(SnmpConstants.version2c);
//		comtarget.setAddress(new UdpAddress(Setting.getInstance().getValue("settings", "ip") + "/" + Setting.getInstance().getValue("settings", "port")));
		comtarget.setAddress(new UdpAddress("192.168.0.190" + "/" + "161"));
		comtarget.setRetries(2);
		comtarget.setTimeout(5000);

		// Create the PDU object
		PDU pdu = new PDU();
		pdu.add(new VariableBinding(new OID(oid)));
		pdu.setType(PDU.GET);
		//pdu.setRequestID(new Integer32(1));

		// Create Snmp object for sending data to Agent
		Snmp snmp = new Snmp(transport);
		snmp.addCommandResponder(trapPrinter);
		snmp.listen();
		ResponseEvent response;
		while (true) {
			response = snmp.getNext(pdu, comtarget);
			if (response != null) {
				PDU responsePDU = response.getResponse();
				System.out.println("pdu = " + responsePDU);
				if (!response.getResponse().get(0).getOid().startsWith(new OID(oid))) {
//					System.out.println("Starting with the same OID - breaking!");
//					break;
				}
				if (responsePDU != null) {
					int errorStatus = responsePDU.getErrorStatus();
					if (errorStatus == PDU.noError) {
						result.add(responsePDU.get(0).toValueString());
						pdu = response.getResponse();
						System.out.println("Adding " + responsePDU.get(0).toValueString());
					} else {
						System.out.println("Response was error: " + pdu.getErrorStatusText());
						break;
					}
				} else {
					System.out.println("PDU received was null");
					break;
				}
			} else {
				System.out.println("Response received was null");
				break;
			}
		}
		snmp.close();

		return result;
	}

	public void registerForOnBatteryTrap() throws IOException {
		PDU trap = new PDU();
		trap.setType(PDU.TRAP);

		OID oid = new OID("1.2.3.4.5");
		trap.add(new VariableBinding(SnmpConstants.snmpTrapOID, oid));
		trap.add(new VariableBinding(SnmpConstants.sysUpTime, new TimeTicks(5000))); // put your uptime here
		trap.add(new VariableBinding(SnmpConstants.sysDescr, new OctetString("System Description")));
		//Add Payload
		Variable var = new OctetString("some string");
		trap.add(new VariableBinding(oid, var));

		// Specify receiver
		Address targetaddress = new UdpAddress("10.101.21.32/162");
		CommunityTarget target = new CommunityTarget();
		target.setCommunity(new OctetString("public"));
		target.setVersion(SnmpConstants.version2c);
		target.setAddress(targetaddress);

		// Send
		Snmp snmp = new Snmp(new DefaultUdpTransportMapping());
		snmp.send(trap, target, null, null);

	}

	/**
	 ** http://www.mibdepot.com/cgi-bin/getmib3.cgi?win=mib_a&i=1628&n=UPS-MIB&r=synso&f=UPS.mib&v=v2&t=tree xtraps	GROUP
	 * upsTrapOnBattery	TRAP	1.3.6.1.2.1.33.2.1 upsTrapTestCompleted	TRAP	1.3.6.1.2.1.33.2.2 upsTrapAlarmEntryAdded	TRAP
	 * 1.3.6.1.2.1.33.2.3 upsTrapAlarmEntryRemoved TRAP	1.3.6.1.2.1.33.2.4
	 */
	public static void main(String args[]) throws IOException {
		SnmpTestClient client = new SnmpTestClient();
		String oid = "1.3.6.1.2.1.33.1.6.3.1";
		String configInputVoltageOid = "1.3.6.1.2.1.33.1.9.1.0";
		List<String> values = client.getValues(oid);
		for (String value : values) {
			System.out.println("Value = " + value);
		}
	}
}
/*
 * public static void main(String[] args) throws Exception {
 // Create PDU           
 PDU trap = new PDU();
 trap.setType(PDU.TRAP);

 OID oid = new OID("1.2.3.4.5");
 trap.add(new VariableBinding(SnmpConstants.snmpTrapOID, oid));
 trap.add(new VariableBinding(SnmpConstants.sysUpTime, new TimeTicks(5000))); // put your uptime here
 trap.add(new VariableBinding(SnmpConstants.sysDescr, new OctetString("System Description"))); 

 //Add Payload
 Variable var = new OctetString("some string");          
 trap.add(new VariableBinding(oid, var));          

 // Specify receiver
 Address targetaddress = new UdpAddress("10.101.21.32/162");
 CommunityTarget target = new CommunityTarget();
 target.setCommunity(new OctetString("public"));
 target.setVersion(SnmpConstants.version2c);
 target.setAddress(targetaddress);

 // Send
 Snmp snmp = new Snmp(new DefaultUdpTransportMapping());
 snmp.send(trap, target, null, null);                      
 }

 */
/*
 * pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.7.1.0 = 1.3.6.1.2.1.33.1.7.7.1]]
Adding 1.3.6.1.2.1.33.1.7.7.1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.7.2.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.7.3.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.7.4.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.7.5.0 = 0:00:00.00]]
Adding 0:00:00.00
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.7.6.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.8.1.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.8.2.0 = -1]]
Adding -1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.8.3.0 = -1]]
Adding -1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.8.4.0 = -1]]
Adding -1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.8.5.0 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.1.0 = 1150]]
Adding 1150
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.2.0 = 600]]
Adding 600
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.3.0 = 120]]
Adding 120
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.4.0 = 600]]
Adding 600
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.5.0 = 1399]]
Adding 1399
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.6.0 = 900]]
Adding 900
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.7.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.8.0 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.9.0 = 85]]
Adding 85
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.2.1.33.1.9.10.0 = 141]]
Adding 141
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.1.1.1.0 = Intelligent 1400]]
Adding Intelligent 1400
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.1.1.2.0 = 00]]
Adding 00
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.1.2.1.0 = 2.08]]
Adding 2.08
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.1.2.2.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.1.2.3.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.1.2.4.0 = 2.43.DP520.WEST.e]]
Adding 2.43.DP520.WEST.e
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.1.1.0 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.1.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.1.3.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.2.1.0 = 100]]
Adding 100
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.2.2.0 = 537]]
Adding 537
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.2.3.0 = 20]]
Adding 20
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.2.4.0 = 29750]]
Adding 29750
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.2.6.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.2.2.7.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.3.1.1.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.3.2.1.0 = 1206]]
Adding 1206
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.3.2.2.0 = 1229]]
Adding 1229
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.3.2.3.0 = 1174]]
Adding 1174
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.3.2.4.0 = 599]]
Adding 599
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.3.2.5.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.4.1.1.0 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.4.1.2.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.4.2.1.0 = 1211]]
Adding 1211
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.4.2.2.0 = 600]]
Adding 600
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.4.2.3.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.1.0 = 4]]
Adding 4
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.1.1 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.1.2 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.1.3 = 3]]
Adding 3
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.1.4 = 4]]
Adding 4
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.2.1 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.2.2 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.2.3 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.2.4 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.3.1 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.3.2 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.3.3 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.3.4 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.4.1 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.4.2 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.4.3 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.1.2.1.4.4 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.1.0 = 120]]
Adding 120
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.2.0 = 141]]
Adding 141
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.3.0 = 85]]
Adding 85
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.5.0 = 2147483647]]
Adding 2147483647
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.8.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.9.0 = 60]]
Adding 60
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.10.0 = 120]]
Adding 120
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.5.2.11.0 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.1.1.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.2.1.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.2.2.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.2.3.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.2.4.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.2.5.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.6.2.6.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.7.2.1.0 = 4]]
Adding 4
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.7.2.2.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.7.2.3.0 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.7.2.4.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.1.1.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.1.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.1.3.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.1.4.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.1.5.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.2.1.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.2.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.2.3.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.2.4.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.1.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.3.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.4.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.5.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.6.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.3.7.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.4.1.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.4.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.4.3.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.4.4.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.1.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.2.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.3.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.4.0 = 3]]
Adding 3
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.5.0 = 5]]
Adding 5
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.6.0 = 7]]
Adding 7
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.5.7.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.6.1.0 = 15]]
Adding 15
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.6.2.0 = 9]]
Adding 9
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.6.3.0 = 11]]
Adding 11
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.6.4.0 = 13]]
Adding 13
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.6.5.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.1.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.2.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.3.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.4.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.5.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.6.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.7.7.0 = 16]]
Adding 16
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.1.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.3.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.4.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.5.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.6.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.7.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.8.8.8.0 = ]]
Adding 
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.1.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.2.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.3.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.4.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.5.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.6.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.7.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.8.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.9.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.10.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.1.11.0 = 0]]
Adding 0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.2.1.0 = 30]]
Adding 30
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.2.2.0 = 10]]
Adding 10
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.2.3.0 = 50]]
Adding 50
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.1.1.1.9.2.4.0 = 12]]
Adding 12
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.1.0 = 8]]
Adding 8
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.1 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.2 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.3 = 3]]
Adding 3
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.4 = 4]]
Adding 4
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.5 = 5]]
Adding 5
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.6 = 6]]
Adding 6
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.7 = 7]]
Adding 7
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.1.8 = 8]]
Adding 8
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.1 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.2 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.3 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.4 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.5 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.6 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.7 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.2.8 = 0.0.0.0]]
Adding 0.0.0.0
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.1 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.2 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.3 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.4 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.5 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.6 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.7 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.3.8 = public]]
Adding public
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.1 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.2 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.3 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.4 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.5 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.6 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.7 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.4.8 = 1]]
Adding 1
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.1 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.2 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.3 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.4 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.5 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.6 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.7 = 2]]
Adding 2
pdu = RESPONSE[requestID=61036277, errorStatus=Success(0), errorIndex=0, VBS[1.3.6.1.4.1.935.2.1.2.1.5.8 = 2]]
Adding 2
**/