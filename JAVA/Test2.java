import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
 
/** Establish a SSL connection to a host and port, writes a byte and
  * prints the response. See
  * http://confluence.atlassian.com/display/JIRA/Connecting+to+SSL+services
  */
public class Test2 {

static String[] s = {"file.encoding",
"file.encoding.pkg",
"file.separator",
"java.class.path",
"java.class.version",
"java.compiler",
"java.home",
"java.io.tmpdir",
"java.version",
"java.vendor",
"java.vendor.url",
"line.separator",
"os.name",
"os.arch",
"os.version",
"path.separator",
"user.dir",
"user.home",
"user.language",
"user.name",
"user.region",
"user.timezone"};

  public static void main(String[] args) {
    for(String x : s)
      System.out.println(Test2.class.getProtectionDomain().getCodeSource().getLocation().getPath());
    try {
      Thread.sleep(2000);
    } catch(InterruptedException e) {
    } 
  }
}
