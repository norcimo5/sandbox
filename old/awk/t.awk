BEGIN { 
    FS=",";
}
{
    printf("dn: cn=%s %s,mail=%s@ticom-geo.com\n", $1, $2, $3);
    printf("objectclass: top\n");
    printf("objectclass: person\n");
    printf("objectclass: organizationalPerson\n");
    printf("objectclass: inetOrgPerson\n");
    printf("objectclass: mozillaAbPersonAlpha\n");
    printf("givenName: %s\n", $1);
    printf("sn: %s\n", $2);
    printf("cn: %s %s\n", $1, $2);
    printf("mail: %s@ticom-geo.com\n", $3);
    printf("modifytimestamp: 0\n\n");
}

END { }
