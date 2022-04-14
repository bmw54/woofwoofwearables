import numpy as np
from skinematics import vector, quat, rotmat

def modifiedKalman(rate, acc, omega, mag,
           D = [0.4, 0.4, 0.4],          
           tau = [0.5, 0.5, 0.5],
           Q_k = None,
           R_k = None):
    '''
    Kalman filter copied from site-packages/skinematics/imus.py with one line commented out
    at the end to prevent the filter from using the first input as the reference.

    Calclulate the orientation from IMU magnetometer data.

    Parameters
    ----------
    rate : float
    	   sample rate [Hz]	
    acc : (N,3) ndarray
    	  linear acceleration [m/sec^2]
    omega : (N,3) ndarray
    	  angular velocity [rad/sec]
    mag : (N,3) ndarray
    	  magnetic field orientation
    D : (,3) ndarray
          noise variance, for x/y/z [rad^2/sec^2]
          parameter for tuning the filter; defaults from Yun et al.
          can also be entered as list
    tau : (,3) ndarray
          time constant for the process model, for x/y/z [sec]
          parameter for tuning the filter; defaults from Yun et al.
          can also be entered as list
    Q_k : None, or (7,7) ndarray
          covariance matrix of process noises
          parameter for tuning the filter
          If set to "None", the defaults from Yun et al. are taken!
    R_k : None, or (7,7) ndarray
          covariance matrix of measurement noises
          parameter for tuning the filter; defaults from Yun et al.
          If set to "None", the defaults from Yun et al. are taken!
          

    Returns
    -------
    qOut : (N,4) ndarray
    	   unit quaternion, describing the orientation relativ to the coordinate
           system spanned by the local magnetic field, and gravity

    Notes
    -----
    Based on "Design, Implementation, and Experimental Results of a Quaternion-
       Based Kalman Filter for Human Body Motion Tracking" Yun, X. and Bachman,
       E.R., IEEE TRANSACTIONS ON ROBOTICS, VOL. 22, 1216-1227 (2006)

    '''

    numData = len(acc)

    # Set parameters for Kalman Filter
    tstep = 1./rate
    
    # check input
    assert len(tau) == 3
    tau = np.array(tau)

    # Initializations 
    x_k = np.zeros(7)	# state vector
    z_k = np.zeros(7)   # measurement vector
    z_k_pre = np.zeros(7)
    P_k = np.eye(7)		 # error covariance matrix P_k

    Phi_k = np.eye(7)    # discrete state transition matrix Phi_k
    for ii in range(3):
        Phi_k[ii,ii] = np.exp(-tstep/tau[ii])

    H_k = np.eye(7)		# Identity matrix

    D = np.r_[0.4, 0.4, 0.4]		# [rad^2/sec^2]; from Yun, 2006
    
    if Q_k is None:
        # Set the default input, from Yun et al.
        Q_k = np.zeros((7,7)) 	# process noise matrix Q_k
        for ii in range(3):
            Q_k[ii,ii] =  D[ii]/(2*tau[ii])  * ( 1-np.exp(-2*tstep/tau[ii]) )
    else:
        # Check the shape of the input
        assert Q_k.shape == (7,7)

    # Evaluate measurement noise covariance matrix R_k
    if R_k is None:
        # Set the default input, from Yun et al.
        r_angvel = 0.01;      # [rad**2/sec**2]; from Yun, 2006
        r_quats = 0.0001;     # from Yun, 2006
        
        r_ii = np.zeros(7)
        for ii in range(3):
            r_ii[ii] = r_angvel
        for ii in range(4):
            r_ii[ii+3] = r_quats
            
        R_k = np.diag(r_ii)    
    else:
        # Check the shape of the input
        assert R_k.shape == (7,7)

    # Calculation of orientation for every time step
    qOut = np.zeros( (numData,4) )

    for ii in range(numData):
        accelVec  = acc[ii,:]
        magVec    = mag[ii,:]
        angvelVec = omega[ii,:]
        z_k_pre = z_k.copy()  # watch out: by default, Python passes the reference!!

        # Evaluate quaternion based on acceleration and magnetic field data 
        accelVec_n = vector.normalize(accelVec)
        magVec_hor = magVec - accelVec_n * (accelVec_n @ magVec)
        magVec_n   = vector.normalize(magVec_hor)
        basisVectors = np.column_stack( [magVec_n,
                                np.cross(accelVec_n, magVec_n), accelVec_n] )
        quatRef = quat.q_inv(rotmat.convert(basisVectors, to='quat')).ravel()

        # Calculate Kalman Gain
        # K_k = P_k * H_k.T * inv(H_k*P_k*H_k.T + R_k)
        K_k = P_k @ np.linalg.inv(P_k + R_k)

        # Update measurement vector z_k
        z_k[:3] = angvelVec
        z_k[3:] = quatRef

        # Update state vector x_k
        x_k += np.array( K_k@(z_k-z_k_pre) ).ravel()

        # Evaluate discrete state transition matrix Phi_k
        Delta = np.zeros((7,7))
        Delta[3,:] = np.r_[-x_k[4], -x_k[5], -x_k[6],      0, -x_k[0], -x_k[1], -x_k[2]]
        Delta[4,:] = np.r_[ x_k[3], -x_k[6],  x_k[5], x_k[0],       0,  x_k[2], -x_k[1]]
        Delta[5,:] = np.r_[ x_k[6],  x_k[3], -x_k[4], x_k[1], -x_k[2],       0,  x_k[0]]
        Delta[6,:] = np.r_[-x_k[5],  x_k[4],  x_k[3], x_k[2],  x_k[1], -x_k[0],       0]
        
        Delta *= tstep/2
        Phi_k += Delta

        # Update error covariance matrix
        P_k = (np.eye(7) - K_k) @ P_k

        # Projection of state
        # 1) quaternions
        x_k[3:] += tstep * 0.5 * quat.q_mult(x_k[3:], np.r_[0, x_k[:3]]).ravel()
        x_k[3:] = vector.normalize( x_k[3:] )
        # 2) angular velocities
        x_k[:3] -= tstep * tau * x_k[:3]

        qOut[ii,:] = x_k[3:]

        # Projection of error covariance matrix
        P_k = Phi_k @ P_k @ Phi_k.T + Q_k

    # Make the first position the reference position
    # qOut = quat.q_mult(qOut, quat.q_inv(qOut[0]))

    return qOut