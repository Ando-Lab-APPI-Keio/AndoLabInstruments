from pymeasure.instruments import Instrument
from parse import parse
from enum import Enum
from pyvisa import constants

class Keithley2000(Instrument):
    def __init__(self, adapter, name="Keithley2000", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def initialize(self):
        self.write('*RST')
        return
    
    def error(self):
        self.write(':SYST:ERR?')
        return self.read()
    
    class Digits(Enum):
        _3H     = 4
        _4H     = 5
        _5H     = 6
        _6H     = 7
        DEFAULT = 'DEFault'
        MINIMUM = 'MINimum'
        MAXIMUM = 'MAXIMUM'
    
    class DigitalFilter(Enum):
        OFF                 = 0
        MOVING_FILTER       = 1
        REPEATING_FILTER    = 2
    
    class Reference(Enum):
        OFF     = 0
        SET     = 1
        ACQUIRE = 2

    def configure_DC_volts(self, resolution:Digits = Digits.DEFAULT, power_line_cycle:float = 1, enable_auto_range:bool = True, custom_range:float = 0, digital_filter:DigitalFilter = DigitalFilter.OFF, digital_filter_readings:int = 10, reference:Reference = Reference.OFF, reference_value:float = 0):
        self.write(":FUNC 'VOLT:DC';")

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def configure_AC_volts(self, resolution:Digits = Digits.DEFAULT, power_line_cycle:float = 1, enable_auto_range:bool = True, custom_range:float = 0, digital_filter:DigitalFilter = DigitalFilter.OFF, digital_filter_readings:int = 10, reference:Reference = Reference.OFF, reference_value:float = 0):
        self.write(":FUNC 'VOLT:AC';")

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def abort(self):
        self.write(':INIT:CONT OFF')
        self.write(':ABOR')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        
        return
    
    def init_trigger(self, continuous:bool = False):
        if(continuous):
            self.write(':INIT:CONT ON;')
        else:
            self.write(':INIT:CONT OFF;:INIT;')
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        return
    
    class TriggerSource(Enum):
        IMMEDIATE   = 0
        TIMER       = 1
        MANUAL      = 2
        BUS         = 3
        EXTERNAL    = 4
    
    class CountMode(Enum):
        INFINITE    = 0
        CUSTOM      = 1

    def configure_trigger(self, source:TriggerSource = TriggerSource.IMMEDIATE, timer_delay:float = 0.001, count_mode:CountMode = CountMode.INFINITE, custom_count:int = 1, enable_auto_delay:bool = True, delay:float = 0):

        self.abort()

        if(source == self.TriggerSource.IMMEDIATE):
            self.write(':TRIG:SOUR IMM')
        if(source == self.TriggerSource.TIMER):
            self.write(':TRIG:SOUR TIM;TIM ' + str(timer_delay))
        if(source == self.TriggerSource.MANUAL):
            self.write(':TRIG:SOUR MAN')
        if(source == self.TriggerSource.BUS):
            self.write(':TRIG:SOUR BUS')
        if(source == self.TriggerSource.EXTERNAL):
            self.write(':TRIG:SOUR EXT')
        
        if(count_mode == self.CountMode.INFINITE):
            self.write(':TRIG:COUN INF')
        if(count_mode == self.CountMode.CUSTOM):
            self.write(':TRIG:COUN ' + str(custom_count))
        
        if(enable_auto_delay):
            self.write(':TRIG:DEL:AUTO ON')
        else:
            self.write(':TRIG:DEL:AUTO OFF')
            self.write(':TRIG:DEL ' + str(delay))
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        
        return
    
    def initiate_measurement(self):
        self.write(':FORM ASC')
        self.write(':FORM:ELEM READ,UNIT,CHAN')
        self.write('INITiate')
        return
    
    class SOURCE(Enum):
        FUNCTION    =   0
        CALC1       =   1
        CALC2       =   2
        CALC3       =   3

    def read_single(self, source:SOURCE):
        self.write(':FORM ASC')
        self.write(':FORM:ELEM READ,UNIT,CHAN')
        self.wait_for_srq('*SRE 1;:STAT:MEAS:ENAB 32;*CLS;')
        if source == self.SOURCE.FUNCTION:
            self.write(':SENS:DATA?')
        if source == self.SOURCE.CALC1:
            self.write(':CALC1:DATA?')
        if source == self.SOURCE.CALC2:
            self.write(':CALC2:DATA?')
        if source == self.SOURCE.CALC3:
            self.write(':CALC3:LIM:FAIL?')
        data = self.read().strip()
        raw, channel = data.split(',')
        raw_voltage, strings = parse("{:f}{:S}", raw)
        voltage = float(str(raw_voltage) + strings[0:4])
        unit = strings[4:]

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        
        return voltage, unit, channel
    
    def wait_for_srq(self, command, timeout=25000):
        # Type of event we want to be notified about
        event_type = constants.EventType.service_request
        # Mechanism by which we want to be notified
        event_mech = constants.EventMechanism.queue
        self.adapter.connection.enable_event(event_type, event_mech)
        self.adapter.connection.discard_events(event_type, event_mech)
        self.write(command)
        # Wait for the event to occur
        self.adapter.connection.wait_for_srq(timeout)
        self.adapter.connection.enable_event(event_type, event_mech)
        self.adapter.connection.discard_events(event_type, event_mech)
        self.write('*SRE 48;')
        return
################################################
### Thermocouple settings
################################################
    class THERMOCOUPLE_TYPE(Enum):
            J   =   'J'
            K   =   'K'
            T   =   'T'
    
    class REFERENCE_JUNCTION_TYPE(Enum):
        SIMULATED   =   0
        REAL        =   1

    def configure_thermocouple(self, thermocouple_type:THERMOCOUPLE_TYPE, reference_junction_type:REFERENCE_JUNCTION_TYPE, simulated_temperature=23, temperature_coefficient=2E-4, voltage_offset=5.463E-2):
        self.write(':TEMP:TC:TYPE ' + thermocouple_type.value)
        if reference_junction_type == self.REFERENCE_JUNCTION_TYPE.SIMULATED:
            self.write(':TEMP:TC:RJUN:RSEL SIM')
            self.write(':TEMP:TC:RJUN:SIM ' + str(simulated_temperature))
        if reference_junction_type == self.REFERENCE_JUNCTION_TYPE.REAL:
            self.write(':TEMP:TC:RJUN:RSEL REAL')
            self.write(':TEMP:TC:RJUN:REAL:TCO ' + str(temperature_coefficient))
            self.write(':TEMP:TC:RJUN:REAL:OFFSET ' + str(voltage_offset))
        return
    class RESOLUTION(Enum):
        _3_5_Digits = 4
        _4_5_Digits = 5
        _5_5_Digits = 6
        _6_5_Digits = 7

    class TEMPERATURE_UNITS(Enum):
        CELSIUS     =   'C'
        FAHREHEIT   =   'F'
        KELVIN      =   'K'
    
    class DIGITAL_FILTER(Enum):
        OFF                 =   0
        MOVING_FILTER       =   1
        REPEATING_FILTER    =   2
    
    class REFERENCE_TYPE(Enum):
        OFF     =   0
        SET     =   1
        ACQUIRE =   2

    def configure_temperature(self, resolution:RESOLUTION, temperature_units:TEMPERATURE_UNITS, digital_filter_type:DIGITAL_FILTER, reference_type:REFERENCE_TYPE, reference_value=0, power_line_cycles=1.00, digital_filter_readings=10):
        self.write(":FUNC 'TEMP'")
        self.write(':TEMP:DIG ' + str(resolution.value))
        self.write(':UNIT:TEMP ' + temperature_units.value)
        self.write(':TEMP:NPLC ' + str(power_line_cycles))
        if digital_filter_type == self.DIGITAL_FILTER.OFF:
                self.write(':TEMP:AVER:STAT OFF')
        if digital_filter_type == self.DIGITAL_FILTER.MOVING_FILTER:
            self.write(':TEMP:AVER:TCON MOV')
            self.write('COUN ' + str(digital_filter_readings))
            self.write('STAT ON')
        if digital_filter_type == self.DIGITAL_FILTER.REPEATING_FILTER:
            self.write(':TEMP:AVER:TCON REP')
            self.write('COUN ' + str(digital_filter_readings))
            self.write('STAT ON')
        
        if reference_type == self.REFERENCE_TYPE.OFF:
            self.write(':TEMP:REF:STAT OFF')
        if reference_type ==  self.REFERENCE_TYPE.SET:
            self.write(':TEMP:REF ' + str(reference_value))
            self.write('REF:STAT ON')
        if reference_type ==  self.REFERENCE_TYPE.ACQUIRE:
            self.wait_for_srq('*SRE 1;:STAT:MEAS:ENAB 32;*CLS;')
            self.write(':TEMP:REF:STAT ON;:TEMP:REF:ACQ')
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        return

################################################
### TCscan settings
################################################
    def open_all_channel(self):
        self.write(':ROUTe:OPEN:ALL')
        return
    
    def close_single_channel(self, channel:int):
        self.write(':ROUTE:CLOSe (@%d)' % channel)
        return
