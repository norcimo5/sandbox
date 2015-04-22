import java.io.File;
import javax.swing.JOptionPane;

public class JTest
{
   public static void main(String[] args)
   {

     File imageDriveLog = new File("./", "testfile.txt");
     if (imageDriveLog.exists()) {
        System.out.println("FILE EXISTS\n");
     } else {
        System.out.println("FILE DOES NOT EXIST!\n");
     } 
   }
}
