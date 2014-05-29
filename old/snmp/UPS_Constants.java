package com.ticomgeo.smacks.shutdown.server.protocol.snmp;

public interface UPS_Constants {
	public static final String TIME_REMAINING_OID = "1.3.6.1.2.1.33.1.2.3.0";
	public static final String MANUFACTURER_OID = "1.3.6.1.2.1.33.1.1.1.0";
	public static final String MODEL_OID = "1.3.6.1.2.1.33.1.1.2.0";
	public static final String OUTPUT_POWER_SOURCE_OID = "1.3.6.1.2.1.33.1.4.1.0";
	public static final String STD_INPUT_VOLTAGE = "1.3.6.1.2.1.33.1.3.3.1.3";
	public static final String STD_OUTPUT_VOLTAGE = "1.3.6.1.2.1.33.1.4.4.1.2";
	public static final String STD_TEMPERATURE_CELSIUS = "1.3.6.1.2.1.33.1.2.7.0";
	public static final String NON_STD_INPUT_VOLTAGE = "1.3.6.1.4.1.935.1.1.1.3.2.1.0";
	public static final String NON_STD_OUTPUT_VOLTAGE = "1.3.6.1.4.1.935.1.1.1.4.2.1.0";
	public static final String NON_STD_TEMPERATURE_CELSIUS = "1.3.6.1.4.1.935.1.1.1.2.2.3.0";
	public static final String ESTIMATED_PERCENTAGE_CHARGE_REMAINING = "1.3.6.1.2.1.33.1.2.4.0";
	public static final String STD_INPUT_CURRENT_OID = "1.3.6.1.2.1.33.1.3.3.1.4";
	public static final String STD_OUTPUT_CURRENT_OID = "1.3.6.1.2.1.33.1.4.4.1.3";
	public static final String STD_OUTPUT_POWER_OID = "1.3.6.1.2.1.33.1.4.4.1.4";
	public static final String STD_OUTPUT_PERCENT_LOAD_OID = "1.3.6.1.2.1.33.1.4.4.1.5";
	public static final String NON_STD_OUTPUT_PERCENT_LOAD_OID = "1.3.6.1.4.1.935.1.1.1.4.2.3.0";
	public static final String SYSTEM_CONTACT =  "1.3.6.1.2.1.1.4.0";
	public static final String SYSTEM_NAME     = "1.3.6.1.2.1.1.5.0";
	public static final String SYSTEM_LOCATION = "1.3.6.1.2.1.1.6.0";
}