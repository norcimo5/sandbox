package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

import com.ticomgeo.smacks.shutdown.server.api.UPS;
import com.ticomgeo.smacks.shutdown.server.api.UpsStatusEvent;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.util.logging.Level;
import java.util.logging.Logger;

public class LoggingUpsListener implements UpsMonitor.UpsListener {

	File logFile;
	BufferedWriter writer;
	UPS ups;
	static final Logger logger = Logger.getLogger(LoggingUpsListener.class.getName());
	boolean printToStdout = false;

	public LoggingUpsListener(UPS ups, File installDirectory) {
		this(ups, installDirectory, false);

	}

	public LoggingUpsListener(UPS ups, File installDirectory, boolean printToStdout) {
		this.printToStdout = printToStdout;
		this.ups = ups;
		String filename = "upslog-" + ups.getName() + "-" + ups.getIpAddress() + ".csv";
		try {
			try {
				File installDir = installDirectory;
				File logDir = new File(installDir, "log");
				logDir.mkdir();
				this.logFile = new File(logDir, filename);
			} catch (Exception e) {
				String tmpDir = System.getProperty("java.io.tmpdir");
				this.logFile = new File(tmpDir, filename);
			}
			logger.log(Level.INFO, "Logging UPS output to file: {0}", this.logFile);
			this.writer = new BufferedWriter(new FileWriter(logFile));
			StringWriter sw = new StringWriter();
			sw.append("IP Address|");
			sw.append("Timestamp|");
			sw.append("Time(ms)|");
			sw.append("Battery Status|");
			sw.append("Output Voltage Source|");
			sw.append("Estimated Minutes of Remaining Chart(min)|");
			sw.append("Estimated Percentage of Remaining Chart(min)|");
			sw.append("Temperature (C)|");
			sw.append("Input Voltage (Volts)|");
			sw.append("Output Voltage (Volts)|");
			sw.append("Output Power (Watts)|");
			sw.append("Output Percent Load|");
			sw.append("Input Current (Amps)|");
			sw.append("Output Current (Amps)|");
			sw.append("\n");
			writer.write(sw.toString());
			writer.flush();
			if (this.printToStdout) {
				System.out.println(sw);
			}
		} catch (Exception e) {
			logger.log(Level.SEVERE, "Error opening UPS log file: " + logFile, e);
		}
	}

	@Override
	public void received(UpsStatusEvent use) {
		try {
			StringWriter sw = new StringWriter();
			sw.append(ups.getIpAddress() + "|");
			sw.append(use.getTimestamp() + "|");
			sw.append(use.getTimestamp().getTime() + "|");
			sw.append(use.getBatteryStatus() + "|");
			sw.append(use.getOutputPowerSource() + "|");
			sw.append(use.getEstimatedMinutesOfRemainingCharge() + "|");
			sw.append(use.getEstimatedPercentageOfRemainingCharge() + "|");
			sw.append(use.getTemperatureCelsius() + "|");
			sw.append(use.getInputVoltage() + "|");
			sw.append(use.getOutputVoltage() + "|");
			sw.append(use.getOutputPowerWatts() + "|");
			sw.append(use.getOutputPercentLoad() + "|");
			sw.append(use.getInputCurrentAmps() + "|");
			sw.append(use.getOutputCurrentAmps() + "|");
			sw.append("\n");
			writer.write(sw.toString());
			writer.flush();
			if (this.printToStdout) {
				System.out.println(sw);
			}
		} catch (IOException ex) {
			logger.log(Level.SEVERE, null, ex);
		}
	}

	public void close() {
		try {
			writer.close();
		} catch (Exception ex) {
			logger.log(Level.SEVERE, null, ex);
		}
	}
}