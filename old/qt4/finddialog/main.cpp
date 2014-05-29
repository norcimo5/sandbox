#include <QApplication>
#include "finddialog.h"

int main(int argc, char *argv[])
{
  int i = 0;
  QApplication app(argc, argv);
  FindDialog *dialog = new FindDialog;
  dialog->show();
  return app.exec(); 
}
