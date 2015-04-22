#!/usr/bin/env python

from Tkinter import *
from sets import Set

class SelectionControlListbox( Listbox ):
    def __init__( self, parent=None, eventhandler=None, **kwargs ):
        Listbox.__init__( self, parent, selectmode=SINGLE, **kwargs )
        self.bind( '<Button-1>', self.onButton1Click )
        self.bindtags( self.bindtags()[1:]+self.bindtags()[0:1] )
        self.idx = None
        self.eventhandler = eventhandler
        self.disabled_indices = Set()

    def disable( self, idx ):
        self.itemconfig( idx, foreground='gray', selectbackground='light gray' )
        self.disabled_indices.add( idx )

    def enable( self, idx ):
        self.itemconfig( idx, foreground='', selectbackground='' )

    def onButton1Click( self, event ):
        sel = self.curselection()
        if sel:
            if self.itemcget( int( sel[0] ), 'foreground' ) == 'gray':
                self.selection_clear( 0, END )
                if self.idx is not None:
                    self.selection_set( self.idx )
            else:
                self.idx = int( sel[0] )
                if self.eventhandler is not None:
                    self.eventhandler( self.idx )

class AutoScrollbar(Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
             self.grid_remove()
        else:
            self.grid()

        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"

class ExtendedOptionMenu( OptionMenu ):
    def __init__(self, master, variable, value, *values, **kwargs):
        OptionMenu.__init__( self, master, variable, value, *values, **kwargs )
        self.values = tuple( [ value ] + list( values ) )
        self.textvariable = variable

    def get( self ):
        return self.textvariable.get()

    def get_values( self ):
        return self.values

    def set( self, text ):
        self.textvariable.set( text )

class ToolTip( object ):

    def __init__( self, widget ):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip( self, text ):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox( "insert" )
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel( self.widget )
        tw.wm_overrideredirect( 1 )
        tw.wm_geometry( "+%d+%d" % (x, y) )
        label = Label( tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1 )
#                      font=("tahoma", "8", "normal"))
        label.pack( ipadx=1 )

    def hidetip( self ):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip( widget, text ):
    toolTip = ToolTip( widget )
    def enter( event ):
        toolTip.showtip( text )
    def leave( event ):
        toolTip.hidetip()

    widget.bind( '<Enter>', enter )
    widget.bind( '<Leave>', leave )


def main( argc, argv ):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
