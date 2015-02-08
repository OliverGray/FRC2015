#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on.
"""

import wpilib

class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.stick = wpilib.Joystick(1)
        self.drive = wpilib.RobotDrive(0,1,2,3)
        self.gyro = wpilib.Gyro(0)
        self.lift1 = wpilib.Jaguar(4)
        self.lift2 = wpilib.Jaguar(5)
        #self.backclaw = wpilib.Jaguar(7)
        self.encoder = wpilib.Encoder(1,2)
        self.encoder.setDistancePerPulse(0.333)
        self.compressor = wpilib.Compressor()
        self.squeeze = wpilib.DoubleSolenoid(0,1)

        self.RobotDrive.setInvertedMotor(2,True)
        self.RobotDrive.setInvertedMotor(3,True)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
      

        self.auto_loop_counter = 0

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""



    def teleopInit(self):
        self.open = True
        self.fork = 0

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""


        self.drive.mecanumDrive_Cartesian(self.stick.getRawAxis(0), self.stick.getRawAxis(1), self.stick.getRawAxis(4), self.gyro.getAngle())

        #BackClaw goodness
        #if self.stick.getRawButton(4) == True:
         #   self.backclaw.set(1.0)
        #elif self.stick.getRawButton(1) == True:
         #   self.backclaw.set(-1.0)



        #Claw picker upper
        if self.stick.getRawButton(2) == True and self.open == False:
            self.open = True
        elif self.stick.getRawButton(2) == True and self.open == True:
            self.open = False
        if self.open == True:
            self.squeeze.set(kForward)
        elif self.open == False:
            self.squeeze.set(kReverse)


        #elevator and reset
        if self.fork == 0:
            if self.stick.getRawButton(5):
                self.liftspeed(1.0)
            elif self.stick.getRawButton(6):
                self.liftspeed(-1.0)
            else:
                self.liftspeed(0.0)
        elif self.fork == 1:
            self.liftspeed(1.0)
        elif self.fork == 2:
            self.liftspeed(-1.0)
        if self.stick.getRawButton(3) == True and self.encoder.getDistance() <= 500:
            self.fork = 1
        elif self.stick.getRawButton(3) == True and self.encoder.getDistance() >= 550:
            self.fork = 2
        if self.encoder.getDistance() >= 500 and self.encoder.getDistance() <= 550:
            self.fork = 0


    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

    def liftspeed(self, speed):
        """elevator lift call as self.liftspeed() with a float as the speed"""
        self.lift1.set(speed)
        self.lift2.set(-speed)

if __name__ == "__main__":
    wpilib.run(MyRobot)