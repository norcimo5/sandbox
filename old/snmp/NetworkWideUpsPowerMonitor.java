package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import com.ticomgeo.smacks.shutdown.server.api.DefaultUPS;
import com.ticomgeo.smacks.shutdown.server.api.UPS;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

public class NetworkWideUpsPowerMonitor {

	private final static Logger logger = Logger.getLogger(NetworkWideUpsPowerMonitor.class.getName());
	private final List<UpsMonitor> upsMonitors = new ArrayList<UpsMonitor>();
	private String broadcastIpAddress;
	private int pollTimeSeconds;
	private int waitTimeMs = 5000;
	private boolean printToStdout = true;
	private File logDir;

	public NetworkWideUpsPowerMonitor(File logDir, String broadcastIpAddress, int pollTimeSeconds, boolean printToStdout) {
		this.broadcastIpAddress = broadcastIpAddress;
		this.pollTimeSeconds = pollTimeSeconds;
		this.logDir = logDir;
		this.printToStdout = printToStdout;
	}

	public NetworkWideUpsPowerMonitor() {
		String tmpDir = System.getProperty("java.io.tmpdir");
		this.logDir = new File(tmpDir);
		this.broadcastIpAddress = "192.168.255.255";
		this.pollTimeSeconds = 5;
	}

	public void stopMonitoring() throws IOException {
		for (UpsMonitor monitor : this.upsMonitors) {
			monitor.stopPolling();
		}
	}

	public void startMonitoring() throws IOException {
		boolean useBroadcast = true;
		// Find all UPSes on the network within 5 seconds
		Set<String> ipAddresses = new HashSet<String>();
		if (useBroadcast) {
			UpsDiscoverer discoverer = new UpsDiscoverer(getBroadcastIpAddress());
			discoverer.setWaitTimeMs(this.waitTimeMs);
			List<UPS> upses = discoverer.findOnceUsingBroadcast();
			// Make sure they are unique
			for (UPS ups : upses) {
				ipAddresses.add(ups.getIpAddress());
			}
		} else {
//			UpsDiscoverer discoverer = new UpsDiscoverer("192.168.0.1","192.168.23.254");
			UpsDiscoverer discoverer = new UpsDiscoverer("192.168.3.1", "192.168.3.254");
			discoverer.setPollTimeMs(10);

			discoverer.connect();
			discoverer.findUsingPolling();;
			ipAddresses = discoverer.getAddresses();
		}
		logger.info("Found UPSes at:" + Arrays.toString(ipAddresses.toArray()));
//		ipAddresses.add("192.168.3.1");
//		ipAddresses.add("192.168.3.129");
		String nov_ips[] = new String[]{
			"192.168.21.20",
			"192.168.21.21",
			"192.168.21.22",
			"192.168.21.23",
			"192.168.21.24",
			"192.168.21.25",
			"192.168.21.30",
			"192.168.21.31"
		};
		for(String ip: nov_ips) {
			ipAddresses.add(ip);
		}
		String sierra_ips[]=new String[] {"192.168.4.18", "192.168.4.17"};

		// Monitor the H&S of all discovered UPSes and log to file
		for (String ipAddress: ipAddresses) {
			logger.info("polling IP Address: " + ipAddress);
			UpsMonitor upsMonitor = new UpsMonitor(ipAddress, ipAddress, ipAddress, getPollTimeSeconds());
			upsMonitors.add(upsMonitor);
			try {
				UPS ups = new DefaultUPS(ipAddress, ipAddress);
				upsMonitor.addUpsListener(new LoggingUpsListener(ups, logDir, printToStdout));
				upsMonitor.connect();
			} catch (IOException e) {
				logger.log(Level.SEVERE, "UPS Monitor failed to connect for ipAddress = " + ipAddress, e);
				upsMonitors.remove(upsMonitor);
			}
		}
	}

	public String getBroadcastIpAddress() {
		return broadcastIpAddress;
	}

	public void setBroadcastIpAddress(String broadcastIpAddress) {
		this.broadcastIpAddress = broadcastIpAddress;
	}

	public int getPollTimeSeconds() {
		return pollTimeSeconds;
	}

	public void setPollTimeSeconds(int pollTimeSeconds) {
		this.pollTimeSeconds = pollTimeSeconds;
	}

	@SuppressWarnings({"null", "ConstantConditions"})
	public static void main(String args[]) throws Exception {
		NetworkWideUpsPowerMonitor monitor = null;
		if (args == null || args.length == 0) {
			monitor = new NetworkWideUpsPowerMonitor();
		} else if (args.length == 4) {
			File dir = new File(args[0]);
			String broadcastIpAddress = args[1];
			int pollingTimeSeconds = Integer.parseInt(args[2]);
			boolean printToStdout = Boolean.parseBoolean(args[3]);
			monitor = new NetworkWideUpsPowerMonitor(dir, broadcastIpAddress, pollingTimeSeconds, printToStdout);

		} else {
			System.out.println("Usage: " + NetworkWideUpsPowerMonitor.class.getName() + " loggingDirectory(TMPDIR) broadcastIpAddress(192.168.255.255) pollingTimeSeconds(5) printToStdout(true)");
			System.exit(1);
		}
		monitor.startMonitoring();
		Thread.sleep(1000 * 20 * 60);
		monitor.stopMonitoring();
	}
}