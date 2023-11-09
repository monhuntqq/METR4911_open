import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
import tkinter as tk

# init motor conditions first for motor hat
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

class MyBtn(tk.Button):
    # set function to call when mouse is held and draged
    def set_down(self,fn):
        self.bind('<B1-Motion>',fn)

    # set function to call when clicked
    def set_click(self,fn):
        self.bind('<Button-1>',fn)
     
    # set function to be called when released
    def set_up(self,fn):
        self.bind('<ButtonRelease-1>',fn)

class BtnFrame(tk.Frame):
    # create a global variable to indicate angle of turn and to prevent over turning
    M1Rot = 0

    def __init__(self,master,*args,**kwargs):
        tk.Frame.__init__(self,master,*args,**kwargs)
        self.rowconfigure([0,1], minsize = 5)
        self.columnconfigure([0,1,2,3,4], minsize = 5)
        
        # create the button and set callback functions for holding to turn continuously (left)
        btn_1 = MyBtn(self,text = '''Left Rotate\non Hold & Drag''')
        btn_1.set_up(self.LeftRot_on_up)
        btn_1.set_down(self.LeftRot_on_down)
        btn_1.grid(row = 0, column = 0, sticky="nsew")

        # create the button and set callback functions for clicking to turn in one go (left)
        btn_1_90 = MyBtn(self,text = '''Left 90deg Turn\non Press''')
        btn_1_90.set_up(self.LeftRot_on_up)
        btn_1_90.set_click(self.Left90_on_down)
        btn_1_90.grid(row = 1, column = 0, sticky="nsew")

        # same process for Right Turning functions
        btn_2 = MyBtn(self,text = '''Right Rotate\non Hold & Drag''')
        btn_2.set_up(self.RightRot_on_up)
        btn_2.set_down(self.RightRot_on_down)
        btn_2.grid(row = 0, column = 4, sticky="nsew")

        btn_2_90 = MyBtn(self,text = '''Right 90deg Turn\non Press''')
        btn_2_90.set_up(self.RightRot_on_up)
        btn_2_90.set_click(self.Right90_on_down)
        btn_2_90.grid(row = 1, column = 4, sticky="nsew")

        # same process for Clockwise Turning of functionality head motor 2
        btn_3 = MyBtn(self,text = 'Clockwise Rotate \non Hold & Drag')
        btn_3.set_up(self.ClocRot_on_up)
        btn_3.set_down(self.ClocRot_on_down)
        btn_3.grid(row = 0, column = 1, sticky="nsew")

        btn_3_90 = MyBtn(self,text = 'Clockwise \n90deg Turn \non Press')
        btn_3_90.set_up(self.ClocRot_on_up)
        btn_3_90.set_click(self.Cloc90_on_down)
        btn_3_90.grid(row = 1, column = 1, sticky="nsew")

        # same process for Anti-Clockwise Turning of functionality head motor 2
        btn_4 = MyBtn(self,text = 'Anti-Clockwise Rotate \non Hold & Drag')
        btn_4.set_up(self.AClocRot_on_up)
        btn_4.set_down(self.AClocRot_on_down)
        btn_4.grid(row = 0, column = 3, sticky="nsew")

        btn_4_90 = MyBtn(self,text = 'Anti-Clockwise \n90deg Turn \non Press')
        btn_4_90.set_up(self.AClocRot_on_up)
        btn_4_90.set_click(self.ACloc90_on_down)
        btn_4_90.grid(row = 1, column = 3, sticky="nsew")

        # an individual stop button to turn off motors and reset step variable on command
        btn_s = MyBtn(self,text = 'Stop Motor')
        btn_s.set_click(self.Stop_on_down)
        btn_s.grid(row = 1, column = 2, sticky="nsew")

        btn_r = MyBtn(self,text = 'Return Motor 1 \nto origin')
        btn_r.set_click(self.ReturnM1_on_down)
        btn_r.grid(row = 0, column = 2, sticky="nsew")

    def LeftRot_on_down(self,x):
        # setup motor1 for directional control of farmbot head
        Motor1.SetMicroStep('hardward','fullstep')

        # using turning step to mark angle so motor 1 won't go over 90deg
        if self.M1Rot < 500:
            self.M1Rot += 1
            Motor1.TurnStep(Dir='forward', steps=1, stepdelay = 0.005)
        else:
            print("Motor 1 angle goes over 90 def, need to stop")

    def Left90_on_down(self,x):
        # setup motor1 for 90deg-one-go directional control of farmbot head
        Motor1.SetMicroStep('hardward','fullstep')
        if self.M1Rot < 50: 
            self.M1Rot += 500
            Motor1.TurnStep(Dir='forward', steps=500, stepdelay = 0.005)
        else:
            print("Motor 1 angle will go over 100 deg, must stop")

    # function called when released
    def LeftRot_on_up(self,x):
        
        Motor1.SetMicroStep('hardward','fullstep')
        if self.M1Rot < 500:
            self.M1Rot += 1
            Motor1.TurnStep(Dir='forward', steps=1, stepdelay = 0.005)
        else:
            print("Motor 1 angle goes over 90 deg, need to stop")

    # function called when clicked or held & draged
    def RightRot_on_down(self,x):
        
        Motor1.SetMicroStep('hardward','fullstep')
        if self.M1Rot > -500:
            self.M1Rot -= 1
            Motor1.TurnStep(Dir='backward', steps=1, stepdelay = 0.005)
        else:
            print("Motor 1 angle goes over 90 deg, need to stop")

    def Right90_on_down(self,x):
        
        Motor1.SetMicroStep('hardward','fullstep')
        if self.M1Rot > -50:
            self.M1Rot -= 500
            Motor1.TurnStep(Dir='backward', steps=500, stepdelay = 0.005)
        else:
            print("Motor 1 angle will go over 100 deg, must stop")

    def RightRot_on_up(self,x):
        
        Motor1.SetMicroStep('hardward','fullstep')
        if self.M1Rot > -500:
            self.M1Rot -= 1
            Motor1.TurnStep(Dir='backward', steps=1, stepdelay = 0.005)
        else:
            print("Motor 1 angle goes over 90 deg, need to stop")

    def ClocRot_on_down(self,x):
        
        Motor2.SetMicroStep('hardward','fullstep')
        Motor2.TurnStep(Dir='forward', steps=1, stepdelay = 0.005)

    def Cloc90_on_down(self,x):
        
        Motor2.SetMicroStep('hardward','fullstep')
        Motor2.TurnStep(Dir='forward', steps=259, stepdelay = 0.005)

    # function called when released
    def ClocRot_on_up(self,x):
        
        Motor2.SetMicroStep('hardward','fullstep')
        Motor2.TurnStep(Dir='forward', steps=1, stepdelay = 0.005)

    def AClocRot_on_down(self,x):
        
        Motor2.SetMicroStep('hardward','fullstep')
        Motor2.TurnStep(Dir='backward', steps=1, stepdelay = 0.005)

    def ACloc90_on_down(self,x):
        
        Motor2.SetMicroStep('hardward','fullstep')
        Motor2.TurnStep(Dir='backward', steps=259, stepdelay = 0.005)

    def AClocRot_on_up(self,x):
        
        Motor2.SetMicroStep('hardward','fullstep')
        Motor2.TurnStep(Dir='backward', steps=1, stepdelay = 0.005)

    def Stop_on_down(self,x):

        Motor1.SetMicroStep('hardward','fullstep')

        # specify a stop function to return motor1 and stop motors
        if self.M1Rot > 0:
            Motor1.TurnStep(Dir='backward', steps=self.M1Rot, stepdelay = 0.005)
            self.M1Rot = 0
            Motor1.Stop()
            Motor2.Stop()
            print("Both motors stop.")
        elif self.M1Rot < 0:
            Motor1.TurnStep(Dir='forward', steps=abs(self.M1Rot), stepdelay = 0.005)
            self.M1Rot = 0
            Motor1.Stop()
            Motor2.Stop()
            print("Both motors stop.")
        else:
            Motor1.Stop()
            Motor2.Stop()
            print("Both motors already at origin, stop.")
    
    def ReturnM1_on_down(self,x):

        Motor1.SetMicroStep('hardward','fullstep')
        
        if self.M1Rot > 0:
            Motor1.TurnStep(Dir='backward', steps=self.M1Rot, stepdelay = 0.005)
            self.M1Rot = 0
            print("Motor 1 returns to origin.")
        elif self.M1Rot < 0:
            Motor1.TurnStep(Dir='forward', steps=abs(self.M1Rot), stepdelay = 0.005)
            self.M1Rot = 0
            print("Motor 1 returns to origin.")
        else:
            print("Motor 1 already returned to origin.")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
               
        self.title('Motor Button Test')
        BtnFrame(self).pack(fill = tk.BOTH,
                            expand = True,)

# create and run an App object
App().mainloop()