package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import com.ticomgeo.smacks.shutdown.server.api.DefaultUpsStatusEvent;
import com.ticomgeo.smacks.shutdown.server.api.UpsStatusEvent;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.Vector;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.snmp4j.PDU;
import org.snmp4j.event.ResponseEvent;
import org.snmp4j.mp.SnmpConstants;
import org.snmp4j.smi.OID;
import org.snmp4j.smi.TimeTicks;
import org.snmp4j.smi.VariableBinding;

public class UpsMonitor implements UPS_Constants {

	private boolean useStandardSnmpCommands = false;
	private String name;
	private String hostname;
	private String ipAddress;
	SNMPManager snmp;
	private final static Logger logger = Logger.getLogger(UpsMonitor.class.getName());
	private final static long DEFAULT_POLL_TIME_SECONDS = 30;
	private long pollTimeSeconds;
	UpsStatusEvent currentUpsStatus;
	private final Set<UpsListener> upsListeners = new HashSet<UpsListener>();

	public UpsMonitor(String name, String ipAddress, String hostname) {
		this(name,ipAddress,hostname,DEFAULT_POLL_TIME_SECONDS);
	}

	public UpsMonitor(String name, String ipAddress, String hostname, long pollTimeSeconds) {
		this.name = name;
		this.ipAddress = ipAddress;
		this.hostname = hostname;
		this.pollTimeSeconds = pollTimeSeconds;
	}

	public void connect() throws IOException {
		this.snmp = new SNMPManager("udp:" + this.getIpAddress() + "/161");
		poller.start();
	}

	public UpsStatusEvent getCurrentUpsStatus() {
		return this.currentUpsStatus;
	}

	public boolean isUseStandardSnmpCommands() {
		return useStandardSnmpCommands;
	}

	public void setUseStandardSnmpCommands(boolean useStandardSnmpCommands) {
		this.useStandardSnmpCommands = useStandardSnmpCommands;
	}

	public long getPollTimeSeconds() {
		return pollTimeSeconds;
	}

	public void setPollTimeSeconds(long pollTimeSeconds) {
		this.pollTimeSeconds = pollTimeSeconds;
	}

	public String getIpAddress() {
		return ipAddress;
	}

	public void setIpAddress(String ipAddress) {
		this.ipAddress = ipAddress;
	}

	public void reconnect() {
		if(this.snmp.isStarted()) {
			this.stopPolling();
		}
		this.snmp = new SNMPManager("udp:" + this.getIpAddress() + "/161");
		this.poller = new Thread(this.pollerRunnable);
		this.poller.start();
	}

	public void changeIpAddress(String ipAddress) throws IOException {
		this.setIpAddress(ipAddress);
		this.reconnect();
	}

	public interface UpsListener {

		void received(UpsStatusEvent upsStatusEvent);
	}

	private void notifyListeners(UpsStatusEvent upsStatusEvent) {
		synchronized (this.upsListeners) {
			for (UpsListener listener : this.upsListeners) {
				try {
					listener.received(upsStatusEvent);
				} catch (Throwable t) {
					logger.log(Level.SEVERE, t.getMessage(), t);
				}
			}
		}
	}

	public void addUpsListener(UpsListener listener) {
		synchronized (this.upsListeners) {
			this.upsListeners.add(listener);
		}
	}

	public void removeUpsListener(UpsListener listener) {
		synchronized (this.upsListeners) {
			this.upsListeners.remove(listener);
		}
	}

	private Runnable pollerRunnable = new Runnable() {
		@Override
		public void run() {
			try {
				snmp.start();
				while (!Thread.interrupted()) {
					long t0 = System.currentTimeMillis();
					UpsStatusEvent use = pollUpsBatched();
					if (use != null) {
						currentUpsStatus = use;
						notifyListeners(use);
						long t1 = System.currentTimeMillis();
						logger.log(Level.INFO, "Time to poll UPS (ms){0}", (t1 - t0));
						logger.info(use.toString());
					}
					try {
						synchronized (this) {
							this.wait(getPollTimeSeconds() * 1000);
						}
					} catch (InterruptedException ex) {
						break;
					}
				}
				snmp.stop();
				logger.info("Exiting Thread");
			} catch (Exception ex) {
				logger.log(Level.WARNING, "Error polling UPS at " + getIpAddress(), ex);
			}
		}
	};

	private Thread poller = new Thread(this.pollerRunnable);

	public void stopPolling() {
		synchronized (poller) {
			poller.interrupt();
		}
	}


	private UpsStatusEvent pollUpsBatched() throws IOException {

		DefaultUpsStatusEvent ups = new DefaultUpsStatusEvent(this.hostname, this.hostname, this.name, this.getIpAddress());

		String oids[] = new String[]{
			SnmpConstants.sysUpTime.toString(),
			UpsStatusEvent.BatteryStatus.getOid(),
			TIME_REMAINING_OID,
			MANUFACTURER_OID,
			MODEL_OID,
			OUTPUT_POWER_SOURCE_OID,
			STD_INPUT_VOLTAGE,
			STD_OUTPUT_VOLTAGE,
			STD_TEMPERATURE_CELSIUS,
			NON_STD_INPUT_VOLTAGE,
			NON_STD_OUTPUT_VOLTAGE,
			NON_STD_TEMPERATURE_CELSIUS,
			ESTIMATED_PERCENTAGE_CHARGE_REMAINING,
			STD_INPUT_CURRENT_OID, 
			STD_OUTPUT_CURRENT_OID,
			NON_STD_OUTPUT_PERCENT_LOAD_OID,
			STD_OUTPUT_PERCENT_LOAD_OID,
			STD_OUTPUT_POWER_OID,
			SYSTEM_NAME
		};

		OID oidArray[] = new OID[oids.length];
		for (int i = 0; i < oids.length; i++) {
			oidArray[i] = new OID(oids[i]);
		}
		ResponseEvent responseEvent = snmp.get(oidArray);

		PDU response = responseEvent.getResponse();
		if (response == null) {
			return null;
		}

		int uptimeHundredthsSeconds = response.getVariable(SnmpConstants.sysUpTime).toInt();
		ups.setUptimeSeconds(uptimeHundredthsSeconds);

		TimeTicks tt = new TimeTicks(uptimeHundredthsSeconds);
		ups.setUptime(tt.toString());

		int status = response.getVariable(new OID(UpsStatusEvent.BatteryStatus.getOid())).toInt();
		ups.setBatteryStatus(status);

		int timeRemaining = response.getVariable(new OID(TIME_REMAINING_OID)).toInt();
		ups.setEstimatedMinutesOfRemainingCharge(timeRemaining);

		String manufacturer = response.getVariable(new OID(MANUFACTURER_OID)).toString();
		ups.setManufacturer(manufacturer);

		String model = response.getVariable(new OID(MODEL_OID)).toString();
		ups.setModel(model);

		int outputPowerSource = response.getVariable(new OID(OUTPUT_POWER_SOURCE_OID)).toInt();
		ups.setOutputPowerSource(outputPowerSource);

		if (isUseStandardSnmpCommands()) {
			int inputVoltage = response.getVariable(new OID(STD_INPUT_VOLTAGE)).toInt();
			ups.setInputVoltage(inputVoltage);

			int outputVoltage = response.getVariable(new OID(STD_OUTPUT_VOLTAGE)).toInt();
			ups.setOutputVoltage(outputVoltage);

			int temperatureCelsius = response.getVariable(new OID(STD_TEMPERATURE_CELSIUS)).toInt();
			ups.setTemperatureCelsius(temperatureCelsius);

			int percentOutputLoad = response.getVariable(new OID(STD_OUTPUT_PERCENT_LOAD_OID)).toInt();
			ups.setOutputPercentLoad(percentOutputLoad);
		} else {
			int inputVoltage = response.getVariable(new OID(NON_STD_INPUT_VOLTAGE)).toInt();
			ups.setInputVoltage(inputVoltage / 10.0);

			int outputVoltage = response.getVariable(new OID(NON_STD_OUTPUT_VOLTAGE)).toInt();
			ups.setOutputVoltage(outputVoltage / 10.0);

			int temperatureCelsius = response.getVariable(new OID(NON_STD_TEMPERATURE_CELSIUS)).toInt();
			ups.setTemperatureCelsius(temperatureCelsius / 10.0);

			int percentOutputLoad = response.getVariable(new OID(NON_STD_OUTPUT_PERCENT_LOAD_OID)).toInt();
			ups.setOutputPercentLoad(percentOutputLoad);
			
		}

		int outputPowerWatts = response.getVariable(new OID(STD_OUTPUT_POWER_OID)).toInt();
		ups.setOutputPowerWatts(outputPowerWatts);

		int inputCurrent = response.getVariable(new OID(STD_INPUT_CURRENT_OID)).toInt();
		ups.setInputCurrentAmps(((double)inputCurrent)/10.0);

		int outputCurrent = response.getVariable(new OID(STD_OUTPUT_CURRENT_OID)).toInt();
		ups.setOutputCurrentAmps(((double)outputCurrent)/10.0);


		int estimatedPercentageOfChargeRemaining = response.getVariable(new OID(ESTIMATED_PERCENTAGE_CHARGE_REMAINING)).toInt();
		ups.setEstimatedPercentageOfRemainingCharge(estimatedPercentageOfChargeRemaining);

		String upsName = response.getVariable(new OID(SYSTEM_NAME)).toString();

		return ups;
	}

	private void printUps() throws IOException {

		OID sysDescr = SnmpConstants.sysDescr;
		snmp.getPrintValue("System Description", sysDescr);

		OID upTime = SnmpConstants.sysUpTime;
		snmp.getPrintValue("Up Time", upTime);

		snmp.getPrintValue("battery charge: ", "1.3.6.1.2.1.33.1.2.4.0");

		snmp.getPrintValue("secondsOnBattery: ", "1.3.6.1.2.1.33.1.2.2.0");

		// 2 - Normal, 3 - Low
		snmp.getPrintValue("battery status: ", "1.3.6.1.2.1.33.1.2.1.0");

		snmp.getPrintValue("Estimated minutes left: ", "1.3.6.1.2.1.33.1.2.3.0");

		snmp.getPrintValue("Estimated seconds left (proprietary): ", "1.3.6.1.4.1.935.1.1.1.2.2.4.0");

		snmp.getPrintValue("Input Voltage: ", "1.3.6.1.2.1.33.1.3.3.1.3.0");

		snmp.getPrintValue("Voltage: ", "1.3.6.1.4.1.935.1.1.1.5.2.10.0");

		snmp.getPrintValue("Nominal Input Voltage*10: ", "1.3.6.1.2.1.33.1.9.1.0");

		snmp.getPrintValue("Nominal Output Voltage ", "1.3.6.1.2.1.33.1.9.3.0");

		snmp.getPrintValue("Output Voltage ", "1.3.6.1.2.1.33.1.4.4.1.2.0");

		snmp.getPrintValue("Input Frequency: ", "1.3.6.1.2.1.33.1.3.3.1.2.0");

		snmp.getPrintValue("Manufacturer: ", "1.3.6.1.2.1.33.1.1.1.0");

		snmp.getPrintValue("Model: ", "1.3.6.1.2.1.33.1.1.2.0");

		if (true) {
			String oids[] = new String[]{
				"1.3.6.1.4.1.935.1.1.1.1.1.1.0",
				"1.3.6.1.4.1.935.1.1.1.3.2.1.0", // input voltage
				"1.3.6.1.4.1.935.1.1.1.3.2.3.0", // max input voltage
				"1.3.6.1.4.1.935.1.1.1.3.2.2.0", // min input voltage
				"1.3.6.1.4.1.935.1.1.1.4.2.1.0", // output voltage
				"1.3.6.1.4.1.935.1.1.1.4.2.3.0",
				"1.3.6.1.4.1.935.1.1.1.2.2.3.0",
				"1.3.6.1.4.1.935.1.1.1.3.2.4.0",
				"1.3.6.1.4.1.935.1.1.1.2.1.1.0",
				"1.3.6.1.4.1.935.1.1.1.4.1.1.0",
				"1.3.6.1.4.1.935.1.1.1.2.2.2.0",
				"1.3.6.1.4.1.935.1.1.1.2.2.1.0",
				"1.3.6.1.4.1.935.1.1.1.5.2.1.0",
				"1.3.6.1.4.1.935.1.1.1.1.2.1.0",
				"1.3.6.1.4.1.935.1.1.1.7.2.3.0",
				"1.3.6.1.4.1.935.1.1.1.5.2.10.0",
				"1.3.6.1.4.1.935.1.1.1.5.2.11.0",
				"1.3.6.1.4.1.935.1.1.1.7.2.1.0",
				"1.3.6.1.4.1.935.1.1.1.2.2.6.0",
				"1.3.6.1.2.1.33.1.9.2.0"
			};
			OID oidArray[] = new OID[oids.length];
			for (int i = 0; i < oids.length; i++) {
				oidArray[i] = new OID(oids[i]);
			}
			ResponseEvent response = snmp.get(oidArray);
			Vector bindings = response.getResponse().getVariableBindings();
			for (Object o : bindings) {
				VariableBinding vb = (VariableBinding) o;
				System.out.println(vb);
			}
		}

	}

	public static void main(String args[]) throws Exception {
		UpsMonitor m = new UpsMonitor("Test UPS", "192.168.207.10","localhost");
		m.connect();
		Thread.sleep(20000);
		System.out.println("changing IP address");
		m.changeIpAddress("192.168.207.9");
	}
}

/*
 No.     Time        Source                Destination           Protocol Info
 862927 17587.674599 192.168.0.190         192.168.3.135         SNMP     get-response SNMPv2-MIB::sysUpTime.0 SNMPv2-MIB::sysContact.0 SNMPv2-MIB::sysName.0 SNMPv2-MIB::sysLocation.0 SNMPv2-SMI::enterprises.935.1.1.1.1.1.1.0 SNMPv2-SMI::enterprises.935.1.1.1.3.2.1.0 SNMPv2-SMI::enterprises.935.1.1.1.4.2.1.0 SNMPv2-SMI::enterprises.935.1.1.1.4.2.3.0 SNMPv2-SMI::enterprises.935.1.1.1.2.2.3.0 SNMPv2-SMI::enterprises.935.1.1.1.3.2.4.0 SNMPv2-SMI::enterprises.935.1.1.1.2.1.1.0 SNMPv2-SMI::enterprises.935.1.1.1.4.1.1.0 SNMPv2-SMI::enterprises.935.1.1.1.2.2.2.0 SNMPv2-SMI::enterprises.935.1.1.1.2.2.1.0 SNMPv2-SMI::enterprises.935.1.1.1.5.2.1.0 SNMPv2-SMI::enterprises.935.1.1.1.1.2.1.0 SNMPv2-SMI::enterprises.935.1.1.1.7.2.3.0 SNMPv2-SMI::enterprises.935.1.1.1.5.2.10.0 SNMPv2-SMI::enterprises.935.1.1.1.5.2.11.0 SNMPv2-SMI::enterprises.935.1.1.1.7.2.1.0 SNMPv2-SMI::enterprises.935.1.1.1.2.2.6.0 RFC1213-MIB::mib-2.33.1.9.2.0

 Frame 862927 (562 bytes on wire, 562 bytes captured)
 Arrival Time: Nov  8, 2012 13:33:25.817102000
 [Time delta from previous captured frame: 0.003314000 seconds]
 [Time delta from previous displayed frame: 0.018068000 seconds]
 [Time since reference or first frame: 17587.674599000 seconds]
 Frame Number: 862927
 Frame Length: 562 bytes
 Capture Length: 562 bytes
 [Frame is marked: False]
 [Protocols in frame: eth:ip:udp:snmp]
 [Coloring Rule Name: UDP]
 [Coloring Rule String: udp]
 Ethernet II, Src: MegaSyst_09:4c:61 (00:03:ea:09:4c:61), Dst: Dell_e3:e6:44 (00:1a:a0:e3:e6:44)
 Destination: Dell_e3:e6:44 (00:1a:a0:e3:e6:44)
 Address: Dell_e3:e6:44 (00:1a:a0:e3:e6:44)
 .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
 .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
 Source: MegaSyst_09:4c:61 (00:03:ea:09:4c:61)
 Address: MegaSyst_09:4c:61 (00:03:ea:09:4c:61)
 .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
 .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
 Type: IP (0x0800)
 Internet Protocol, Src: 192.168.0.190 (192.168.0.190), Dst: 192.168.3.135 (192.168.3.135)
 Version: 4
 Header length: 20 bytes
 Differentiated Services Field: 0x00 (DSCP 0x00: Default; ECN: 0x00)
 0000 00.. = Differentiated Services Codepoint: Default (0x00)
 .... ..0. = ECN-Capable Transport (ECT): 0
 .... ...0 = ECN-CE: 0
 Total Length: 548
 Identification: 0xecc9 (60617)
 Flags: 0x00
 0... = Reserved bit: Not set
 .0.. = Don't fragment: Not set
 ..0. = More fragments: Not set
 Fragment offset: 0
 Time to live: 64
 Protocol: UDP (0x11)
 Header checksum: 0x066a [correct]
 [Good: True]
 [Bad : False]
 Source: 192.168.0.190 (192.168.0.190)
 Destination: 192.168.3.135 (192.168.3.135)
 User Datagram Protocol, Src Port: snmp (161), Dst Port: netopia-vo4 (1842)
 Source port: snmp (161)
 Destination port: netopia-vo4 (1842)
 Length: 528
 Checksum: 0x0000 (none)
 Good Checksum: False
 Bad Checksum: False
 Simple Network Management Protocol
 version: version-1 (0)
 community: public
 data: get-response (2)
 get-response
 request-id: 1
 error-status: noError (0)
 error-index: 0
 variable-bindings: 22 items
 SNMPv2-MIB::sysUpTime.0 (1.3.6.1.2.1.1.3.0): 112424600
 Object Name: 1.3.6.1.2.1.1.3.0 (SNMPv2-MIB::sysUpTime.0)
 Scalar Instance Index: 0
 SNMPv2-MIB::sysUpTime: 112424600
 SNMPv2-MIB::sysContact.0 (1.3.6.1.2.1.1.4.0): Administrator
 Object Name: 1.3.6.1.2.1.1.4.0 (SNMPv2-MIB::sysContact.0)
 Scalar Instance Index: 0
 SNMPv2-MIB::sysContact: Administrator
 SNMPv2-MIB::sysName.0 (1.3.6.1.2.1.1.5.0): UPS Agent
 Object Name: 1.3.6.1.2.1.1.5.0 (SNMPv2-MIB::sysName.0)
 Scalar Instance Index: 0
 SNMPv2-MIB::sysName: UPS Agent
 SNMPv2-MIB::sysLocation.0 (1.3.6.1.2.1.1.6.0): My Office
 Object Name: 1.3.6.1.2.1.1.6.0 (SNMPv2-MIB::sysLocation.0)
 Scalar Instance Index: 0
 SNMPv2-MIB::sysLocation: My Office
 SNMPv2-SMI::enterprises.935.1.1.1.1.1.1.0 (1.3.6.1.4.1.935.1.1.1.1.1.1.0): 496E74656C6C6967656E742031343030
 Object Name: 1.3.6.1.4.1.935.1.1.1.1.1.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.1.1.1.0)
 Value (OctetString): 496E74656C6C6967656E742031343030
 SNMPv2-SMI::enterprises.935.1.1.1.3.2.1.0 (1.3.6.1.4.1.935.1.1.1.3.2.1.0): 1199
 Object Name: 1.3.6.1.4.1.935.1.1.1.3.2.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.3.2.1.0)
 Value (Integer32): 1199
 SNMPv2-SMI::enterprises.935.1.1.1.4.2.1.0 (1.3.6.1.4.1.935.1.1.1.4.2.1.0): 1211
 Object Name: 1.3.6.1.4.1.935.1.1.1.4.2.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.4.2.1.0)
 Value (Integer32): 1211
 SNMPv2-SMI::enterprises.935.1.1.1.4.2.3.0 (1.3.6.1.4.1.935.1.1.1.4.2.3.0): 0
 Object Name: 1.3.6.1.4.1.935.1.1.1.4.2.3.0 (SNMPv2-SMI::enterprises.935.1.1.1.4.2.3.0)
 Value (Integer32): 0
 SNMPv2-SMI::enterprises.935.1.1.1.2.2.3.0 (1.3.6.1.4.1.935.1.1.1.2.2.3.0): 20
 Object Name: 1.3.6.1.4.1.935.1.1.1.2.2.3.0 (SNMPv2-SMI::enterprises.935.1.1.1.2.2.3.0)
 Value (Integer32): 20
 SNMPv2-SMI::enterprises.935.1.1.1.3.2.4.0 (1.3.6.1.4.1.935.1.1.1.3.2.4.0): 600
 Object Name: 1.3.6.1.4.1.935.1.1.1.3.2.4.0 (SNMPv2-SMI::enterprises.935.1.1.1.3.2.4.0)
 Value (Integer32): 600
 SNMPv2-SMI::enterprises.935.1.1.1.2.1.1.0 (1.3.6.1.4.1.935.1.1.1.2.1.1.0): 2
 Object Name: 1.3.6.1.4.1.935.1.1.1.2.1.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.2.1.1.0)
 Value (Integer32): 2
 SNMPv2-SMI::enterprises.935.1.1.1.4.1.1.0 (1.3.6.1.4.1.935.1.1.1.4.1.1.0): 2
 Object Name: 1.3.6.1.4.1.935.1.1.1.4.1.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.4.1.1.0)
 Value (Integer32): 2
 SNMPv2-SMI::enterprises.935.1.1.1.2.2.2.0 (1.3.6.1.4.1.935.1.1.1.2.2.2.0): 538
 Object Name: 1.3.6.1.4.1.935.1.1.1.2.2.2.0 (SNMPv2-SMI::enterprises.935.1.1.1.2.2.2.0)
 Value (Integer32): 538
 SNMPv2-SMI::enterprises.935.1.1.1.2.2.1.0 (1.3.6.1.4.1.935.1.1.1.2.2.1.0): 100
 Object Name: 1.3.6.1.4.1.935.1.1.1.2.2.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.2.2.1.0)
 Value (Integer32): 100
 SNMPv2-SMI::enterprises.935.1.1.1.5.2.1.0 (1.3.6.1.4.1.935.1.1.1.5.2.1.0): 120
 Object Name: 1.3.6.1.4.1.935.1.1.1.5.2.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.5.2.1.0)
 Value (Integer32): 120
 SNMPv2-SMI::enterprises.935.1.1.1.1.2.1.0 (1.3.6.1.4.1.935.1.1.1.1.2.1.0): 322E3038
 Object Name: 1.3.6.1.4.1.935.1.1.1.1.2.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.1.2.1.0)
 Value (OctetString): 322E3038
 SNMPv2-SMI::enterprises.935.1.1.1.7.2.3.0 (1.3.6.1.4.1.935.1.1.1.7.2.3.0): 1
 Object Name: 1.3.6.1.4.1.935.1.1.1.7.2.3.0 (SNMPv2-SMI::enterprises.935.1.1.1.7.2.3.0)
 Value (Integer32): 1
 SNMPv2-SMI::enterprises.935.1.1.1.5.2.10.0 (1.3.6.1.4.1.935.1.1.1.5.2.10.0): 120
 Object Name: 1.3.6.1.4.1.935.1.1.1.5.2.10.0 (SNMPv2-SMI::enterprises.935.1.1.1.5.2.10.0)
 Value (Integer32): 120
 SNMPv2-SMI::enterprises.935.1.1.1.5.2.11.0 (1.3.6.1.4.1.935.1.1.1.5.2.11.0): 2
 Object Name: 1.3.6.1.4.1.935.1.1.1.5.2.11.0 (SNMPv2-SMI::enterprises.935.1.1.1.5.2.11.0)
 Value (Integer32): 2
 SNMPv2-SMI::enterprises.935.1.1.1.7.2.1.0 (1.3.6.1.4.1.935.1.1.1.7.2.1.0): 4
 Object Name: 1.3.6.1.4.1.935.1.1.1.7.2.1.0 (SNMPv2-SMI::enterprises.935.1.1.1.7.2.1.0)
 Value (Integer32): 4
 SNMPv2-SMI::enterprises.935.1.1.1.2.2.6.0 (1.3.6.1.4.1.935.1.1.1.2.2.6.0): 0
 Object Name: 1.3.6.1.4.1.935.1.1.1.2.2.6.0 (SNMPv2-SMI::enterprises.935.1.1.1.2.2.6.0)
 Value (Integer32): 0
 RFC1213-MIB::mib-2.33.1.9.2.0 (1.3.6.1.2.1.33.1.9.2.0): 600
 Object Name: 1.3.6.1.2.1.33.1.9.2.0 (RFC1213-MIB::mib-2.33.1.9.2.0)
 Value (Integer32): 60
 */
