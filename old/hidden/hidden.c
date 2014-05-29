/*
*--------------------------------------------------*
*                                                  *
*       H_LINE.c Elimination de parties cachées    *
*                                                  *
*       Date : 30.03.87                            *
*       Patrick-Gilles MAILLOT                     *
*                                                  *
*                                                  *
*--------------------------------------------------*
*/

#include <math.h>
#include <stdio.h>


/*--------------------------------------*/
/*      C O N S T A N T S               */
/*--------------------------------------*/

#define  B_X  131 /* bit_map x dimension */
#define  B_Y  49  /* bit_map y dimension */
#define  B_I  '.' /* bit_map background color index */


#define         MAXV 100 /* maximum number of non-horizontal vertices */
#define  MAXI 100 /* maximum number of intersections */
#define         MAXF 100 /* maximum number of vertices in the z buffer */
#define  MAXL 16.0 /* maximum delta for color indexes */
#define  MAXS 10  /* maximum number of light sources */

/*--------------------------------------*/
/* D E F I N E D    S T R U C T U R E S */
/*--------------------------------------*/

struct f_bord {
    int tf0;  /* facet basic index */

    int tx0;
    int ty0;  /* facet border starting coordinates */
    int tz0;
    int idy;  /* true if start and end points are inverted */
    /* and also the index pointer of the next vector */
    int tx1;
    int ty1;  /* facet border ending coordinates */
    int tz1;

    int idx;  /* if 0, then the vertice is horizontal */
    int inx;
    int d0x;  /* Bresenham parameters for x's evolution */
    int d1x;
    int d2x;

    int idz;
    int inz;
    int d0z;  /* Bresenham parameters for z's evolution */
    int d1z;
    int d2z;

    float n_x;
    float n_y;  /* normalizased normal vector for vertices i and i+1 */
    float n_z;
};

struct z_vect {
    int tf0;  /* facet basic index */

    int tx0;
    int tz0;  /* z vertice starting coordinates */

    int tx1;  /* z vertice ending coordinate */

    int idz;
    int inz;
    int d0z;  /* Bresenham parameters for z's evolution */
    int d1z;
    int d2z;

    float n_x;
    float n_y;  /* normalizased normal vector at starting position */
    float n_z;

    float d_x;
    float d_y;  /* normalizased normal vector delta evolution */
    float d_z;
};

struct y_inte {
    int tf0;  /* facet basic index */
    int tx0;
    int tz0;  /* intersection coordinates at y = constant */

    float n_x;
    float n_y;  /* normalizased normal vector at the intersection */
    float n_z;
};

struct s_lite {
    int l_t;  /* 0: constant light; 1: ponctual light source */
    float l_i;  /* intensity factor between 0.0 and 1.0 */

    int l_x;
    int l_y;  /* source light position */
    int l_z;

    float d_x;
    float d_y;  /* normalizased normal vector at the intersection */
    float d_z;
};


/*--------------------------------------*/
/*      G L O B A L     D A T A S       */
/*--------------------------------------*/


char pixtab[B_X + 1][B_Y + 1]; /* pixel buffer ( the interactive display ) */

struct f_bord facets[MAXF];
int  fp, xp, yp, zp; /* current facet's values */
int  xb, yb, zb; /* save values of last begin_facet */
int  ymin, ymax; /* y boxing for all facets */
int  idf;  /* start index pointer for the current facet */
int  ip;  /* facet's index pointer in facets structure */
int  yh;  /* plane equation for intersections y and facets */

struct y_inte inters[MAXI];
int  it;  /* index pointer in inters structure */
int  kf, kx, kz; /* current intersection's values */
int  xmin, xmax; /* x boxing for all 'xz' vertices at y = constant */

struct z_vect zbuffr[MAXV];
int  ipp;  /* index pointer in zbuffr structure */

struct s_lite lights[MAXS];




/* structure initialization */

init()
{
    register int i,j;

    ip = 0;
    ymin =  32767;
    ymax = -32767;
    /* 'bit_map' initialization */
    for (i = 0; i < B_X + 1; i++)
        for (j = 0; j < B_Y + 1; j++) pixtab[i][j] = B_I;
}



/* begin facet procedure */

begin_facet(f,x,y,z)
int f,x,y,z;

{
    fp = f; /* set current values */
    xp = x;
    yp = y;
    zp = z;
    idf = ip; /* set current index = start index */
    xb = x; /* remember begin point */
    yb = y;
    zb = z;
    if (yp < ymin) ymin = yp; /* update y boxing */
    if (yp > ymax) ymax = yp;
}


/* end facet definition procedure */

end_facet()
{
    register int i, j, k;
    float  norm;
    float  n_x, n_y, n_z;
    float  p_x, p_y, p_z;
    float  g_x, g_y, g_z;

    draw_facet(xb,yb,zb);  /* draw a closing vertice */
    for (i = idf; i < ip ; i++) /* compute the vector of each vertice */
    {
        if ( facets[i].idy )
        {
            n_x = (float)(facets[i].tx0 - facets[i].tx1);
            n_y = (float)(facets[i].ty0 - facets[i].ty1);
            n_z = (float)(facets[i].tz0 - facets[i].tz1);
        }
        else
        {
            n_x = (float)(facets[i].tx1 - facets[i].tx0);
            n_y = (float)(facets[i].ty1 - facets[i].ty0);
            n_z = (float)(facets[i].tz1 - facets[i].tz0);
        }
        k = i - 1;
        if ( k < idf) k = ip - 1; /* k = previous point's index in facets' */
        if ( facets[k].idy )
        {
            p_x = (float)(facets[k].tx1 - facets[k].tx0);
            p_y = (float)(facets[k].ty1 - facets[k].ty0);
            p_z = (float)(facets[k].tz1 - facets[k].tz0);
        }
        else
        {
            p_x = (float)(facets[k].tx0 - facets[k].tx1);
            p_y = (float)(facets[k].ty0 - facets[k].ty1);
            p_z = (float)(facets[k].tz0 - facets[k].tz1);
        }
        g_x = n_y * p_z - n_z * p_y; /* compute the normal vector */
        g_y = n_x * p_z - n_z * p_x;
        g_z = n_x * p_y - n_y * p_x;
        norm = sqrt(g_x*g_x + g_y*g_y + g_z*g_z);
        facets[i].n_x = g_x / norm;  /* normalize the normal vector */
        facets[i].n_y = g_y / norm;
        facets[i].n_z = g_z / norm;
    }
    for (i = idf; i < ip ; i++) /* compute informations for each vertice */
    {
        j = i + 1;
        if ( j >= ip ) j = idf; /* next vertice index in facets' */
        facets[i].tz1 = j;  /* remember it for each vertice */
        facets[i].tx1 = facets[i].ty1 - facets[i].ty0;
    }    /* and also abs( delta_y ) */
}


/* facet border definition procedure */

draw_facet(x,y,z)
int x,y,z;
{

    register int dx, dy, dt, dz, iv;


    if (y != yp)
    {   /* test horizontal vertices */
        facets[ip].tf0 = fp; /* else update facets' structure */
        if (y < yp)
        {
            dx = xp-x;
            dy = yp-y;
            dz = zp-z;
            facets[ip].idy = 1; /* start-end points inversion */
            facets[ip].tx0 = x;
            facets[ip].ty0 = y;
            facets[ip].tz0 = z;
            facets[ip].tx1 = xp;
            facets[ip].ty1 = yp;
            facets[ip].tz1 = zp;
        }
        else
        {
            dx = x-xp;
            dy = y-yp;
            dz = z-zp;
            facets[ip].idy = 0; /* start and end points non inverted */
            facets[ip].tx0 = xp;
            facets[ip].ty0 = yp;
            facets[ip].tz0 = zp;
            facets[ip].tx1 = x;
            facets[ip].ty1 = y;
            facets[ip].tz1 = z;
        }
        if (dx < 0)   /* Bresenham parameters for x's evolution */
        {
            facets[ip].idx = -1;
            dx = -dx;
        }
        else
        {
            facets[ip].idx = 1;
        }
        dt = dy;
        if (dx < dy)
        {
            facets[ip].inx = 1;
            iv = dx;
            dx = dy;
            dy = iv;
        }
        else
        {
            facets[ip].inx = 0;
        }
        facets[ip].d0x = 2*dy-dx;
        facets[ip].d1x = 2*dy;
        facets[ip].d2x = 2*(dy-dx); /* done... */
        if (dz < 0)   /* Bresenham parameters for z's evolution */
        {
            facets[ip].idz = -1;
            dz= -dz;
        }
        else
        {
            facets[ip].idz = 1;
        }
        if (dz < dt)
        {
            facets[ip].inz = 1;
            iv = dz;
            dz = dt;
            dt = iv;
        }
        else
        {
            facets[ip].inz = 0;
        }
        facets[ip].d0z = 2*dt-dz;
        facets[ip].d1z = 2*dt;
        facets[ip].d2z = 2*(dt-dz); /* done... */
        yp = y;   /* update current values and y boxing */
        if(yp < ymin) ymin = yp;
        if(yp > ymax) ymax = yp;
    }
    else
    {   /* horizontal vertice case */
        facets[ip].idy = 0;  /* start and end points non inverted */
        facets[ip].tx0 = xp;
        facets[ip].ty0 = yp;
        facets[ip].tz0 = zp;
        facets[ip].tx1 = x;
        facets[ip].ty1 = y;
        facets[ip].tz1 = z;
        facets[ip].idx = 0;
    }
    ip++;    /* update pointer */
    xp = x;
    zp = z;
}



/* Intersection computation with the Y = yh plane */

intersect()
{

    register int i, j, iy;
    float r, s;

    it = 0;   /* initiate inters' index pointer */
    for (i = 0; i < ip; i++)
    {
        if (facets[i].idx != 0) /* eliminate the horizontal vertices */
        {
            if (facets[i].ty0 <= yh) /* is there an intersection */
            {   /* with the Y=yh plane ?    */
                if (facets[i].ty1 > yh)
                {   /* yes so the current x and z values are good */
                    inters[it].tf0 = facets[i].tf0;
                    inters[it].tx0 = facets[i].tx0;
                    inters[it].tz0 = facets[i].tz0;
                    j = facets[i].tz1; /* j is the next's vertice index in facets */
                    if ( facets[i].idy ) /* test the y's inversion flag */
                    {
                        s = (float)(facets[i].ty1 - facets[i].ty0) / facets[i].tx1;
                        r = 1. - s;  /* use parametric equation */
                    }
                    else
                    {
                        r = (float)(facets[i].ty1 - facets[i].ty0) / facets[i].tx1;
                        s = 1. - r;  /* use parametric equation */
                    }   /* compute the normal vector at this position */
                    inters[it].n_x = facets[i].n_x * r + facets[j].n_x * s;
                    inters[it].n_y = facets[i].n_y * r + facets[j].n_y * s;
                    inters[it].n_z = facets[i].n_z * r + facets[j].n_z * s;
                    it++;   /* update index pointer */
                    if (facets[i].inx) /* compute Bresenham evolution for x's */
                    {
                        if (facets[i].d0x < 0)
                        {
                            facets[i].d0x += facets[i].d1x;
                        }
                        else
                        {
                            facets[i].d0x += facets[i].d2x;
                            facets[i].tx0 += facets[i].idx;
                        }
                    }
                    else
                    {
                        iy = facets[i].ty0;
                        while (iy <= yh)
                        {
                            facets[i].tx0 += facets[i].idx;
                            if (facets[i].d0x < 0)
                            {
                                facets[i].d0x += facets[i].d1x;
                            }
                            else
                            {
                                facets[i].d0x += facets[i].d2x;
                                iy++;
                            }
                        }
                    }   /* done */
                    if (facets[i].inz) /* compute Bresenham evolution for z's */
                    {
                        if (facets[i].d0z < 0)
                        {
                            facets[i].d0z += facets[i].d1z;
                        }
                        else
                        {
                            facets[i].d0z += facets[i].d2z;
                            facets[i].tz0 += facets[i].idz;
                        }
                    }
                    else
                    {
                        iy = facets[i].ty0;
                        while (iy <= yh)
                        {
                            facets[i].tz0 += facets[i].idz;
                            if (facets[i].d0z < 0)
                            {
                                facets[i].d0z += facets[i].d1z;
                            }
                            else
                            {
                                facets[i].d0z += facets[i].d2z;
                                iy++;
                            }
                        }
                    }   /* done */
                    facets[i].ty0++;
                }
            }
        }
    }
}


/* Move routine to draw a vector in the z_buffer bit_map */

move_x(i)

int i;

{
    kx = inters[i].tx0;   /* update current values */
    kz = inters[i].tz0;
    kf = inters[i].tf0;
    if( kx < xmin ) xmin = kx;  /* update x boxing */
    if( kx > xmax ) xmax = kx;
}


/* Draw routine to draw a vector in the z_buffer bit_map */

draw_x(i)
int i;
{

    register int dx, dy, dz, lx, iv;


    lx = inters[i].tx0;
    if( lx != kx)
    {
        if( lx < kx)
        {   /* vertice inversion */
            dx = kx - lx;
            dz = kz - inters[i].tz0;
            zbuffr[ipp].tx0 = lx;
            zbuffr[ipp].tx1 = kx;
            zbuffr[ipp].tz0 = inters[i].tz0;
            zbuffr[ipp].n_x = inters[i-1].n_x; /* compute normal vector */
            zbuffr[ipp].n_y = inters[i-1].n_y; /* and evolution */
            zbuffr[ipp].n_z = inters[i-1].n_z;
            zbuffr[ipp].d_x = (inters[i].n_x - inters[i-1].n_x) / dx;
            zbuffr[ipp].d_y = (inters[i].n_y - inters[i-1].n_y) / dx;
            zbuffr[ipp].d_z = (inters[i].n_z - inters[i-1].n_z) / dx;
        }
        else
        {   /* non inverted vertice */
            dx = lx - kx;
            dz = inters[i].tz0 - kz;
            zbuffr[ipp].tx0 = kx;
            zbuffr[ipp].tx1 = lx;
            zbuffr[ipp].tz0 = kz;
            zbuffr[ipp].n_x = inters[i].n_x;  /* compute normal vector */
            zbuffr[ipp].n_y = inters[i].n_y;  /* and evolution */
            zbuffr[ipp].n_z = inters[i].n_z;
            zbuffr[ipp].d_x = (inters[i-1].n_x - inters[i].n_x) / dx;
            zbuffr[ipp].d_y = (inters[i-1].n_y - inters[i].n_y) / dx;
            zbuffr[ipp].d_z = (inters[i-1].n_z - inters[i].n_z) / dx;
        }
        if( dz < 0 )  /* compute Bresenham parameters */
        {
            zbuffr[ipp].idz = -1;
            dz = -dz;
        }
        else
        {
            zbuffr[ipp].idz = 1;
        }
        if( dz < dx)
        {
            iv = dz;
            dz = dx;
            dx = iv;
            zbuffr[ipp].inz = 1;
        }
        else
        {
            zbuffr[ipp].inz = 0;
        }
        zbuffr[ipp].tf0 = kf;
        zbuffr[ipp].d0z = 2 * dx - dz;
        zbuffr[ipp].d1z = 2 * dx;
        zbuffr[ipp].d2z = 2 * (dx - dz); /* done */
        ipp++;    /* update index pointer */
        kx = inters[i].tx0;   /* update coordinates */
        if( kx < xmin ) xmin = kx;  /* update x boxing */
        if( kx > xmax ) xmax = kx;
    }
    kz = inters[i].tz0;
}


/* rasterization procedure */


raster()
{
    register int x, i, zp, ind, il;
    float n_x, n_y, n_z;
    float d_x, d_y, d_z;
    float norm, lum, clg;


    for (x = xmin; x <= xmax; x++) /* for each value in the x boxing */
    {
        zp = -32767;   /* reset to background */
        ind = B_I;    /* reset color index to background */
        for (i = 0; i < ipp; i++)  /* compute x's intersection */
        {
            if (x >= zbuffr[i].tx0 && x <= zbuffr[i].tx1)
            {   /* there is an intersection ... */
                if (ind == B_I || zbuffr[i].tz0 > zp)
                {   /* z_buffer test */
                    zp  = zbuffr[i].tz0;  /* remember values */
                    ind = zbuffr[i].tf0;
                    n_x = zbuffr[i].n_x;
                    n_y = zbuffr[i].n_y;
                    n_z = zbuffr[i].n_z;
                }
                zbuffr[i].n_x += zbuffr[i].d_x; /* compute the normal vector */
                zbuffr[i].n_y += zbuffr[i].d_y; /* evolution */
                zbuffr[i].n_z += zbuffr[i].d_z;
                if (zbuffr[i].inz)  /* compute z evolution of the vertice */
                {
                    zbuffr[i].tx0++;
                    if (zbuffr[i].d0z <= 0)
                    {
                        zbuffr[i].d0z += zbuffr[i].d1z;
                    }
                    else
                    {
                        zbuffr[i].d0z += zbuffr[i].d2z;
                        zbuffr[i].tz0 += zbuffr[i].idz;
                    }
                }
                else
                {
                    while (zbuffr[i].tx0 < x)
                    {
                        zbuffr[i].tz0 += zbuffr[i].idz;
                        if (zbuffr[i].d0z <= 0)
                        {
                            zbuffr[i].d0z += zbuffr[i].d1z;
                        }
                        else
                        {
                            zbuffr[i].d0z += zbuffr[i].d2z;
                            zbuffr[i].tx0++;
                        }
                    }
                }    /* done */
            }
        }     /* update with the final color index */
        clg = 0.;
        for ( il = 0; il < MAXS; il++)
        {
            if (lights[il].l_t != -1)
            {
                if (lights[il].l_t == 0)
                {
                    d_x = lights[il].d_x;
                    d_y = lights[il].d_y;
                    d_z = lights[il].d_z;
                }
                else
                {
                    d_x = (float)( x - lights[il].l_x);
                    d_y = (float)(yh - lights[il].l_y);
                    d_z = (float)(zp - lights[il].l_z);
                    norm = sqrt(d_x*d_x + d_y*d_y + d_z*d_z);
                    d_x /= norm;
                    d_y /= norm;
                    d_z /= norm;
                }
                lum = (float)lights[il].l_i * (n_x*d_x + n_y*d_y + n_z*d_z);
                if ( lum < 0. ) lum = -lum;
                clg += lum;
            }
        }
        pixtab[x][yh] = ind + (int)(clg * MAXL);
    }
}


/* hidden line removal entry point */

elimin()
{

    register int i0;

    for (yh = ymin; yh < ymax; yh++)
    {   /* compute intersections with the Y=yh plane */
        intersect();
        if (it != 0)
        {   /* there are some intersections ... */
            ipp = 0;   /* reset index pointer */
            xmin = 32767;
            xmax = -32767;
            for (i0 = 0; i0 < it;) /* prepare zbuffr structure */
            {
                move_x(i0++);
                draw_x(i0++);
            }
            if (ipp != 0) raster(); /* compute each pixel */
        }
    }
}


/* interactive test program */

main()
{
    int it1, x, y, z, f, i0, i1;
    char c0, file_name[20];
    int l_x, l_y, l_z, type, lp;
    float norm;
    FILE *fp, *fopen();

    /* lights sources init */
    for (lp = 0; lp < MAXS; lp++) lights[lp].l_t = -1;
    init();
    it1 = 1;
    while (it1)
    {
        printf ("-> b)egin, c)lose, d)raw, e)limin, f)ile, l)ight, p)rint : ");
        scanf  ("%1s",&c0);
        switch (c0) {
        case 'b' :  /* begin facet */
            scanf  ("%d %d %d %d",&f,&x,&y,&z);
            begin_facet(f,x,y,z);
            break;
        case 'c' :  /* close facet */
            end_facet();
            break;
        case 'd' :  /* draw border */
            scanf  ("%d %d %d",&x,&y,&z);
            draw_facet(x,y,z);
            break;
        case 'e' :  /* hidden lines removal */
            elimin();
            break;
        case 'f' :  /* input from file */
            printf (" -> Enter file name : ");
            scanf  ("%s",file_name);
            if ((fp = fopen(file_name,"r")) == NULL)
            {
                printf ("-- error: can't find %s\n",file_name);
            }
            else
            {
                while ( fscanf (fp,"%1c",&c0) != EOF)
                {
                    switch (c0) {
                    case 'b' :  /*begin facet */
                        fscanf  (fp,"%d %d %d %d",&f,&x,&y,&z);
                        begin_facet(f,x,y,z);
                        break;
                    case 'c' :  /* close facet */
                        end_facet();
                        break;
                    case 'd' :  /* draw border */
                        fscanf  (fp,"%d %d %d",&x,&y,&z);
                        draw_facet(x,y,z);
                        break;
                    default :
                        break;
                    }
                }
                fclose(fp);
            }
            break;
        case 'l' :   /* light source position */
            printf(" -> Enter index, intensity, type, and position : ");
            scanf ("%d %f %d %d %d %d",&lp,&norm,&type,&l_x,&l_y,&l_z);
            lights[lp].l_i = norm;
            lights[lp].l_t = type;
            lights[lp].l_x = l_x;
            lights[lp].l_y = l_y;
            lights[lp].l_z = l_z;
            if( type == 0 )
            {
                norm = sqrt((float)(l_x*l_x) + (float)(l_y*l_y) + (float)(l_z*l_z));
                lights[lp].d_x  = (float) l_x / norm;
                lights[lp].d_y  = (float) l_y / norm;
                lights[lp].d_z  = (float) l_z / norm;
            }
            break;
        case 'p' :   /* display resulting picture */
            printf("    Enter file_name : ");
            scanf ("%s",file_name);
            if ((fp = fopen(file_name,"a")) == NULL)
            {
                printf("-- Error, can't open %s\n",file_name);
            }
            else
            {
                fprintf(fp,"   HIDDEN results :\n");
                for (i0 = B_Y; i0 >= 0; i0--)
                {
                    fprintf(fp,"%4d  ",i0);
                    for (i1 = 0; i1 < B_X; i1++)
                        fprintf(fp,"%c",pixtab[i1][i0]);
                    fprintf(fp,"\n");
                }
                fprintf(fp,"     ");
                for (i1 = 0; i1 < B_X; i1++)
                    fprintf(fp,"%c",(i1-(i1/10)*10 + '0'));
                fprintf(fp,"\n");
                fprintf(fp,"\n\nLights : i type intensity l_x l_y l_z d_x d_y d_z\n");
                for (lp = 0; lp < MAXS; lp++)
                {
                    if (lights[lp].l_t != -1)
                        fprintf(fp,"         %d   %d  %f  %d %d %d\n",lp,lights[lp].l_t,
                                lights[lp].l_i,
                                lights[lp].l_x, lights[lp].l_y, lights[lp].l_z);
                }
                fprintf(fp,"\f");
                close(fp);
            }
            init();
            break;
        default :
            break;
        }
    }
}
