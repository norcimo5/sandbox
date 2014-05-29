// 3D non-perspective Convex,  Evgeny Demidov  8 Sep 2001
import java.awt.*;
import java.awt.event.*;
import java.util.StringTokenizer;
//import java.awt.image.*;
public class Convex3D extends java.applet.Applet
    implements MouseListener, MouseMotionListener {
  int nVert, nFace, h,w,h2,w2, mx0,my0, xPol[],yPol[];
  double fiX = .2, fiY = .3, dfi = .01, scale;
  int[][] face;
  double[][] vert, vert1, Norm;
  double[] Norm1z;
  Image buffImage;     Graphics buffGraphics;
  Color[] col;

public void init() {
  w = getSize().width;   h = getSize().height;
  w2 = w/2;  h2 = h/2;
  String s=getParameter("N");
  StringTokenizer st = new StringTokenizer(s);
  nVert = Integer.parseInt(st.nextToken());
  nFace = Integer.parseInt(st.nextToken());
  vert = new double[nVert][3];  vert1 = new double[nVert][2];
  s=getParameter("Vert");
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
  s=getParameter("Faces");
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
  s = getParameter("bgColor"); if (s != null){
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
   vert1[i][1] = m10*vert[i][0] + m11*vert[i][1] + m12*vert[i][2];}
  for (int i = 0; i < nFace; i++)
   Norm1z[i] = m20*Norm[i][0] + m21*Norm[i][1] + m22*Norm[i][2];
}

public void mouseMoved(MouseEvent e) {}

public void paint(Graphics g) {
  buffGraphics.clearRect(0, 0, w, h);
  for (int i = 0; i < nFace; i++){
   if (Norm1z[i] > 0){
    for (int j = 0; j < face[i].length; j++){
     xPol[j] = w2 + (int)vert1[face[i][j]][0];
     yPol[j] = h2 - (int)vert1[face[i][j]][1];}
    buffGraphics.setColor(col[(int)(Norm1z[i])]);
   buffGraphics.fillPolygon(xPol,yPol, face[i].length);}}
  g.drawImage(buffImage, 0, 0, this);
//  showStatus( "fiX=" + (int)(360*fiX) + "   fiY=" + (int)(360*fiY));
}
public void update(Graphics g)   {  paint(g);  }

}
