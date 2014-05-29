import java.io.*;       
public class WindowsUtils {     
     private WindowsUtils() { }
     private static final String WINDOWS_DESKTOP = "Desktop";
     public static String getWindowsCurrentUserDesktopPath() { //return the current user desktop path
         return System.getenv("userprofile") + "/" + WINDOWS_DESKTOP ;
     }
     public static void createInternetShortcutOnDesktop(String name, String target) throws IOException {
         String path = getWindowsCurrentUserDesktopPath() + "/"+ name + ".URL";
         createInternetShortcut(name, path, target, "");
     }
     public static void createInternetShortcutOnDesktop(String name, String target, String icon) throws IOException {
         String path = getWindowsCurrentUserDesktopPath() + "/"+ name + ".URL";
         createInternetShortcut(name, path, target, icon);
     }
     public static void createInternetShortcut(String name, String where, String target, String icon) throws IOException {
         FileWriter fw = new FileWriter(where);
         fw.write("[InternetShortcut]\n");
         fw.write("URL=" + target + "\n");
         if (!icon.equals("")) {
             fw.write("IconFile=" + icon + "\n");
         }
         fw.flush();
         fw.close();
     }
     public static void main(String[] args) throws IOException {
         WindowsUtils.createInternetShortcutOnDesktop("GOOGLE", "http://www.google.com/");
     }
}
