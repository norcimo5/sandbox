import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;


public class SocketTest {
	
	public static void main(String[] args){
	ServerSocket serverSocket = null;
	
	// Gets the socket's input and output stream and opens readers and writers on them.
	try {
	      serverSocket = new ServerSocket(162);
	} 
	catch (IOException e) {
	      System.out.println("Could not listen on port: 162");
	          System.exit(-1);
	}

	// Initiates communication with the client by writing to the socket (shown in bold).
	Socket clientSocket = null;
	try {
	      clientSocket = serverSocket.accept();
	} 
	catch (IOException e) {
	      System.out.println("Accept failed: 162");
	          System.exit(-1);
	}

	// Communicates with the client by reading from and writing to the socket (the while loop).
//	PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
//	BufferedReader in = 
//	    new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
//	    String inputLine, outputLine;
//
//	    // initiate conversation with client
//	    KnockKnockProtocol kkp = new KnockKnockProtocol();
//	    outputLine = kkp.processInput(null);
//	    out.println(outputLine);
//
//	    while ((inputLine = in.readLine()) != null) {   
//	          outputLine = kkp.processInput(inputLine);
//	          out.println(outputLine);
//	          if (outputLine.equals("Bye."))
//	              break;
//	    }


	// CLOSE AND EXIT
//	out.close();
//	in.close();
	try {
		clientSocket.close();
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	try {
		serverSocket.close();
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}

}
}