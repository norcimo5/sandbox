import java.io.*;
import java.net.*;

  new Thread () {
	  public void run () {
		  DatagramSocket serverSocket = new DatagramSocket(162);
		  byte[] receiveData = new byte[1024];
		  byte[] sendData = new byte[1024];
		  while(true)
		  {
			  DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
        try {
          serverSocket.setSoTimeout
			    serverSocket.receive(receivePacket);
        } catch (InterruptedIOException e) {
          System.err.println("Timeout!");
          buttonHWW.setBackground(Color.RED);
          continue;
        }

			  String sentence = new String( receivePacket.getData());
			  System.out.println(">>> HWW HEARTBEAT <<<");
        buttonHWW.setBackground(Color.GREEN);
			  System.out.println("RECEIVED: " + sentence);
			  InetAddress IPAddress = receivePacket.getAddress();
			  int port = receivePacket.getPort();
			  String capitalizedSentence = sentence.toUpperCase();
			  sendData = capitalizedSentence.getBytes();
			  DatagramPacket sendPacket =
					new DatagramPacket(sendData, sendData.length, IPAddress, port);
			  serverSocket.send(sendPacket);
		  }
	  }
  }
