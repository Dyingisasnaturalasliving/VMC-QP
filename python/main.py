import numpy as np
import pybullet as p
import pybullet_data as pd
import robot as rob
import convexMPCController
import time
import math
import swingLeg
import sys
import matplotlib.pyplot as plt

import locomotion
# import stanceController


physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0)
p.setAdditionalSearchPath('/home/luobin/anaconda3/lib/python3.7/site-packages/pybullet_data')
p.setPhysicsEngineParameter(numSolverIterations=30)
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,0.41]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0.0])
p.setAdditionalSearchPath('/home/luobin/anaconda3/lib/python3.7/site-packages/pybullet_data/a1')
robot_id = p.loadURDF("a1.urdf",cubeStartPos, cubeStartOrientation)
p.setAdditionalSearchPath('./')
p.loadURDF("slope.urdf", [3.0, 0, 0.0], [0, 0, 0, 1])

robot = rob.Robot(p, robot_id)

# mass = 108 / 9.8;
# inertial = [0.01683993, 0.056579028, 0.064713601, 8.3902e-05, 0.000597679, 2.5134e-05]
# planning_time_step = 0.03
# weights = [5, 5, 0.2, 0.0, 0.0, 10, 0.0, 0.0, 1., 1., 1., 1., 0]
# weight_alpha = 1e-5
# friction_coeff = 0.4
#
# convexMPC = convexMPCController.ContactForceMpcCaculate(mass, inertial,planning_time_step,
#                                                         weights, weight_alpha, friction_coeff)

# linear_velocity_in_gravity_frame = [0.0, 0.0, 0.0]
# angular_velocity_in_gravity_frame = [0.0, 0.0, 0.0]
# euler_angle = [0.0 / 180 * 3.1416, 0.0 / 180 * 3.1416, 0.0 / 180 * 3.1416]
# foot_pos_in_gravity_frame = [0.17, -0.13, -0.4,
#                              0.17, 0.13, -0.4,
#                              -0.17, -0.13, -0.4,
#                              -0.17, 0.13, -0.4]
# leg_contact_state = [1, 1, 1,1]
# robot_height = 0.3
# desired_linear_velocity_in_gravity_frame = [0.0, 0.0, 0.0]
# desired_angular_velocity_in_gravity_frame = [0.0, 0.0, 0.0]
# desired_euler_angle = [0.0, 0.0, 0.0]
# desired_robot_height = 0.3





# start = time.clock()
# contact_trajectory = convexMPC.getContactForceTrajectory(linear_velocity_in_gravity_frame,
#                                                              angular_velocity_in_gravity_frame,
#                                                              euler_angle,
#                                                              foot_pos_in_gravity_frame,
#                                                              leg_contact_state,
#                                                              robot_height,
#                                                              desired_linear_velocity_in_gravity_frame,
#                                                              desired_angular_velocity_in_gravity_frame,
#                                                              desired_euler_angle,
#                                                              desired_robot_height)
# end = time.clock()
# for i in range(12):
#     if i % 3 == 0:
#         print("\n")
#     print(-contact_trajectory[i])
#
# print("\n\n")
# print(end - start)



time_step = 0.001
p.setTimeStep(time_step)



p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)

# desired_linear_velocity_in_gravity_frame = [0.0, 0.0, 0.0]
# desired_angular_velocity_in_gravity_frame = [0.0, 0.0, 0.0]
# desired_euler_angle = [0.0, 0.0, 0.0]
# desired_robot_height = 0.3
#
# step_count = 0
# period = 2.5
# robot.printJointInfo()
# swing_leg_controller = swingLeg.SwingLeg(robot, None, 1.0)

# swing_time = 100.0
step_count = 0
current_time = 0.0

locomotion_controller = locomotion.Locomotion(robot)

desired_linear_velocity = [0.0, 0.0, 0.0]
desired_angular_velocity = [0.0, 0.0, 0.0]
desired_euler_angle= [0.0, 0.0, 0.0]
desired_robot_height = 0.3

period = 2.0


phase = 0.0

foot_pos_record = []





np.set_printoptions(suppress=True)

estimated_vel = []
actual_vel = []

measured_val = []

desired_x_speed = 0.0
desired_y_speed = 0.0
desired_twist_speed= 0.0

while current_time <= 30:
    location, _ = p.getBasePositionAndOrientation(robot_id)
    p.resetDebugVisualizerCamera(
        cameraDistance=1.5,
        cameraYaw=20,
        cameraPitch=-30,
        cameraTargetPosition=location
    )
    # p.resetBasePositionAndOrientation(robot_id, [0.0, 0.0, 1.0],
    #                                   p.getQuaternionFromEuler(
    #                                       [0.0 / 180.0 * math.pi, 0.0 / 180.0 * math.pi, 0 / 180.0 * math.pi]))
    #
    #
    # phase = math.fmod(current_time, 0.1) / 0.1
    # trajectory =swing_leg_controller.swingTrajectoryGenerate(np.mat([0.0, -0.13, -0.24]).transpose(),
    #                                              np.mat([0.2, -0.13, 0.05]).transpose(),
    #                                              np.mat([0.4, -0.13, -0.24]).transpose(),
    #                                              phase)
    #
    # robot.setFootPosInBaseFrame(0, trajectory)
    # robot.setFootPosInBaseFrame(1, [0.17, 0.13, -0.24])
    # robot.setFootPosInBaseFrame(2, [-0.17, -0.13, -0.24])
    # robot.setFootPosInBaseFrame(3, [-0.17, 0.13, -0.24])
    #
    # foot_pos_record.append(robot.getFootPosInBodyFrame()[0][0])


    # start = np.mat([[0.0, 0.0, -0.3]]).transpose()
    # mid = np.mat([[0.2, -0.1, 0.1]]).transpose()
    # end = np.mat([[0.4, -0.2, -0.3]]).transpose()
    #
    # phase = math.fmod(current_time, swing_time) / swing_time
    #
    # trajectory = swing_leg_controller.swingTrajectoryGenerate(start, mid, end, phase)
    #
    # robot.setFootPosInGravityFrame(0, trajectory)
    # robot.setFootPosInGravityFrame(1, [0.17, 0.13, -0.3])
    # robot.setFootPosInGravityFrame(2, [-0.17, -0.13, -0.3])
    # robot.setFootPosInGravityFrame(3, [-0.17, 0.13, -0.3])



    if step_count < 10:
        robot.setFootPosInBaseFrame(0, [0.17, -0.13, -0.1])
        robot.setFootPosInBaseFrame(1, [0.17, 0.13, -0.3])
        robot.setFootPosInBaseFrame(2, [-0.17, -0.13, -0.3])
        robot.setFootPosInBaseFrame(3, [-0.17, 0.13, -0.3])

        # stance_controller.run([0.0, -0.0, 0.0], 0.3, 0, 0, math.pi)
        # joint_pos = [-90.0 / 180 * math.pi]*12
        # mass_mat_raw = p.calculateMassMatrix(robot_id, joint_pos)
        # mass_mat = np.mat(np.zeros([18, 18]))
        #
        # for i in range(18):
        #     for j in range(18):
        #         mass_mat[i, j] = mass_mat_raw[i][j]
        #
        # print(mass_mat[12:18, 12:18], '\n\n')
        roll = 0.0 / 180.0 * math.pi
        pitch = 0.0 / 180.0 * math.pi
        yaw = 0.0 / 180.0 * math.pi
        euler = p.getQuaternionFromEuler([roll, pitch, yaw])
        euler = list(euler)

        pos = [0.0]*19

        pos[0:4] = euler
        pos[4:7] = [0.0]*3

        pos[7:19] = [0.0]*12

        vel = [0.0]*18
        vel[0:6] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        acc = [0.0]*18
        acc[0:6] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


        C_term = p.calculateInverseDynamics(robot_id, pos, vel, acc)

        C_term_mat = np.mat(np.zeros([18, 1]))

        for i in range(18):
            C_term_mat[i, 0] = C_term[i]

        print(pos,'\n')
        print(C_term_mat, '\n\n')


        # linear_jacobian, angular_jacobian = p.calculateJacobian(robot_id, 5, [0.0]*3, [0.0]*12, [0.0]*12, [0.0]*12)
        #
        # for e in angular_jacobian:
        #     print(e)
        # for e in linear_jacobian:
        #     print(e)
        #
        # print('\n\n')

    elif step_count < 1000:
        pass

    else:

        kp = 10

        # desired_linear_velocity[0] = kp* (0.0 - robot_pos[0])
        # desired_linear_velocity[1] = kp * (0.0 - robot_pos[1])
        #
        # desired_angular_velocity[2] = kp * (0.0 - robot_euler[2])
        #
        # desired_euler_angle[1] = 0.2 * math.sin(2 * math.pi / period * current_time)
        # desired_linear_velocity[0] += 0.0001
        #
        # if desired_linear_velocity[0] > 1.0:
        #     desired_linear_velocity[0] = 1.0

        # desired_angular_velocity[2] = 10.0 * (0.0 - robot.getRobotEuler()[2])
        # desired_linear_velocity[0] = 1.0 * (0.0 - robot.getRobotPos()[0])
        # desired_linear_velocity[1] = 1.0 * (0.0 - robot.getRobotPos()[1])

        # desired_linear_velocity[1] += 1e-3
        # if desired_linear_velocity[1] > 1.5:
        #     desired_linear_velocity[1] = 1.5

        # if current_time < 40.0:
        #     desired_x_speed = 0.5
        #     desired_y_speed = 0.0
        #     desired_twist_speed = -0.0
        # elif current_time < 60.0:
        #     desired_x_speed = 0.0
        #     desired_y_speed = -0.3
        #     desired_twist_speed = 0.0
        # elif current_time < 70.0:
        #     desired_x_speed = 0.0
        #     desired_y_speed = 0.3
        #     desired_twist_speed = 0.0
        # elif current_time < 100.0:
        #     desired_x_speed = 0.0
        #     desired_y_speed = 0.0
        #     desired_twist_speed = 0.5
        # elif current_time < 120.0:
        #     desired_x_speed = 0.0
        #     desired_y_speed = 0.0
        #     desired_twist_speed = -1.2
        # else:
        #     desired_x_speed = -0.3
        #     desired_y_speed = 0.0
        #     desired_twist_speed = 0.0

        desired_speed = 0.3

        yaw = robot.getRobotEuler()[2]

        speed, _= p.multiplyTransforms([0, 0, 0], p.getQuaternionFromEuler([0, 0, -yaw]),
                             [desired_speed, 0, 0], [0, 0, 0, 1])


        desired_x_speed = speed[0]
        desired_y_speed = speed[1]


        desired_twist_speed= 0.7



        locomotion_controller.run(current_time, desired_x_speed, desired_y_speed, desired_twist_speed, desired_robot_height)
        # print("current_time: ",current_time, '\n\n')

        # foot_pos_record.append(robot.getFootPosInGravityFrame()[0][2])

        # print(robot.getRobotPos()[2])

        estimated_vel.append(locomotion_controller._state_estimator.getEstimatedVelocity()[0])
        actual_vel.append(robot.getRobotLinearVelocity()[0])

        # measured_val.append(robot.getRobotPos()[2])

        current_time += 5* time_step


    #     linear_velocity_in_gravity_frame = robot.getRobotLinearVelocity()
    #     angular_velocity_in_gravity_frame = robot.getRobotAngulurVelocity()
    #     euler_angle = robot.getRobotEuler()
    #     euler_angle = list(euler_angle)
    #     euler_angle[2] = 0.0
    #     foot_pos_in_gravity_frame = robot.getFootPosInGravityFrame()
    #     foot_pos_in_gravity_frame = np.asarray(foot_pos_in_gravity_frame).flatten()
    #     leg_contact_state = [int(1), int(1), int(1), int(1)]
    #     robot_height = robot.getRobotPos()[2]
    #     robot_pos = robot.getRobotPos()
    #
    #     kp = 10
    #
    #     desired_linear_velocity_in_gravity_frame[0] = kp * (0.0 - robot_pos[0])
    #     desired_linear_velocity_in_gravity_frame[1] = kp * (0.0 - robot_pos[1])
    #     desired_angular_velocity_in_gravity_frame[2] = kp * (0.0 - robot.getRobotEuler()[2])
    #
    #     desired_euler_angle[0] = 0.0 * math.sin(2 * math.pi / period * (step_count-1000) * time_step)
    #     desired_euler_angle[1] = 0.0 * math.sin(2 * math.pi / period * (step_count - 1000) * time_step)
    #     desired_robot_height = 0.0 * math.sin(2 * math.pi / period * (step_count - 1000) * time_step) + 0.3
    #
    #
    #
    #     contact_trajectory = convexMPC.getContactForceTrajectory(linear_velocity_in_gravity_frame,
    #                                                              angular_velocity_in_gravity_frame,
    #                                                              euler_angle,
    #                                                              foot_pos_in_gravity_frame,
    #                                                              leg_contact_state,
    #                                                              robot_height,
    #                                                              desired_linear_velocity_in_gravity_frame,
    #                                                              desired_angular_velocity_in_gravity_frame,
    #                                                              desired_euler_angle,
    #                                                              desired_robot_height)
    #
    #
    #     robot.setFootForceInGravityFrame(0, contact_trajectory[0:3])
    #     robot.setFootForceInGravityFrame(1, contact_trajectory[3:6])
    #     robot.setFootForceInGravityFrame(2, contact_trajectory[6:9])
    #     robot.setFootForceInGravityFrame(3, contact_trajectory[9:12])

    # step_count += 1


    step_count += 1
    # nStepSimulation(5)
    robot.step()
    # p.stepSimulation()




p.disconnect()


#
plt.plot(estimated_vel, color='green', label='estimated')
plt.plot(actual_vel, color='black', label='actual')
plt.legend()

plt.figure()
plt.plot(measured_val)
plt.show()







