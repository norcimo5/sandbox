#!/usr/bin/env python2.7
################################################################################
# Name        : rfdu_adjuster.py                                               #
# Description : RFDU ADJUSTER                                                  #
################################################################################

################################################################################
# IMPORTS                                                                      #
################################################################################
import subprocess as sub
import os, sys, time, datetime
import signal, re, math
from optparse import OptionParser
from decimal import Decimal, getcontext
from xml.dom.minidom import parseString
from xml.dom.minidom import Document

################################################################################
# GLOBAL STRINGS                                                               #
################################################################################
DEFAULT_XML_FILE   = './AntennaProfiles.xml'
DEFAULT_TMP_FOLDER = '/tmp/rfdu.tmp'

################################################################################
# CLASS DEFINITIONS                                                            #
################################################################################
class rfdu:
    "RFDU Adjuster"
    def __init__(self):
        self.parser   = None
        self.options  = None
        self.args     = None
        self.myInit()
        self.xmlFile = DEFAULT_XML_FILE

    def __del__(self):
        #self.close()
        return

    ################################################################################        
    # getAntennaList()                                                             #
    # return a pointer to the xml dom object of the AntennaProfiles.xml file       #
    # and a list of antennas                                                       #
    ################################################################################        
    def getAntennaList(self):
        #Try and open the AntennaProfiles.xml file and parse the xml
        try: 
            #open the xml file for reading:
            file = open(self.xmlFile,'r')
            #convert to string:
            data = file.read()
            #close file because we dont need it anymore:
            file.close()
            #parse the xml from the file
            dom = parseString(data)
        except:
            print "\nCould not find the file: %s\nPlease Try again..." % self.xmlFile
            sys.exit(0)
    
        #if(debug):
        #Now rename the AntennaProfiles.xml file to AntennaProfiles.xml.orig
        #If a .orig exists, delete it
        try:
            if os.path.isfile(self.outputFile + '.orig'):
                os.remove(self.outputFile + '.orig')
            if os.path.isfile(self.outputFile):
                os.rename(self.outputFile, self.outputFile + '.orig') 
        except:
            print "Could not rename %s.\nVerify you have permission." % self.outputFile
            sys.exit(0)
    
        #Walk through the xml entries and find all the antennas defined
        #Also get the frequency range for each antenna
        more = True
        index = 0
        antenna = []
        antennaList = []
        while more == True:
            try:
                antenna = []
                xmlData = dom.getElementsByTagName('cs:Id')[index].firstChild.data
                antenna.append(xmlData.strip('\n\t'))
                xmlData = dom.getElementsByTagName('cs:MinFreqMHz')[index].firstChild.data
                antenna.append(xmlData.strip('\n\t'))
                xmlData = dom.getElementsByTagName('cs:MaxFreqMHz')[index].firstChild.data
                antenna.append(xmlData.strip('\n\t'))
                antennaList.append(antenna)
                index += 1
            except:
                more = False
        return dom,antennaList
    
    ################################################################################        
    # updateXmlFile(dom,antennaList,tolerance)                                     #
    ################################################################################        
    def updateXmlFile(self, dom,antennaList, tolerance = 0):
        ifPointer = ""
        xmlPointer = ""
        fpName = ""
        anum = 0
        id = ""
        con = [] 
        #Walk through the xml file and find the antennas and add
        #their index to the array
        more = True
        while more == True:
            try:
                ant = dom.getElementsByTagName('cs:AntennaProfile')[anum]
                #get the CalibrationsParams element and delete all entries it contains
                id = ant.getElementsByTagName('cs:Id')[0].firstChild.data
                for antenna in antennaList:
                    if antenna[0]  in id:
                        antenna.append(anum)
                anum += 1
            except:
                more = False
      
        #Now walk through the antenna list
        #1. Delete the existing data
        #2. Walk through the consolidated csv file in /tmp/naToAp
        #3. Add an entry for each value that changes based on the threshold input
        #4. Prettify the xml then write it back to the AntennaProfiles.xml file   
        for antenna in antennaList:
            #Get the records for this antenna
            #get the element for the requested AntennaID
            
            ant = dom.getElementsByTagName('cs:AntennaProfile')[antenna[3]]
            #get the CalibrationsParams element and delete all entries it contains
            #remove the connection element so we can write it back at the end of the cal values
            try:
                con = ant.getElementsByTagName('cs:Connections')[0]
                ant.removeChild(con)
            except:
                pass
            
            #First thing we want to do is to remove all the children under CalibrationParams 
            #cs:CalibrationParams node
            #ant.removeChild(cal)
            #print dom.toprettyxml(indent='  ')
    
            more = True
            while more == True:
                try:
                    cal = ant.getElementsByTagName('cs:CalibrationParams')[0]
                    ant.removeChild(cal)
                except:
                    more = False
    
            #Now we have an empty calibration element, walk through the csv file
            #and start reading values. Write the first one to the element
            #and then find the next value where the difference in delay is 
            #>= to the tolerance requested
            line = " "
            data = []
            row = []
    
            if antenna[0] != self.options.id:
                continue

            if self.args:
                fpName = self.args[0]
            else:    
                fpName = "./%s.csv"%(antenna[0])
    
            # if data does not exist to be inserted, continue
            if not os.path.isfile(fpName):
                print "Warning: %s file not found! Skipping ..." % fpName
                continue
            
            ifPointer = open(fpName,'r')
            
            #set lasty so that it always writes the first value
            lasty = 10000 * float(tolerance)
             
            #Read each line and store it in an array
            _digits = re.compile('^[0-9]')
            while line != "":
                line = ifPointer.readline()
                if "," in line and bool(_digits.search(line)):
                    x = float((line.split(","))[0])/1000000
                    lastreadx = x
                    y = float((line.split(","))[1])*1000000000 #convert to ns
                    lastready = y
                    row.append(x)
                    row.append(y)
                    if abs(y - lasty) >= tolerance:
                        data.append(row)
                        lasty = y
                    row = []
                    
            #append the last value in the file to the end of the array
            #so that it gets written to the file        
            row.append(lastreadx)
            row.append(lastready)
            data.append(row)
    
            #Read each entry in the data array and write it to the
            #cs:CalibrationParams element
            for row in data:
                newC = dom.createElement('cs:CalibrationParams')
                newF = dom.createElement('cs:FrequencyMHz')
                newT1 = dom.createTextNode(str(row[0]))
                newF.appendChild(newT1)
                newC.appendChild(newF)
                newD = dom.createElement('cs:DelayNanoSecs')
                newT2 = dom.createTextNode(str(row[1]))
                newD.appendChild(newT2)
                newC.appendChild(newD)
                #print newC.toprettyxml(indent='  ')
                ant.appendChild(newC)
            
            
            ant.appendChild(con)
           
            ifPointer.close()
            #end of loop per antenna
    
    
        #temporarily write out the data to a file
        #for some reason it still writes out too many blank lines
        #and puts everything on its own line.  So clean all this up
        uglyXml = dom.toprettyxml(indent='  ')
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
        xout = text_re.sub('>\g<1></', uglyXml)
    
        try: 
            #open the xml file for writing
            file = open(DEFAULT_TMP_FOLDER,'w')
            #write the new xml output
            file.write(xout)
            #close file 
            file.close()
        except:
            print "\nCould not write to the file: %s\nVerify you have permission and try again..."%"aptmp.tmp"
            sys.exit(0)
            
        #rewrite the file output to remove all extra \n lines  
        try: 
            #open the xml file for writing
            out = open(self.outputFile,'w')
            inf = open(DEFAULT_TMP_FOLDER,'r')
            line = inf.readline()
            while line != "":
                if len(line.strip("\t\n ")) != 0:
                    out.write(line)
                line = inf.readline()
            #close files
            inf.close()
            out.close()
        except:
            print "\nCould not write to the file: %s\nVerify you have permission and try again..." % self.xmlFile
            sys.exit(0)

    def myInit(self):
        self.parser = OptionParser()
        self.parser.add_option("--id", dest="id"     , type = "string", default = "ACQUISITION1" , help = "Antenna ID" )
        self.parser.add_option("-i"  , dest="inputFile", type = "string", default = DEFAULT_XML_FILE, help = "Alternate input filename for antenna profile"  )
        self.parser.add_option("-o"  , dest="outputFile" , type = "string", default = DEFAULT_XML_FILE, help = "Alternate output filename for antenna profile" )
        (self.options, self.args) = self.parser.parse_args() 
  
        self.id = self.options.id
        self.xmlFile    = self.options.inputFile
        self.outputFile = self.options.outputFile
        if len(self.args) == 0:
            print 'Invalid arguments!'
            self.parser.print_help()
            print
            sys.exit(1)
        
                
################################################################################
# MAIN                                                                         #
################################################################################
if __name__ == '__main__':

    session = rfdu()

    if session:
        ( dom, antennaList ) = session.getAntennaList()
        session.updateXmlFile( dom, antennaList )

    session = None

    sys.exit(0)

################################################################################
# EOF                                                                          #
################################################################################
