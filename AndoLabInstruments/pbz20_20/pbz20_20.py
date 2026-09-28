from pymeasure.instruments import Instrument
from enum import Enum

class PBZ20_20(Instrument):
    def __init__(self, adapter, name="PBZ20_20", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def initialize(self):
        self.write('*RST')

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def error(self):
        self.write(':SYST:ERR?')
        return self.read()
    
    def output(self, enable:bool):
        if(enable):
            self.write('OUTPut:STATe:IMMediate 1')
        else:
            self.write('OUTPut:STATe:IMMediate 0')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return

    def set_voltage(self, voltage:float):
        self.write('VOLT ' + str(voltage))
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def clear_protection(self):
        self.write('OUTPut:PROTection:CLEar')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    

    class PROT_MODE(Enum):
        LIMIT   = 0
        TRIP    = 1

    def set_OVP_mode(self, mode:PROT_MODE):
        '''
        Sets the mode (V-LIMIT or OVP) of the overvoltage protection features.
        '''
        if(mode == self.PROT_MODE.LIMIT):
            self.write('VOLTage:PROTection:STATe LIMit')
        if(mode == self.PROT_MODE.TRIP):
            self.write('VOLTage:PROTection:STATe TRIP')
        return

    def set_OCP_mode(self, mode:PROT_MODE):
        '''
        Sets the mode (I or OCP) of the overcurrent protection features.
        '''
        if(mode == self.PROT_MODE.LIMIT):
            self.write('CURRent:PROTection:STATe LIMit')
        if(mode == self.PROT_MODE.TRIP):
            self.write('CURRent:PROTection:STATe TRIP')
        return
    
    def set_OVP_limit(self, under:float, over:float):
        self.write('VOLTage:PROTection:UNDer ' + str(under))
        self.write('VOLTage:PROTection:OVER ' + str(over))
        return

    def set_OCP_limit(self, under:float, over:float):
        self.write('CURRent:PROTection:UNDer ' + str(under))
        self.write('CURRent:PROTection:OVER ' + str(over))
        return
    
    def set_OVP_limit_abs(self, unsigned_limit:float):
        self.set_OVP_limit(-1*unsigned_limit, unsigned_limit)
        return
    
    def set_OCP_limit_abs(self, unsigned_limit:float):
        self.set_OCP_limit(-1*unsigned_limit, unsigned_limit)
        return
    
    def set_soft_start_timer(self, time:float):
        self.write('TRIGger:OUTPut:SSTart:RISE ' + str(time))


    class FUNC_MODE(Enum):
        """
        constant voltage (CV) or constant current (CC)
        """
        CV = 'CV'
        CC = 'CC'

    def get_function_mode(self) -> str:
        self.write('FUNCtion:MODE?')
        return self.read().strip()

    def set_function_mode(self, mode: FUNC_MODE):
        '''
        switch between CV/CC mode
        '''
        was_on = self.get_output_state()
        if was_on:
            self.output(False)
 
        self.write('FUNCtion:MODE ' + mode.value)
 
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
 
        return
    
    def get_output_state(self) -> bool:
        self.write('OUTPut:STATe:IMMediate?')
        return self.read().strip() in ('1', 'ON')

    def set_current(self, current:float):
        self.write('CURR ' + str(current))
 
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
 
        return

 
    class CURR_RESPONSE(Enum):
        US35  = 35
        US100 = 100
        US350 = 350
        MS1   = 1000

    def set_current_response(self, response: CURR_RESPONSE):
        '''
        set the response time for the CC mode, which is required
        to counteract the electromotive force via magnetic induction
        We can select the response time from 100/350/1000us.
        '''
        self.write('CURRent:RESPonse ' + str(response.value) + 'US')
 
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
 
        return