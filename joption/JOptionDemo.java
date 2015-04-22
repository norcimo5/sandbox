import javax.swing.JOptionPane;

public class JOptionDemo
{
   public static void main(String[] args)
   {
      String fullName = " ";
      String strAge = " ";
      
      int age = 0;
      
      fullName = JOptionPane.showInputDialog(null, "Enter your full name: ");
      
      JOptionPane.showMessageDialog(null, "Your full name is " + fullName);
      
      strAge = JOptionPane.showInputDialog(null, " Enter your age: ");
      
      age = Integer.parseInt(strAge);
      
      JOptionPane.showConfirmDialog(null, age, "Is this your real age?",
            JOptionPane.OK_CANCEL_OPTION);
      
      JOptionPane.showMessageDialog(null, "Your age is " + age + ".");         
   }
}
