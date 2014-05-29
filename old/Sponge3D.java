// 3D non-perspective fractal Sponges,  Evgeny Demidov  10 Oct 2001
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.util.StringTokenizer;

public class Sponge3D extends Frame implements WindowListener, MouseListener, MouseMotionListener {
  int nVert, nFace, it, h,w,h2,w2, mx0,my0, xPol[],yPol[], Zsort[];
  double fiX = .2, fiY = .3, dfi = .01, scale, scl;
  int[][] face;
  double[][] vert, vert1, Norm;
  double[] Norm1z;
  Image buffImage;     Graphics buffGraphics;
  Color[] col;
  boolean painted;

   /**
    * 
    */
   private static final long serialVersionUID = 1L;
   public static void main(String[] args) {
     java.awt.EventQueue.invokeLater(new Runnable() {
       @Override
       public void run() {
         new Sponge3D();
       }
     });
   }

public Sponge3D() {
  this.setSize(320, 320);
  this.setVisible(true);
  this.setLayout(new FlowLayout());
  this.addWindowListener(this);

  System.setProperty("par", "3 3");
  System.setProperty("N", "8 6");
  System.setProperty("Vert",
    "1 1 1, 1 1 -1, -1 1 -1, -1 1 1, 1 -1 1, 1 -1 -1, -1 -1 -1, -1 -1 1");
  System.setProperty("Faces",
    "0 1 2 3 -1 7 6 5 4 -1 0 4 5 1 -1 5 6 2 1 -1 6 7 3 2 -1 0 3 7 4 -1");
  System.setProperty("bgColor", "100 100 255");

  w = getSize().width;   h = getSize().height;
  w2 = w/2;  h2 = h/2;
  String s=System.getProperty("par");
  StringTokenizer st = new StringTokenizer(s);
  it = Integer.parseInt(st.nextToken());
  scl = Double.valueOf(st.nextToken()).doubleValue();
  s=System.getProperty("N");  st = new StringTokenizer(s);
  nVert = Integer.parseInt(st.nextToken());
  nFace = Integer.parseInt(st.nextToken());
  vert = new double[nVert][3];  vert1 = new double[nVert][3];
  s=System.getProperty("Vert");
  st = new StringTokenizer(s, " ,");
  double max = 0;
  for (int i = 0; i < nVert; i++){
   vert[i][0] = Double.valueOf(st.nextToken()).doubleValue();
   vert[i][1] = Double.valueOf(st.nextToken()).doubleValue();
   vert[i][2] = Double.valueOf(st.nextToken()).doubleValue();
   double vv = vert[i][0]*vert[i][0] + vert[i][1]* vert[i][1] +
    vert[i][2]* vert[i][2];
   if ( max < vv) max = vv;}
  scale = w2 / Math.sqrt(max);
  face = new int[nFace][];
  int tmp[] = new int[30];
  Zsort = new int[nVert];
  for (int i = 0; i < nVert; i++) Zsort[i] = i;
  s=System.getProperty("Faces");
  st = new StringTokenizer(s);
  for (int i = 0; i < nFace; i++){
   int l = 0;
   while ( (tmp[l]=Integer.parseInt(st.nextToken())) != -1) l++;
   face[i] = new int[l];
   for (int j = 0; j < l; j++) face[i][j] = tmp[j];}
  buffImage = createImage(w, h);   buffGraphics = buffImage.getGraphics();
  col = new Color[256];
  Norm = new double[nFace][3];  Norm1z = new double[nFace];
  for (int i = 0; i < nFace; i++){
   Norm[i][0] = (vert[face[i][1]][1] - vert[face[i][0]][1])*
    (vert[face[i][2]][2] - vert[face[i][1]][2]) -
    (vert[face[i][2]][1] - vert[face[i][1]][1])*
    (vert[face[i][1]][2] - vert[face[i][0]][2]);
   Norm[i][1] = -(vert[face[i][1]][0] - vert[face[i][0]][0])*
    (vert[face[i][2]][2] - vert[face[i][1]][2]) +
    (vert[face[i][2]][0] - vert[face[i][1]][0])*
    (vert[face[i][1]][2] - vert[face[i][0]][2]);
   Norm[i][2] = (vert[face[i][1]][0] - vert[face[i][0]][0])*
    (vert[face[i][2]][1] - vert[face[i][1]][1]) -
    (vert[face[i][2]][0] - vert[face[i][1]][0])*
    (vert[face[i][1]][1] - vert[face[i][0]][1]);
   double mod = Math.sqrt(Norm[i][0]*Norm[i][0] + Norm[i][1]*Norm[i][1] +
    Norm[i][2]*Norm[i][2]) / 255.5;
   Norm[i][0] /= mod;    Norm[i][1] /= mod;    Norm[i][2] /= mod;}
  xPol = new int[30];  yPol = new int[30];
  for (int i = 0; i < 256; i++) col[i] = new Color(i, i, i);
  s = System.getProperty("bgColor"); if (s != null){
   st = new StringTokenizer(s);
   int red = Integer.parseInt(st.nextToken());
   int green = Integer.parseInt(st.nextToken());
   int blue = Integer.parseInt(st.nextToken());
   setBackground( new Color(red, green, blue));}
  else setBackground(new Color(255,255,255));
  addMouseListener(this);
  addMouseMotionListener(this);
  rotate();
}
public void destroy() {
  removeMouseListener(this);
  removeMouseMotionListener(this);
}
public void mouseClicked(MouseEvent e){}       // event handling
public void mousePressed(MouseEvent e) {
  mx0 = e.getX();  my0 = e.getY();
  if ( e.isControlDown() ) {
    it--;  if (it < 0) it = 0;
    painted = false;
    repaint();}
  if ( e.isAltDown() ){
    it++;
    painted = false;
    repaint();}
  e.consume();
}
public void mouseReleased(MouseEvent e){}
public void mouseEntered(MouseEvent e) {}
public void mouseExited(MouseEvent e)  {}
public void mouseDragged(MouseEvent e) {
  int x1 = e.getX();  int y1 = e.getY();
  fiY += dfi*(x1 - mx0);   mx0 = x1;
  fiX += dfi*(y1 - my0);   my0 = y1;
  rotate();
  repaint();
  e.consume();
}

public void rotate(){
  double ct = Math.cos(fiX), cf = Math.cos(fiY),
         st = Math.sin(fiX), sf = Math.sin(fiY),
         m00 =  scale*cf,    m02 =  scale*sf,
         m10 = scale*st*sf, m11 =  scale*ct, m12 = -scale*st*cf,
         m20 = -ct*sf, m21 = st, m22 = ct*cf;
  for (int i = 0; i < nVert; i++){
   vert1[i][0] = m00*vert[i][0] + m02*vert[i][2];
   vert1[i][1] = m10*vert[i][0] + m11*vert[i][1] + m12*vert[i][2];
   vert1[i][2] = m20*vert[i][0] + m21*vert[i][1] + m22*vert[i][2];}
  for (int i = 0; i < nFace; i++)
   Norm1z[i] = m20*Norm[i][0] + m21*Norm[i][1] + m22*Norm[i][2];

  for (int i = nVert - 1; --i >= 0;) {
    boolean flipped = false;
    for (int j = 0; j <= i; j++) {
      int a = Zsort[j],  b = Zsort[j + 1];
      if (vert1[a][2] > vert1[b][2]) {
        Zsort[j + 1] = a;   Zsort[j] = b;
        flipped = true;
      }
    }
    if (!flipped) break;
  }
  painted = false;
}

public void mouseMoved(MouseEvent e) {}

public void paint(Graphics g) {
  if ( !painted ){
   buffGraphics.clearRect(0, 0, w, h);
   recursion(it, 0, 0, 1, 1-1/scl);
   painted = true;}
  g.drawImage(buffImage, 0, 0, this);
}

public void recursion(int n, double Xo, double Yo, double sc, double tr) {
  if (n == 0) drawPolygon(Xo, Yo, sc);
  else{
   for (int i = 0; i < nVert; i++){
    int is = Zsort[i];
    recursion(n-1, Xo + vert1[is][0]*tr, Yo + vert1[is][1]*tr, sc/scl, tr/scl);}}
}                         

public void drawPolygon(double Xo, double Yo, double sc) {
  for (int i = 0; i < nFace; i++){
   if (Norm1z[i] > 0){
    for (int j = 0; j < face[i].length; j++){
     xPol[j] = w2 + (int)(Xo + vert1[face[i][j]][0]*sc);
     yPol[j] = h2 - (int)(Yo + vert1[face[i][j]][1]*sc);}
   buffGraphics.setColor(col[(int)(Norm1z[i])]);
   buffGraphics.fillPolygon(xPol,yPol, face[i].length);
   buffGraphics.setColor(Color.black);
   buffGraphics.drawPolygon(xPol,yPol, face[i].length);}}
}

  @Override
    public void update(Graphics g) {
          paint(g);
            }

  @Override
    public void windowActivated(WindowEvent e) {
        }

  @Override
    public void windowClosed(WindowEvent e) {
        }

  @Override
    public void windowClosing(WindowEvent e) {
          dispose();
              System.exit(0);
                }

  @Override
    public void windowDeactivated(WindowEvent e) {
        }

  @Override
    public void windowDeiconified(WindowEvent e) {
        }

  @Override
    public void windowIconified(WindowEvent e) {
        }

  @Override
    public void windowOpened(WindowEvent e) {
        }

}
