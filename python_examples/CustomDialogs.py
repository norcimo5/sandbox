#!/usr/bin/env python

from Tkinter import *

# similar to tkSimpleDialog, but uses grid geometry manager
class GridDialog( Toplevel ):
    def __init__( self, parent, title = None ):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent

        self.node = None

        self.rowconfigure( 0, weight=1 )
        self.columnconfigure( 0, weight=1 )

        self.bodyframe = Frame( self )
        self.bodyframe.grid( row=0, column=0, sticky=NSEW )
        self.initial_focus = self.body( self.bodyframe )

        self.buttonboxframe = Frame( self )
        self.buttonboxframe.grid( row=1, column=0, sticky=NSEW )
        self.buttonbox( self.buttonboxframe )

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body( self, master ):
        return None

    def buttonbox( self, master ):

        w = Button( master, text="OK", width=10, command=self.ok, default=ACTIVE )
        w.grid( row=0, column=0 )
        w = Button( master, text="Cancel", width=10, command=self.cancel)
        w.grid( row=0, column=1 )
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def ok( self, event=None ):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel( self, event=None ):
        self.parent.focus_set()
        self.destroy()

    def validate( self ):
        # return True if entries are valid, otherwise ignore ok button click
        return True

    def apply( self ):
        # set the values you want and whoever created this dialog can check them
        pass

class ErrorDialog( GridDialog ):
    def __init__( self, parent, errormsg, title='Error' ):
        self.errormsg = errormsg
        GridDialog.__init__( self, parent, title )

    def body( self, master ):
        Label( master, text=self.errormsg ).grid()

    def buttonbox( self, master ):
        self.okbuttonimage = PhotoImage( file='icons/ok.gif' )
        self.okbutton = Button( master, text="OK", compound=LEFT, image=self.okbuttonimage, command=self.ok, default=ACTIVE )
        self.okbutton.grid( row=0, column=0 )
        self.bind("<Return>", self.ok)

class YesNoDialog( GridDialog ):
    def __init__( self, parent, message, title=None ):
        self.yes = False
        self.message = message
        GridDialog.__init__( self, parent, title )

    def body( self, master ):
        Label( master, text=self.message ).grid()

    def buttonbox( self, master ):
        self.okbuttonimage = PhotoImage( file='icons/ok.gif' )
        self.okbutton = Button( master, text="Yes", compound=LEFT, image=self.okbuttonimage, command=self.ok, default=ACTIVE )
        self.okbutton.grid( row=0, column=0 )
        self.cancelbuttonimage = PhotoImage( file='icons/cancel.gif' )
        self.cancelbutton = Button( master, text="No", compound=LEFT, image=self.cancelbuttonimage, command=self.cancel)
        self.cancelbutton.grid( row=0, column=1 )

    def validate( self ):
        return True

    def apply( self ):
        self.yes = True


def main( argc, argv ):

    root = Tk()
    dlg = GridDialog( root, "Example GridDialog" )

if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
