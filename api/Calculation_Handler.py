import scipy.integrate


class Averages_Module:
    def get_averages(self, time_period, timeseries):
        timestamps = [d['Time'] for d in timeseries]
        values = [d['Value'] for d in timeseries]
        if len(timestamps) == 0:
             return []
        i = 0
        averages = []
        beginning_timestamps = []
        while i < len(timestamps):
            l = 0
            sum = 0.0
            start_time = timestamps[i]
            beginning_timestamps.append(start_time)
            while i < len(timestamps) and timestamps[i] < start_time + time_period:
                sum += values[i]
                l += 1
                i += 1
            if l > 0:
                average = sum / l
                averages.append(average)
        ret = []
        for k in range(0, len(beginning_timestamps)):
            ret.append({"Time": beginning_timestamps[k], "Value": averages[k]})
        return ret
        

class Velocity_Module:
    def get_velocity_from_acceleration(self, acceleration_timeseries):
        timestamps = [d['Time'] for d in acceleration_timeseries]
        values = [d['Value'] for d in acceleration_timeseries]
        velocity = scipy.integrate.cumtrapz(values, x=timestamps)
        ret = []
        for k in range(0, len(velocity)):
            ret.append({"Time": timestamps[k], "Value": velocity[k]})
        return ret






    
    
  

      
