package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import java.io.IOException;

import org.snmp4j.CommandResponder;
import org.snmp4j.CommandResponderEvent;
import org.snmp4j.CommunityTarget;
import org.snmp4j.MessageDispatcher;
import org.snmp4j.MessageDispatcherImpl;
import org.snmp4j.PDU;
import org.snmp4j.Snmp;
import org.snmp4j.mp.MPv1;
import org.snmp4j.mp.MPv2c;
import org.snmp4j.mp.SnmpConstants;
import org.snmp4j.security.Priv3DES;
import org.snmp4j.security.SecurityProtocols;
import org.snmp4j.smi.OctetString;
import org.snmp4j.smi.TcpAddress;
import org.snmp4j.smi.TransportIpAddress;
import org.snmp4j.smi.UdpAddress;
import org.snmp4j.transport.AbstractTransportMapping;
import org.snmp4j.transport.DefaultTcpTransportMapping;
import org.snmp4j.transport.DefaultUdpTransportMapping;
import org.snmp4j.util.MultiThreadedMessageDispatcher;
import org.snmp4j.util.ThreadPool;
/**
 * @See http://shivasoft.in/blog/java/snmp/generating-trap-in-snmp-using-snmp4j/
 * iptables -I PREROUTING -t nat -i eth0 -p udp --dport 162 -j REDIRECT --to-port 10162 
 */
public class TrapReceiver implements CommandResponder {

	public static void main(String[] args) {
		TrapReceiver snmp4jTrapReceiver = new TrapReceiver();
		try {
//			snmp4jTrapReceiver.listen(new UdpAddress("192.168.0.190/161"));
//			snmp4jTrapReceiver.listen(new UdpAddress("localhost/161"));
			snmp4jTrapReceiver.listen(new UdpAddress("0.0.0.0/10162"));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Trap Listener
	 */
	public synchronized void listen(TransportIpAddress address)
	    throws IOException {
		AbstractTransportMapping transport;
		if (address instanceof TcpAddress) {
			transport = new DefaultTcpTransportMapping((TcpAddress) address);
		} else {
			transport = new DefaultUdpTransportMapping((UdpAddress) address);
		}

		ThreadPool threadPool = ThreadPool.create("DispatcherPool", 10);
		MessageDispatcher mDispathcher = new MultiThreadedMessageDispatcher(
		    threadPool, new MessageDispatcherImpl());

		// add message processing models
		mDispathcher.addMessageProcessingModel(new MPv1());
		mDispathcher.addMessageProcessingModel(new MPv2c());

		// add all security protocols
		SecurityProtocols.getInstance().addDefaultProtocols();
		SecurityProtocols.getInstance().addPrivacyProtocol(new Priv3DES());

		Snmp snmp = new Snmp(mDispathcher, transport);
		snmp.addCommandResponder(this);

		// Create Target
		CommunityTarget target = new CommunityTarget();
		target.setCommunity(new OctetString("public"));
		target.setVersion(SnmpConstants.version2c);
		UdpAddress remote=new UdpAddress("192.168.0.190/161");
		target.setAddress(remote);
		
//		PDU pdu = new PDU();
//		pdu.add(new VariableBinding(new OID(oid)));
//		pdu.setType(PDU.SET);
//		ResponseEvent response = snmp.getNext(pdu, target);

		transport.listen();
		System.out.println("Listening on " + address);

		try {
			this.wait();
		} catch (InterruptedException ex) {
			Thread.currentThread().interrupt();
		}
	}

	/**
	 * This method will be called whenever a pdu is received on the given port specified in the listen() method
	 */
	public synchronized void processPdu(CommandResponderEvent cmdRespEvent) {
		System.out.println("Received PDU...");
		PDU pdu = cmdRespEvent.getPDU();
		if (pdu != null) {
			System.out.println("Trap Type = " + pdu.getType());
			System.out.println("Variables = " + pdu.getVariableBindings());
		}
	}
}