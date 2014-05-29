import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Properties;
 
public class PropertiesXMLExample
{
      public static void main(String[] args) throws IOException
            { 
                    Properties props = new Properties();
                          props.setProperty("email.support", "donot-spam-me@nospam.com");
                           
                                //where to store?
                                OutputStream os = new FileOutputStream("./email-configuration.xml");
                                 
                                      //store the properties detail into a pre-defined XML file
                                      props.storeToXML(os, "Support Email","UTF-8");
                                       
                                            System.out.println("Done");
                                                }
}
