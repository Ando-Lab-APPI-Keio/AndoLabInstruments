from pymeasure.instruments import Instrument
from enum import Enum

class LI5640(Instrument):
    def __init__(self, adapter, name="LI5640", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
        return
    
    def initialize(self):
        self.write('*RST')
        return
    def error(self):
        self.write('EROR?')
        return self.read()
    ################################################################
    ## input setings
    ################################################################
    class INPUT_COUPLING(Enum):
        AC = 0
        DC = 1

    def coupling(self, read:bool, coupling:INPUT_COUPLING):
        if(read):
            self.write('ICPL?')
            return str.strip(self.read())
        else:
            self.write('ICPL ' + str(coupling.value))
            return
    
    class INPUT_GROUNDING(Enum):
        FLOAT   = 0
        GROUND  = 1

    def ground(self, read:bool, ground:INPUT_GROUNDING):
        if(read):
            self.write('IGND?')
            return str.strip(self.read())
        else:
            self.write('IGND ' + str(ground.value))
            return
    
    class SIGNAL_INPUT(Enum):
        A   = 0
        AB  = 1
        I6  = 2
        I8  = 3

    def signal_input(self, read:bool, input:SIGNAL_INPUT):
        if(read):
            self.write('ISRC?')
            return str.strip(self.read())
        else:
            self.write('ISRC ' + str(input.value))
            return
    ################################################################
    ## filter settings
    ################################################################
    class LINE_FILTER(Enum):
        THROUGH         = 0
        LINE            = 1
        LINE2           = 2
        LINE_AND_LINE2  = 3

    class LINE_FREQ(Enum):
        _50Hz   = 0
        _60Hz   = 1

    def line_filter(self, read:bool, linefilter:LINE_FILTER, linefreq:LINE_FREQ=LINE_FREQ._50Hz):
        if(read):
            self.write('ILIN?')
            return str.strip(self.read())
        else:
            self.write('ILIN ' + str(linefilter.value))
            if(linefilter != self.LINE_FILTER.THROUGH):
                self.write('IFREQ ' + str(linefreq.value))
            return

    def lowpass_filter(self, read:bool, enable:bool):
        if(read):
            self.write('ITHR?')
            return str.strip(self.read())
        else:
            if(enable):
                self.write('ITHR ' + str(0))
            else:
                self.write('ITHR ' + str(1))
            return
    ########################################################################
    ## dynamic reserve
    ########################################################################
    class DYNAMIC_RESERVE(Enum):
        HIGH    =   0
        MEDIUM  =   1
        LOW     =   2

    def dynamic_reserve(self, read:bool, dreserve:DYNAMIC_RESERVE):
        if(read):
            self.write('DRSV?')
            return str.strip(self.read())
        else:
            self.write('DRSV ' + str(dreserve.value))
            return
    ########################################################################
    ## sensityvity settings
    ########################################################################
    class VOLTAGE_SENSITIVITY(Enum):
        _2nV    = 0
        _5nV    = 1
        _10nV   = 2
        _20nV   = 3
        _50nV   = 4
        _100nV  = 5
        _200nV  = 6
        _500nV  = 7
        _1uV    = 8
        _2uV    = 9
        _5uV    = 10
        _10uV   = 11
        _20uV   = 12
        _50uV   = 13
        _100uV  = 14
        _200uV  = 15
        _500uV  = 16
        _1mV    = 17
        _2mV    = 18
        _5mV    = 19
        _10mV   = 20
        _20mV   = 21
        _50mV   = 22
        _100mV  = 23
        _200mV  = 24
        _500mV  = 25
        _1V     = 26
    
    def set_voltage_sensitivity(self, read:bool, sensitivity:VOLTAGE_SENSITIVITY):
        if(read):
            self.write('VSEN?')
            return str.strip(self.read())
        else:
            self.write('VSEN ' + str(sensitivity.value))
            return

    class CURRENT_SENSITIVITY(Enum):
        _5fA    = 1
        _10fA   = 2
        _20fA   = 3
        _50fA   = 4
        _100fA  = 5
        _200fA  = 6
        _500fA  = 7
        _1pA    = 8
        _2pA    = 9
        _5pA    = 10
        _10pA   = 11
        _20pA   = 12
        _50pA   = 13
        _100pA  = 14
        _200pA  = 15
        _500pA  = 16
        _1nA    = 17
        _2nA    = 18
        _5nA    = 19
        _10nA   = 20
        _20nA   = 21
        _50nA   = 22
        _100nA  = 23
        _200nA  = 24
        _500nA  = 25
        _1uA    = 26

    def set_current_sensitivity(self, read:bool, sensitivity:CURRENT_SENSITIVITY):
        if(read):
            self.write('ISEN?')
            return str.strip(self.read())
        else:
            self.write('ISEN ' + str(sensitivity.value))
            return
    
    class TIME_CONSTANT(Enum):
        _10us   = 0
        _30us   = 1
        _100us  = 2
        _300us  = 3
        _1ms    = 4
        _3ms    = 5
        _10ms   = 6
        _30ms   = 7
        _100ms  = 8
        _300ms  = 9
        _1s     = 10
        _3s     = 11
        _10s    = 12
        _30s    = 13
        _100s   = 14
        _300s   = 15
        _1ks    = 16
        _3ks    = 17
        _10ks   = 18
        _30ks   = 19
    
    ########################################################################
    ## time constant settings
    ########################################################################
    def set_time_constant(self, read:bool, timeconstant:TIME_CONSTANT):
        if(read):
            self.write('TCON')
            return str.strip(self.read())
        else:
            self.write('TCON ' + str(timeconstant.value))
            return
    
    def execute_auto_time_constant(self):
        self.write('ATIM')
        return
    
    def set_synchronous_filter(self, read:bool, enable:bool):
        if(read):
            self.write('SYNC?')
            return str.strip(self.read())
        else:
            if(enable):
                self.write('SYNC ' + str(1))
            else:
                self.write('SYNC ' + str(0))
            return
    
    class SLOPE(Enum):
        _6dB    = 0
        _12dB   = 1
        _18dB   = 2
        _24dB   = 3

    def set_slope(self, read:bool, slope:SLOPE):
        if(read):
            self.write('SLOP')
            return str.strip(self.read())
        else:
            self.write('SLOP ' + str(slope.value))
            return
    
    ################################################################
    ## reference settings
    ################################################################
    class REFERENCE_SOURCE(Enum):
        REFIN               = 0
        INTERNAL_OSCILLATOR = 1
        SIGNAL              = 2

    def set_reference_source(self, read:bool, reference:REFERENCE_SOURCE):
        if(read):
            self.write('RSRC?')
            return str.strip(self.read())
        else:
            self.write('RSRC ' + str(reference.value))
            return
    class REFERENCE_EDGE(Enum):
        SINE_POS    = 0
        TTL_POS     = 1
        TTL_NEG     = 2

    def set_reference_edge(self, read:bool, edge:REFERENCE_EDGE):
        if(read):
            self.write('REDG?')
            return str.strip(self.read())
        else:
            self.write('REDG ' + str(edge.value))
            return
    
    class BASIC_FUNCTION_REF_MODE(Enum):
        INTERNAL_F  = 0
        INTERNAL_2F = 1
        REFERENCE_F = 2
        REFERENCE_2F= 3
        SIGNAL_F    = 4
        SIGNAL_2F   = 5
        INTERNAL    = 6
        REFERENCE   = 8
        SIGNAL      = 9
        
    def set_basic_function_ref_mode(self, read:bool, brm:BASIC_FUNCTION_REF_MODE):
        if(read):
            self.write('BRM?')
            return str.strip(self.read())
        else:
            self.write('BRM ' + str(brm.value))
            return
    
    def set_harmonic_order(self, read:bool, number:int):
        if(read):
            self.write('HARM?')
            return str.strip(self.read())
        else:
            self.write('HARM ' + str(number))
            return

    ################################################################
    ## data settings
    ################################################################
    class DATA1TYPE(Enum):
        X       = 0
        R       = 1
        NOISE   = 2
        AUX1    = 3

    def set_data1(self, read:bool, data1type:DATA1TYPE):
        if(read):
            self.write('DDEF? 1')
            return str.strip(self.read())
        else:
            self.write('DDEF 1, ' + str(data1type.value))
            return

    class DATA2TYPE(Enum):
        Y       = 0
        THETA   = 1
        AUX1    = 2
        AUX2    = 3

    def set_data2(self, read:bool, data2type:DATA2TYPE):
        if(read):
            self.write('DDEF? 2')
            return str.strip(self.read())
        else:
            self.write('DDEF 2, ' + str(data2type.value))
            return

    class OUTPUT_TYPE(Enum):
        LINE_NUMBER     = 0
        DATA1           = 1
        DATA2           = 2
        FREQUENCY       = 3
        SENSITIVITY     = 4
        OVERLEVEL       = 5

    def set_output_type(self, read:bool, *outputtype:OUTPUT_TYPE):
        if(read):
            self.write('OTYP?')
            return str.strip(self.read())
        else:
            outputstrings = ''
            for i, t in enumerate(outputtype):
                if(i == 0):
                    outputstrings += str(t.value)
                else:
                    outputstrings += ',' + str(t.value)
            self.write('OTYP ' + outputstrings)
            return
    
    def read_data(self):
        self.write('DOUT?')
        output_data = [float(s) for s in str.strip(self.read()).split(',')]
        return output_data
    
    def check_overlevel(self):
        self.write('OVER?')
        return str.strip(self.read())
