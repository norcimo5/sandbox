#include <netdb.h>
#include <signal.h>
#include <time.h>

#include <iomanip>
#include <fstream>
#include <sstream>

#include <boost/regex.hpp>

#include <ll_util/numeric_utils.h>
#include <ll_util/string_utils.h>

#include <slog/slog_stream.h>

#include "MxgSigGen.h"
#include "MxgUtils.h"
#include "mxgSCPICmdStrings.h"
#include "snl_parse.h"
#include "RegexPredicate.h"
#include "tg_TimeConvert.h"

CalReturnStatus getSystemTime( timespec& gpsTime )
{ 
  CalReturnStatus ntpSynchronized = CAL_FAILURE;
  float ntpTolerance   = 0.1;
  float rootDispersion = 0.0;
  int stratum = 0;

  do {

      // Parse the output
      char buf[128] = { 0 };
      if( fgets( buf, sizeof(buf), fp ) == NULL ) {
        slog_err << "Ntp check failed fgets: " << strerror( errno ) << endl;
        break;
      }

      // Check the first line of output for success or error
      string output( buf );

      if( output.find( "Connection refused" ) != string::npos ) {
        slog_err << "The NTP service does NOT appear to be operational!" << endl;
        break;
      }

      if( output.find( "assID=" ) == string::npos ) {
        slog_err << "Ntp check provided unknown output: " << output << endl;
        break;
      }

      // Parse the status values we're interested in
      if( fscanf( fp, "stratum=%d, rootdispersion=%f\n", &stratum, &rootDispersion ) ==  0 ) {
        slog_err << "Ntp check failed fscanf: " << strerror( errno ) << endl;
        break;
      }

      slog_info << "NTP at stratum " << stratum << " within " << rootDispersion << " ms" << endl;

      // Validate if NTP is synchronized enough to perform collection
      double toleranceMs = ntpTolerance * 1e3;
      if( (stratum >= 10) || (rootDispersion >= toleranceMs) ) {
        slog_info << "NTP not capable of collection" << endl;
        break;
      }

      // get time
      timeval todTime;
      gettimeofday(&todTime, NULL);
      slog_debug << "System time: [ " << todTime.tv_sec << "." << todTime.tv_usec << " ]" << endl;

      // Adjust systime if it's between root dispertion 
      float tod_msec = (float)todTime.tv_usec / 1e3;
      if( (tod_msec <= rootDispersion) || (tod_msec >= (1e3 - rootDispersion )) ) {
        float adjustment = rootDispersion - tod_msec + ( (tod_msec > rootDispersion) * 1e3 );
        slog_info  << "Adjusting system time by waiting " << (adjustment) << "ms to compensate for root dispersion" << endl;
        usleep( (unsigned long)(adjustment * 1e3) );
        gettimeofday(&todTime, NULL);
        slog_debug << "Adjusted system time: [ " << todTime.tv_sec << "." << todTime.tv_usec << " ]" << endl;
      }

      gpsTime.tv_sec  = todTime.tv_sec;
      ntpSynchronized = CAL_SUCCESS;

    } while(false);

  return ntpSynchronized;
}
