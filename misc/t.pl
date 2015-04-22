#!/usr/bin/perl

my $MYFILE;

print "[ CREATING FILE ]\n";

open( $MYFILE, '>', "./test.txt" ) or
  die "Unable to open filename : $!";

close($MYFILE);

print "[ DONE ]\n";
