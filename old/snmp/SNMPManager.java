package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.snmp4j.CommandResponder;
import org.snmp4j.CommandResponderEvent;

import org.snmp4j.CommunityTarget;
import org.snmp4j.PDU;
import org.snmp4j.Snmp;
import org.snmp4j.Target;
import org.snmp4j.TransportMapping;
import org.snmp4j.event.ResponseEvent;
import org.snmp4j.event.ResponseListener;
import org.snmp4j.log.JavaLogFactory;
import org.snmp4j.log.LogFactory;
import org.snmp4j.mp.SnmpConstants;
import org.snmp4j.smi.Address;
import org.snmp4j.smi.Gauge32;
import org.snmp4j.smi.GenericAddress;
import org.snmp4j.smi.Integer32;
import org.snmp4j.smi.OID;
import org.snmp4j.smi.OctetString;
import org.snmp4j.smi.Variable;
import org.snmp4j.smi.VariableBinding;
import org.snmp4j.transport.DefaultUdpTransportMapping;

/**
 * @See http://shivasoft.in/blog/java/snmp/create-snmp-client-in-java-using-snmp4j/
 * @See http://www.oidview.com/mibs/0/UPS-MIB.html
 */
public class SNMPManager {

	Snmp snmp = null;
	String address = null;
	TransportMapping transport;
	private static final Logger logger = Logger.getLogger(SNMPManager.class.getName());

	/**
	 * Constructor
	 *
	 * @param add
	 */
	public SNMPManager(String address) {
		this();
		this.address = address;
	}

	public SNMPManager() {
		LogFactory.setLogFactory(new JavaLogFactory());
		LogFactory f = LogFactory.getLogFactory();
//		f.getRootLogger().setLogLevel(LogLevel.DEBUG);
	}
// Do not forget this line!
	CommandResponder trapPrinter = new CommandResponder() {
		public synchronized void processPdu(CommandResponderEvent e) {
			PDU command = e.getPDU();
			if (command != null) {
				System.out.println("trap: " + command.toString());
			}
		}
	};

	/**
	 * Start the Snmp session. If you forget the listen() method you will not get any answers because the communication is
	 * asynchronous and the listen() method listens for answers.
	 *
	 * @throws IOException
	 */
	public void start() throws IOException {
		this.transport = new DefaultUdpTransportMapping();
		snmp = new Snmp(this.transport);
//		snmp.addCommandResponder(trapPrinter);
		transport.listen();
	}

	public boolean isStarted() {
		if (this.transport != null) {
			return true;
		} else {
			return false;
		}
	}

	public void stop() throws IOException {
		if (transport != null) {
			snmp.close();
		}
	}

	/**
	 * Method which takes a single OID and returns the response from the agent as a String.
	 *
	 * @param oid
	 * @return
	 * @throws IOException
	 */
	public String getAsString(OID oid) throws IOException {
		ResponseEvent event = get(new OID[]{oid});
		return event.getResponse().get(0).getVariable().toString();
	}

	public String getAsString(String oid) throws IOException {
		return this.getAsString(new OID(oid));
	}

	public int getAsInt(String oid) throws IOException {
		return this.getAsInt(new OID(oid));
	}

	public int getAsInt(OID oid) throws IOException {
		ResponseEvent event = get(new OID[]{oid});
		return event.getResponse().get(0).getVariable().toInt();
	}

	/**
	 * This method is capable of handling multiple OIDs
	 *
	 * @param oids
	 * @return
	 * @throws IOException
	 */
	public ResponseEvent get(OID oids[]) throws IOException {
		PDU pdu = new PDU();
		for (OID oid : oids) {
			pdu.add(new VariableBinding(oid));
		}
		pdu.setType(PDU.GET);
		ResponseEvent event = snmp.send(pdu, getTarget(), null);
		if (event != null) {
			return event;
		}
		throw new RuntimeException("GET timed out");
	}

	public ResponseEvent setAsString(String oidString, String value) throws IOException {
		OID oid = new OID(oidString);
		return this.set(oid, value);
	}

	public ResponseEvent set(OID oid, String value) throws IOException {
		PDU pdu = new PDU();
		Variable var = new OctetString(value);
		VariableBinding vb = new VariableBinding(oid, var);
		pdu.add(vb);
		pdu.setType(PDU.SET);
		return snmp.set(pdu, getTarget());
	}

	public ResponseEvent set(OID oid, int value) throws IOException {
		PDU pdu = new PDU();
		Variable var = new Integer32(value);
		VariableBinding vb = new VariableBinding(oid, var);
		pdu.add(vb);
		pdu.setType(PDU.SET);
		ResponseEvent response = snmp.set(pdu, getTarget());
		return response;
//		System.out.println("error status = " + response.getResponse().getErrorStatusText());
	}

	public ResponseEvent setGaugeValue(OID oid, int value) throws IOException {
		PDU pdu = new PDU();
		Variable var = new Gauge32(value);
		VariableBinding vb = new VariableBinding(oid, var);
		pdu.add(vb);
		pdu.setType(PDU.SET);
		ResponseEvent response = snmp.set(pdu, getTarget());
		return response;
//		System.out.println("error status = " + response.getResponse().getErrorStatusText());
	}

	/**
	 * This method returns a Target, which contains information about where the data should be fetched and how.
	 *
	 * @return
	 */
	private Target getTarget() {
		Address targetAddress = GenericAddress.parse(address);
		CommunityTarget target = new CommunityTarget();
		target.setCommunity(new OctetString("public"));
		target.setAddress(targetAddress);
		target.setRetries(2);
		target.setTimeout(1500);
		target.setVersion(SnmpConstants.version2c);
		return target;
	}

	public void getPrintValue(String name, String oid) throws IOException {
		this.getPrintValue(name, new OID(oid));
	}

	public void getPrintValue(String name, OID oid) throws IOException {
		String value = this.getAsString(oid);
//		System.out.println(name + ": " + value);
	}

	private Target getDiscoveryTarget(String address, int timeout) {
		Address targetAddress = GenericAddress.parse("udp:" + address + "/161");
		CommunityTarget target = new CommunityTarget();
		target.setCommunity(new OctetString("public"));
		target.setAddress(targetAddress);
		target.setRetries(1);
		target.setTimeout(timeout);
		target.setVersion(SnmpConstants.version2c);
		return target;
	}

	public String getUpsLocation(Target target) {
		String location = "N/A";
		PDU pdu = new PDU();
		OID systemName = new OID(UPS_Constants.SYSTEM_NAME);
		pdu.add(new VariableBinding(systemName));
		pdu.setType(PDU.GET);
		ResponseEvent event;
		try {
			event = snmp.send(pdu, target, null);
			if (event != null) {
				if (event.getResponse() != null) {
					location = event.getResponse().get(0).getVariable().toString();
				}
			}
		} catch (IOException ex) {
			logger.log(Level.SEVERE, null, ex);
		}
		return location;
	}

	private boolean isUps(Target target) {
		PDU pdu = new PDU();
		OID upsManufacturerOid = new OID("1.3.6.1.2.1.33.1.1.1.0");
		pdu.add(new VariableBinding(upsManufacturerOid));
		pdu.setType(PDU.GET);
		ResponseEvent event;
		try {

			event = snmp.send(pdu, target, null);
			boolean isUps = this.isUps(event);
			return isUps;
		} catch (IOException ex) {
			logger.log(Level.SEVERE, null, ex);
		}
		return false;
	}

	private boolean isUps(ResponseEvent event) {
		if (event != null) {
			if (event.getResponse() == null) {
				return false;
			}
			String response = event.getResponse().get(0).getVariable().toString();
			logger.info(response);
			if ("INTELLIPOWER".equalsIgnoreCase(response)) {
				return true;
			} else {
				return false;
			}
		}
		return false;
	}

	private int[] toInts(String address) {
		String[] stringOctets = address.split("\\.");
		int octets[] = new int[stringOctets.length];
		for (int i = 0; i < octets.length; i++) {
			octets[i] = Integer.parseInt(stringOctets[i]);
		}
		return octets;
	}

	public void findAvailableUpsAddresses(final Set<String> upses, String broadcastAddress, int waitTimeMs) {
		final ResponseListener listener = new ResponseListener() {
			@Override
			public void onResponse(ResponseEvent event) {
				print(event);
				boolean isUps = isUps(event);
				if (isUps) {
					String address = event.getPeerAddress().toString();
					upses.add(address);
					print(event);
				}
			}

			private void print(ResponseEvent event) {
				if (event.getResponse() == null) {
					return;
				}
				String response = event.getResponse().get(0).getVariable().toString();
				String address = event.getPeerAddress().toString();
				logger.info(address + ":" + response);
			}
		};

		Target target = this.getDiscoveryTarget(broadcastAddress, waitTimeMs);
//		Target target = this.getDiscoveryTarget("192.168.117.255", 10000);
		PDU pdu = new PDU();
		OID upsManufacturerOid = new OID("1.3.6.1.2.1.33.1.1.1.0");
//		OID upsManufacturerOid = new OID("1.3.6.1.2.1.1.5.0");
//		OID deviceName = new OID("1.3.6.1.2.1.1.1.0");
		pdu.add(new VariableBinding(upsManufacturerOid));
//		pdu.add(new VariableBinding(deviceName));
		pdu.setType(PDU.GET);
		try {
			snmp.send(pdu, target, null, listener);
		} catch (IOException ex) {
			Logger.getLogger(SNMPManager.class.getName()).log(Level.SEVERE, null, ex);
		}
		try {
			Thread.sleep(waitTimeMs * 2);
		} catch (InterruptedException ex) {
			logger.log(Level.SEVERE, "Sleep interrupted", ex);
		}
	}

	public void findAvailableUpsAddresses(final Map<String, String> addressNames, String startingAddress, String endingAddress, int pollTimeMs) {
		int startingOctets[] = this.toInts(startingAddress);
		int endingOctets[] = this.toInts(endingAddress);

		for (int i0 = startingOctets[0]; i0 <= endingOctets[0]; i0++) {
			for (int i1 = startingOctets[1]; i1 <= endingOctets[1]; i1++) {
				for (int i2 = startingOctets[2]; i2 <= endingOctets[2]; i2++) {
					for (int i3 = startingOctets[3]; i3 <= endingOctets[3]; i3++) {
						String targetAddress = i0 + "." + i1 + "." + i2 + "." + i3;
						Target target = this.getDiscoveryTarget(targetAddress, pollTimeMs);
						logger.fine(targetAddress);
						if (this.isUps(target)) {
							logger.info("Found UPS at " + targetAddress);
							String location = this.getUpsLocation(target);
							addressNames.put(targetAddress, location);
						}
					}
				}
			}
		}
	}

	public static void main(String[] args) throws Exception {
		/**
		 * Port 161 is used for Read and Other operations Port 162 is used for the trap generation
		 */
		//SNMPManager client = new SNMPManager("udp:127.0.0.1/161");
		//SNMPManager client = new SNMPManager("udp:192.168.0.190/161");
		SNMPManager client = new SNMPManager("udp:192.168.117.50/161");
		client.start();

		long t0 = System.currentTimeMillis();
		Set<String> addresses = new HashSet<String>();
		if (true) {
			//client.findAvailableUpsAddresses(addresses, "192.168.127.255",10000);
			client.findAvailableUpsAddresses(addresses, "255.255.255.255", 10000);
			Thread.currentThread().sleep(10000);
		} else {
			Map<String, String> map = new HashMap<String, String>();
			client.findAvailableUpsAddresses(map, "192.168.117.0", "192.168.117.255", 50);
		}
		long t1 = System.currentTimeMillis();
		logger.info((t1 - t0) / 1000.0 + " seconds to find UPSes ");
		/**
		 * OID - .1.3.6.1.2.1.1.1.0 => SysDec OID - .1.3.6.1.2.1.1.5.0 => SysName => MIB explorer will be usefull here, as
		 * discussed in previous article
		 */
		client.getPrintValue("System Description: ", "1.3.6.1.2.1.1.1.0");

		String batteryCharge = "1.3.6.1.2.1.33.1.2.4.0";

		String charge = client.getAsString(new OID(batteryCharge));
		System.out.println("battery charge: " + charge);

		String secondsOnBattery = "1.3.6.1.2.1.33.1.2.2.0";
		String seconds = client.getAsString(new OID(secondsOnBattery));
		System.out.println("secondsOnBattery: " + seconds);

		String upsBattery = "1.3.6.1.2.1.33.1.2.1.0";
		ResponseEvent battery = client.get(new OID[]{new OID(upsBattery)});
		System.out.println("battery status: " + battery.getResponse().get(0).getVariable());

		String secondsLeft = "1.3.6.1.2.1.33.1.2.3.0";
		String secondsL = client.getAsString(new OID(secondsLeft));
		System.out.println("secondsLeft: " + secondsL);

//		SET: 1.3.6.1.2.1.33.1.9.8.0: 3
		String mute = "1.3.6.1.2.1.33.1.9.8.0";
		client.set(new OID(mute), 2);
		ResponseEvent muted = client.get(new OID[]{new OID(mute)});
		System.out.println("mute status: " + muted.getResponse().get(0).getVariable());

//		Thread.sleep(Integer.MAX_VALUE);
		// filer = 192.168.112.31
	}
}
