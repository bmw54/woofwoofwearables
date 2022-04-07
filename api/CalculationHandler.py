import scipy.integrate
import numpy as np

class Calculation_Module:

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
        
    def get_velocity_from_acceleration(self, acceleration_timeseries):
        timestamps = [d['Time'] for d in acceleration_timeseries]
        values = [d['Value'] for d in acceleration_timeseries]
        velocity = scipy.integrate.cumtrapz(values, x=timestamps)
        ret = []
        for k in range(0, len(velocity)):
            ret.append({"Time": timestamps[k], "Value": velocity[k]})
        return ret

    def get_position_from_acceleration(self, acceleration_timeseries):
        timestamps = [d['Time'] for d in acceleration_timeseries]
        values = [d['Value'] for d in acceleration_timeseries]
        velocity = scipy.integrate.cumtrapz(values, x=timestamps)
        print(len(velocity))
        print(len(timestamps))
        timestamps.pop()
        position = scipy.integrate.cumtrapz(velocity, x=timestamps)
        ret = []
        for k in range(0, len(position)):
            ret.append({"Time": timestamps[k], "Value": position[k]})
        return ret
    
    def calculate_pitch_from_vector(self, vector):
        angle = np.arctan(vector[2], vector[1]);
        print(angle)
        return angle
    
    def calculate_angle_two_vectors(self, a_vec, b_vec):
        a_mag = np.linalg.norm(a_vec)
        b_mag = np.linalg.norm(b_vec)
        dot = np.dot(a_vec, b_vec)
        angle = np.arccos(dot/(a_mag * b_mag))
        print(angle)
        return angle

    def get_pitches_angles_from_vectors(self, vectors):
        pitches = []
        angles = []
        for i in range(0, len(vectors)):
            pitches.append(self.calculate_pitch_from_vector(vectors[i]))
            projection = [0, vectors[i][1], vectors[i][2]]
            angles.append(self.calculate_angle_two_vectors(vectors[i], projection))
        return pitches, angles

    def calculate_frequency(self, angles, timestamps):
        mean = np.mean(angles)
        print(mean)
        if len(angles) < 2 or len(timestamps) <2  or len(angles) != len(timestamps) :
            return 0.0
        before = angles[0]
        crosses = 0
        for i in range(1, len(angles)):
            curr = angles[i]
            if (curr <= mean and before > mean) or (curr >= mean and before < mean):
                crosses+=1
            before = curr
        duration = timestamps[-1] - timestamps[0]
        frequency = crosses / (duration * 2)
        print(crosses)
        return frequency
    
    def calculate_average_amplitude(self, angles):
        rms = np.sqrt(np.mean(np.square(angles)))
        return rms

if __name__ == '__main__':
    ch = Calculation_Module()
    angles =[30, 25, 20, 15, 10, 5, 0 , -5, -10, -15, -20, -25, -30]
    timestamps = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.60]
    frequency = ch.calculate_frequency(angles, timestamps)
    print(frequency)

    amplitude = ch.calculate_average_amplitude(angles)
    print(amplitude)
