import javax.swing.JOptionPane;
import java.net.InetAddress;
import java.net.UnknownHostException;

public class Dtest {
    public static String getAddress() {
        try {
            InetAddress addr = InetAddress.getLocalHost();
            return addr.getHostAddress();
        } catch (UnknownHostException e) {
            return "127.0.0.1";
        }   
    }

    public static void main(String[] args) {
        JOptionPane.showMessageDialog(null, Dtest.getAddress() , "Address", JOptionPane.WARNING_MESSAGE);
    }
}

