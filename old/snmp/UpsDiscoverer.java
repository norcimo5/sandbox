package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import com.ticomgeo.smacks.shutdown.server.api.DefaultUPS;
import com.ticomgeo.smacks.shutdown.server.api.UPS;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Timer;
import java.util.TimerTask;
import java.util.logging.Level;
import java.util.logging.Logger;

/*
 * http://www.serveradminblog.com/2011/02/neighbour-table-overflow-sysctl-conf-tunning/
 * http://stackoverflow.com/questions/1043567/java-ioexception-no-buffer-space-available-while-sending-udp-packets-on-linux
 * On Linux, may need to do this:
 *   sysctl -w net.ipv4.neigh.default.gc_thresh3=66000
 *   sysctl -w net.ipv4.neigh.default.gc_thresh2=8192
 *   sysctl -w net.ipv4.neigh.default.gc_thresh1=4096
 */
public class UpsDiscoverer {

	private final static Logger logger = Logger.getLogger(UpsDiscoverer.class.getName());
	List<UPS> availableUpses = new ArrayList<UPS>();
	private Set<String> addresses = Collections.synchronizedSet(new HashSet<String>());
	private Map<String, String> addressNames = Collections.synchronizedMap(new HashMap<String, String>());
	SNMPManager client = new SNMPManager();
	private boolean useBroadcast = false;
	private String beginAddress;
	private String endAddress;
	private String broadcastAddress;
	private int pollTimeMs = 30;
	private int waitTimeMs = 1000;
	private int pollRate = 30 * 60 * 1000;
	private Timer timer;
	private TimerTask timerTask = new TimerTask() {
		@Override
		public void run() {
			try {
				connect();
				if (isUseBroadcast()) {
					try {
						findUsingBroadcast();
						logger.log(Level.INFO, "{0} UPSes found", addresses.size());
						printUpsList();
					} catch (IOException ex) {
						logger.log(Level.SEVERE, null, ex);
						logger.warning("Exiting UPS Discovery");
						return;
					}
				} else {
					try {
						findUsingPolling();
					} catch (IOException ex) {
						logger.log(Level.SEVERE, null, ex);
						logger.log(Level.INFO, "{0} UPSes found", getAddressNames().size());
						logger.warning("Exiting UPS Discovery");
						printUpsMap();
						return;
					}
				}
			} catch (IOException ex) {
				logger.log(Level.SEVERE, "Error starting UPS Discoverer", ex);
			}
		}
	};

	public UpsDiscoverer() {
		this.useBroadcast = true;
	}

	public UpsDiscoverer(String broadcastAddress) {
		this.broadcastAddress = broadcastAddress;
		this.useBroadcast = true;
	}

	public UpsDiscoverer(String beginAddress, String endAddress) {
		this.useBroadcast = false;
		this.beginAddress = beginAddress;
		this.endAddress = endAddress;

	}

	public Map<String, String> getAddressNames() {
		return addressNames;
	}

	public void connect() throws IOException {
		if(!client.isStarted()) {
			client.start();
		}
	}

	public void start() throws IOException {
		if (this.timer != null) {
			this.timer.cancel();
		}
		this.timer = new Timer("UPS Discoverer Timer", true);
		//this.timer.scheduleAtFixedRate(timerTask,
		this.timer.scheduleAtFixedRate(timerTask, 1000, getPollRate());
	}

	public void stop() throws IOException {
		client.stop();
		if (this.timer != null) {
			this.timer.cancel();
		}
	}

	public List<UPS> getAvailableUpses() {
		return this.availableUpses;
	}

	public List<UPS> findOnceUsingBroadcast() throws IOException {
		this.connect();
		client.findAvailableUpsAddresses(getAddresses(), this.broadcastAddress, getWaitTimeMs());
		this.stop();
		List<UPS> upses = new ArrayList<UPS>();
		for (String address : this.addresses) {
			String ip = address;
			if (address.contains("/")) {
				String tokens[] = address.split("/");
				ip = tokens[0];
			}
			UPS ups = new DefaultUPS(ip, ip);
			upses.add(ups);
		}
		this.availableUpses.clear();
		this.availableUpses.addAll(upses);
		return upses;
	}

	public void findUsingBroadcast() throws IOException {
		client.findAvailableUpsAddresses(getAddresses(), this.broadcastAddress, getWaitTimeMs());
	}

	public void findUsingPolling() throws IOException {
		if (!this.client.isStarted()) {
			this.client.start();
		}
		client.findAvailableUpsAddresses(getAddressNames(), getBeginAddress(), getEndAddress(), getPollTimeMs());
		this.printUpsMap();
	}

	public int getPollTimeMs() {
		return pollTimeMs;
	}

	public void setPollTimeMs(int pollTimeMs) {
		this.pollTimeMs = pollTimeMs;
	}

	public int getWaitTimeMs() {
		return waitTimeMs;
	}

	public void setWaitTimeMs(int waitTimeMs) {
		this.waitTimeMs = waitTimeMs;
	}

	public boolean isUseBroadcast() {
		return useBroadcast;
	}

	public void setUseBroadcast(boolean useBroadcast) {
		this.useBroadcast = useBroadcast;
	}

	public String getBeginAddress() {
		return beginAddress;
	}

	public void setBeginAddress(String beginAddress) {
		this.beginAddress = beginAddress;
	}

	public String getEndAddress() {
		return endAddress;
	}

	public void setEndAddress(String endAddress) {
		this.endAddress = endAddress;
	}

	public Set<String> getAddresses() {
		return addresses;
	}

	public void printUpsList() {
		for (String ip : this.addresses) {
			System.out.println(ip);
		}
	}

	public void printUpsMap() {
		Set<String> addresses = this.getAddressNames().keySet();
		for (String address : addresses) {
			String name = this.getAddressNames().get(address);
			logger.log(Level.INFO, "IP Address{0}, Name = {1}", new Object[]{addresses, name});
		}
	}

	public int getPollRate() {
		return pollRate;
	}

	public void setPollRate(int pollRate) {
		this.pollRate = pollRate;
	}

	public static void main(String args[]) throws Exception {
		//UpsDiscoverer discoverer = new UpsDiscoverer("192.168.117.1", "192.168.117.255");
//		UpsDiscoverer discoverer = new UpsDiscoverer("192.168.127.255");
//		UpsDiscoverer discoverer = new UpsDiscoverer("192.168.4.255");
//		UpsDiscoverer discoverer = new UpsDiscoverer("255.255.255.255");
//		UpsDiscoverer discoverer = new UpsDiscoverer("192.168.1.1", "192.168.23.254");
//		UpsDiscoverer discoverer = new UpsDiscoverer("10.1.1.1", "10.1.1.254");
//		discoverer.setWaitTimeMs(1000);
//		discoverer.connect();
//		discoverer.findUsingPolling();
//		discoverer.findOnceUsingBroadcast();
//		discoverer.printUpsList();
		// MQL Lab 3: 192.168.207.9/161

		UpsDiscoverer discoverer = new UpsDiscoverer("192.168.207.1", "192.168.207.20");
		discoverer.setPollTimeMs(40);
		discoverer.setPollRate(60 * 1000);
		discoverer.start();
		Thread.sleep(60 * 1000 * 60);
	}
}