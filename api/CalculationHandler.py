import numpy as np
import math as m
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import blackman
import matplotlib.animation as ani
from mpl_toolkits.mplot3d import Axes3D
import TwoIMUs

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
        
    # def get_velocity_from_acceleration(self, acceleration_timeseries):
    #     timestamps = [d['Time'] for d in acceleration_timeseries]
    #     values = [d['Value'] for d in acceleration_timeseries]
    #     velocity = scipy.integrate.cumtrapz(values, x=timestamps)
    #     ret = []
    #     for k in range(0, len(velocity)):
    #         ret.append({"Time": timestamps[k], "Value": velocity[k]})
    #     return ret

    # def get_position_from_acceleration(self, acceleration_timeseries):
    #     timestamps = [d['Time'] for d in acceleration_timeseries]
    #     values = [d['Value'] for d in acceleration_timeseries]
    #     velocity = scipy.integrate.cumtrapz(values, x=timestamps)
    #     print(len(velocity))
    #     print(len(timestamps))
    #     timestamps.pop()
    #     position = scipy.integrate.cumtrapz(velocity, x=timestamps)
    #     ret = []
    #     for k in range(0, len(position)):
    #         ret.append({"Time": timestamps[k], "Value": position[k]})
    #     return ret
    
    def calculate_pitch_from_vector(self, vector):
        angle = m.atan(vector[2] / vector[1]);
        return angle
    
    def calculate_angle_two_vectors(self, a_vec, b_vec):
        a_mag = np.linalg.norm(a_vec)
        b_mag = np.linalg.norm(b_vec)
        dot = np.dot(a_vec, b_vec)
        angle = np.arccos(dot/(a_mag * b_mag))
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
        N = len(angles)
        # sample spacing
        T = timestamps[1] - timestamps[0]
        w = blackman(N)
        ywf = fft(angles*w)
        xf = fftfreq(N, T)[:N//2]
        max_amp_freq = np.argmax(2.0/N * np.abs(ywf[1:N//2])) / (N * T)
        print(np.max(2.0/N * np.abs(ywf[1:N//2])))
        # mean = np.mean(angles)
        # if len(angles) < 2 or len(timestamps) <2  or len(angles) != len(timestamps) :
        #     return 0.0
        # before = angles[0]
        # crosses = 0
        # for i in range(1, len(angles)):
        #     curr = angles[i]
        #     if (curr <= mean and before > mean) or (curr >= mean and before < mean):
        #         crosses+=1
        #     before = curr
        # duration = timestamps[-1] - timestamps[0]
        # frequency = crosses / (duration * 2)
        return max_amp_freq
    
    def calculate_average_amplitude(self, angles):
        rms = np.sqrt(np.mean(np.square(angles)))
        return rms

    def calculate_ft(self, angles, timestamps):
        # N = len(angles)
        # # sample spacing
        # T = timestamps[1] - timestamps[0]
        # yf = fft(angles)
        # xf = fftfreq(N, T)[:N//2]
        # w = blackman(N)
        # ywf = fft(angles*w)
        # xf = fftfreq(N, T)[:N//2]
        # plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
        # plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')
        # plt.legend(['FFT', 'FFT w. window'])
        # plt.grid()
        # plt.savefig("fft.png")

        # max_amp = np.max(2.0/N * np.abs(ywf[1:N//2]))
        # max_amp_freq = xf[1:N//2][list(2.0/N * np.abs(ywf[1:N//2])).index(max_amp)]

        # print(max_amp)
        # print(max_amp_freq)

        t0 = timestamps[0]
        t1 = timestamps[-1]
        n_samples = len(angles)
        xs = timestamps
        ys = angles
        # plt.subplot(2, 1, 1)
        # plt.plot(xs, ys)
        np_fft = np.fft.fft(ys)
        amplitudes = 2 / n_samples * np.abs(np_fft) 
        frequencies = np.fft.fftfreq(n_samples) * n_samples * 1 / (t1 - t0)
        # plt.subplot(2, 1, 2)
        plt.semilogx(frequencies[:len(frequencies) // 2], amplitudes[:len(np_fft) // 2])
        plt.ylim((0,0.2))
        #print(amplitudes[:len(np_fft) // 2])
        max_amp = np.max(amplitudes[:len(np_fft) // 2])
        max_amp_freq = frequencies[:len(frequencies) // 2][list(amplitudes[:len(np_fft) // 2]).index(max_amp)]

        print(max_amp)
        print(max_amp_freq)
        dists = frequencies[:len(frequencies) // 2]
        weights = amplitudes[:len(np_fft) // 2]
        avefreq = sum([dists[i]*weights[i] for i in range(len(dists))])/sum(weights)
        print(avefreq)
        plt.savefig("ftt2.png")
        plt.close()



    def calculate_side_bias_from_vectors(self, vectors):
        angles = [m.atan(vector[0] / vector[1]) for vector in vectors]
        mean = np.mean(angles)
        return mean


    def plot_vectors(self, vectors, timestamps):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        timeStep = timestamps[1]-timestamps[0]
        vectors = np.asarray(vectors)
        #def plotOrientation(i=int):
        #sampleNum = i%len(timestamps)
        origin = np.array([[0, 0, 0],[0, 0, 0], [0,0,0]]) # origin point
        ax.clear()
        ax.set_xlim([0, 2])
        ax.set_ylim([0, 2])
        ax.set_zlim([0, 2])
        print(vectors[1])
    
        vlength=np.linalg.norm(vectors[0])
        ax.quiver(*origin,vectors[1][0],vectors[1][1],vectors[1][2],
                pivot='tail',length=vlength,arrow_length_ratio=0.3/vlength)
        ax.set_box_aspect((1, 1, 1))  # aspect ratio is 1:1:1 in data space
        ax.set_xlabel('X') # X-axis seems to be North
        ax.set_ylabel('Y') # Y-axis seems to be cross_product(Up, North)
        ax.set_zlabel('Z') # Z-axis seems to be Up
       # animator = ani.FuncAnimation(fig, plotOrientation, interval = timeStep*1000)
        #animator.save('test_anim.mp4', fps=1/timeStep)
        plt.savefig("Vecs.png")
        plt.close()

if __name__ == '__main__':
    # ch = Calculation_Module()
    # timestamps = np.arange(0, 2, 0.05)
    # angles = 30 * np.cos(timestamps)

    # frequency = ch.calculate_frequency(angles, timestamps)
    # print(frequency)

    # amplitude = ch.calculate_average_amplitude(angles)
    # print(amplitude)

    # side_bias  = ch.calculate_side_bias(angles)
    # print(side_bias)

    # ch.calculate_fft(angles, timestamps)
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    calculation_module.plot_vectors(vectors, timestamps)

