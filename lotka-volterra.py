import plotly.graph_objects as go
import tkinter as tk
import plotly.io as pio
from tkinter import *
from PIL import ImageTk, Image
import os

root = tk.Tk()
frame = Frame(root)

class GUI:
    def __init__(self):
        self.frame = Frame(root)
        self.frame.pack(side="top",expand=True,fill="both")
        root.title("NMD population models")
    
    def clearFrame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
    
    def drawGraph(self,a,b,c,d,x0,y0):

        system = equations()

        system.setY0(y0)
        system.setX0(x0)

        system.setAlpha(a)
        system.setBeta(b)
        system.setGamma(c)
        system.setDelta(d)

        system.setIterations(300)
        system.compute()
        system.setStepSize(0.01)

        timeList = system.getTimeList()
        xValues = system.get_X_VALUES()
        yValues = system.get_Y_VALUES()

        trace1 = go.Scatter(x = timeList, y=yValues, mode='lines', name='Predators')
        trace2 = go.Scatter(x = timeList, y=xValues, mode='lines', name='Prey')

        # Create figure object and add traces
        fig = go.Figure()
        fig.add_trace(trace1)
        fig.add_trace(trace2)

        # Update layout
        fig.update_layout(
            title= f'Population forecast with Lotka-Volterra',
            xaxis_title='Time',
            yaxis_title='Population size (# of animals)'
        )

        filename = 'render.png'
        pio.write_image(fig, filename)
        print(f'Plot saved as {filename}')

        self.displayGraph("render")

    def drawGraphCompetitiveLV(self,r1,r2,alpha1,alpha2,K1,K2,x0,y0):
        system = equations()

        system.setIterations(80)
        system.setR1(r1)
        system.setR2(r2)
        system.setK1(K1)
        system.setK2(K2)
        system.setalphaone(alpha1)
        system.setalphatwo(alpha2)

        system.setX0(x0)
        system.setY0(y0)

        system.competitive_Lotka_Volterra_compute()

        timeList = system.getTimeList()
        xValues = system.get_X_VALUES()
        yValues = system.get_Y_VALUES()

        trace1 = go.Scatter(x = timeList, y=yValues, mode='lines', name='Species 1')
        trace2 = go.Scatter(x = timeList, y=xValues, mode='lines', name='Species 2')

        # Create figure object and add traces
        fig = go.Figure()
        fig.add_trace(trace1)
        fig.add_trace(trace2)

        # Update layout
        fig.update_layout(
            title= f'Population forecast with Lotka-Volterra',
            xaxis_title='Time',
            yaxis_title='Population size (# of animals)'
        )

        filename = 'render_competitive.png'
        pio.write_image(fig, filename)
        print(f'Plot saved as {filename}')

        self.displayGraph("render_competitive")


    def render_PPPage(self):
        self.clearFrame()

        self.frame.welcome_label2 = Label(self.frame, text = "Welcome to the simple Lotka - Volterra model")
        self.frame.welcome_label2.grid(row = 1, column = 4)

        self.frame.return_home1 = Button(self.frame, text = "return to home page", command = self.renderHome)
        self.frame.return_home1.grid(row = 3, column = 4)

        self.frame.equation1_label = Label(self.frame, text = "dx/dt = ax - bxy")
        self.frame.equation2_label = Label(self.frame, text = "dy/dt = cxy - dy")

        self.frame.equation1_label.grid(row = 5, column = 4)
        self.frame.equation2_label.grid(row = 7, column = 4)

        self.frame.get_param_a = Entry(self.frame, text = 'a')
        self.frame.get_param_b = Entry(self.frame, text = 'b')
        self.frame.get_param_c = Entry(self.frame, text = 'c')
        self.frame.get_param_d = Entry(self.frame, text = 'd')

        self.frame.get_param_a.grid(row = 9, column = 4)
        self.frame.get_param_b.grid(row = 12, column = 4)
        self.frame.get_param_c.grid(row = 15, column = 4)
        self.frame.get_param_d.grid(row = 19, column = 4)

        self.frame.enter_a_label = Label(self.frame, text = "enter a: ")
        self.frame.enter_b_label = Label(self.frame, text = "enter b: ")
        self.frame.enter_c_label = Label(self.frame, text = "enter c: ")
        self.frame.enter_d_label = Label(self.frame, text = "enter d: ")

        self.frame.enter_a_label.grid(row = 9, column = 1)
        self.frame.enter_b_label.grid(row = 12, column = 1)
        self.frame.enter_c_label.grid(row = 15, column = 1)
        self.frame.enter_d_label.grid(row = 19, column = 1)


        self.frame.middle_label = Label(self.frame, text = "initial conditions: ")
        self.frame.middle_label.grid(row = 21, column = 4)
    
        self.frame.enter_x0_entry = Entry(self.frame)
        self.frame.enter_y0_entry = Entry(self.frame)

        self.frame.enter_x0_entry.grid(row = 23, column = 4)
        self.frame.enter_y0_entry.grid(row = 25, column = 4)

        self.frame.enter_x0_label = Label(self.frame, text = "enter x(0): ")
        self.frame.enter_y0_label = Label(self.frame, text = "enter y(0): ")

        self.frame.enter_x0_label.grid(row = 23, column = 1)
        self.frame.enter_y0_label.grid(row = 25, column = 1)


        self.frame.render_graph_button = Button(self.frame, text = "Render Graph", command = lambda : self.drawGraph(
            float(self.frame.get_param_a.get()),
            float(self.frame.get_param_b.get()),
            float(self.frame.get_param_c.get()),
            float(self.frame.get_param_d.get()),
            float(self.frame.enter_x0_entry.get()),
            float(self.frame.enter_y0_entry.get())
        ))
        self.frame.render_graph_button.grid(row = 27, column = 4)
    
    def displayGraph(self,name): 
        img = Image.open(f"{name}.png")
        img = img.resize((650, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.frame.panel = Label(root, image=img)
        self.frame.panel.image = img
        self.frame.panel.pack()

    def render_PPLVpage(self):
        self.clearFrame()

        self.frame.welcome_label2 = Label(self.frame, text = "Welcome to the competitve Lotka - Volterra model")
        self.frame.welcome_label2.grid(row = 1, column = 4)

        self.frame.return_home1 = Button(self.frame, text = "return to home page", command = self.renderHome)
        self.frame.return_home1.grid(row = 3, column = 4)

        self.frame.equation1_label = Label(self.frame, text = "dx/dt = r1 * x (1 - (x + ay)/K1)")
        self.frame.equation2_label = Label(self.frame, text = "dy/dt = r2 * y (1 - (y + bx)/K2)")

        self.frame.equation1_label.grid(row = 5, column = 4)
        self.frame.equation2_label.grid(row = 7, column = 4)

        self.frame.get_param_gr1 = Entry(self.frame, text = 'r1')
        self.frame.get_param_gr2 = Entry(self.frame, text = 'r2')
        self.frame.get_param_k1 = Entry(self.frame, text = 'k1')
        self.frame.get_param_k2 = Entry(self.frame, text = 'k2')
        self.frame.get_param_a = Entry(self.frame, text = "a")
        self.frame.get_param_b = Entry(self.frame, text = 'b')


        self.frame.get_param_gr1.grid(row = 9, column = 4)
        self.frame.get_param_gr2.grid(row = 12, column = 4)
        self.frame.get_param_k1.grid(row = 15, column = 4)
        self.frame.get_param_k2.grid(row = 19, column = 4)
        self.frame.get_param_a.grid(row = 22, column = 4)
        self.frame.get_param_b.grid(row = 25, column = 4)


        self.frame.enter_r1_label = Label(self.frame, text = "enter r1: ")
        self.frame.enter_r2_label = Label(self.frame, text = "enter r2: ")
        self.frame.enter_k1_label = Label(self.frame, text = "enter K1: ")
        self.frame.enter_k2_label = Label(self.frame, text = "enter K2: ")
        self.frame.enter_a_label = Label(self.frame, text = "enter a: ")
        self.frame.enter_b_label = Label(self.frame, text = "enter b: ")

        self.frame.enter_r1_label.grid(row = 9, column = 1)
        self.frame.enter_r2_label.grid(row = 12, column = 1)
        self.frame.enter_k1_label.grid(row = 15, column = 1)
        self.frame.enter_k2_label.grid(row = 19, column = 1)
        self.frame.enter_a_label.grid(row = 22, column = 1)
        self.frame.enter_b_label.grid(row = 25, column = 1)


        self.frame.middle_label = Label(self.frame, text = "initial conditions: ")
        self.frame.middle_label.grid(row = 28, column = 4)
    
        self.frame.enter_x0_entry = Entry(self.frame)
        self.frame.enter_y0_entry = Entry(self.frame)

        self.frame.enter_x0_entry.grid(row = 31, column = 4)
        self.frame.enter_y0_entry.grid(row = 34, column = 4)

        self.frame.enter_x0_label = Label(self.frame, text = "enter x(0): ")
        self.frame.enter_y0_label = Label(self.frame, text = "enter y(0): ")

        self.frame.enter_x0_label.grid(row = 31, column = 1)
        self.frame.enter_y0_label.grid(row = 34, column = 1)


        self.frame.render_graph_button = Button(self.frame, text = "Render Graph", command = lambda : [self.drawGraphCompetitiveLV( #drawGraphCompetitiveLV(r1,r2,alpha1,alpha2,K1,K2,x0,y0)
            float(self.frame.get_param_gr1.get()),
            float(self.frame.get_param_gr2.get()),
            float(self.frame.get_param_a.get()),
            float(self.frame.get_param_b.get()),
            float(self.frame.get_param_k1.get()),
            float(self.frame.get_param_k2.get()),
            float(self.frame.enter_x0_entry.get()),
            float(self.frame.enter_y0_entry.get())
        ),
        self.displayGraph("render_competitive")])
        self.frame.render_graph_button.grid(row = 37, column = 4)

    def start(self):
        self.frame.welcome_label = Label(self.frame, text = "Welcome to the population modelling interface")
        self.frame.welcome_label.grid(row = 1, column = 1)

        self.frame.goto_basic_model = Button(self.frame, text = "go to simple predator - prey modelling", command = self.render_PPPage)
        self.frame.goto_basic_model.grid(row = 5, column =1)

        self.frame.goto_comp_model = Button(self.frame, text = "go to competitive lotka - volterra", command = self.render_PPLVpage)
        self.frame.goto_comp_model.grid(row = 7, column = 1)

        self.frame.exit_button = Button(self.frame, text = "exit", command = exit)
        self.frame.exit_button.grid(row = 9, column = 1)
    
    def renderHome(self):
        self.clearFrame()
        self.start()



class equations:
    def __init__(self):
        ########PARAMETERS########
        self._alpha = 0.0
        self._beta = 0.0
        self._gamma = 0.0
        self._delta = 0.0
        self._X0 = 0.0
        self._Y0 = 0.0

        ########COMPETTITIVE LOTKA VOLTERRA PARAMS################
        self._r1 = 0.0
        self._r2 = 0.0
        self._K1 = 0.0
        self._K2 = 0.0
        self._alpha1 = 0.0
        self._alpha2 = 0.0

        ########COMPUTATION########
        self.Iterations = 0
        self._stepSize = 0.01

        ########OUTPUTS########
        self.X_VALUES = []
        self.Y_VALUES = []
        self.time_list = [0, self._stepSize, 2 * self._stepSize]
  
    def setStepSize(self,SS):
        print(SS)
        self._stepSize = SS
    
    def setY0(self,Y0):
        self._Y0 = Y0
    
    def setX0(self, X0):
        self._X0 = X0

    def setAlpha(self,alpha):
        self._alpha = alpha
    
    def setBeta(self,beta):
        self._beta = beta
    
    def setGamma(self,gamma):
        self._gamma = gamma
    
    def setDelta(self,delta):
        self._delta = delta
    
    def setIterations(self,iter):
        self.Iterations = iter
    
    def setR1(self,arOne):
        self._r1 = arOne
    
    def setR2(self,arTwo):
        self._r2 = arTwo
    
    def setK1(self,kayOne):
        self._K1 = kayOne
    
    def setK2(self,kayTwo):
        self._K2 = kayTwo
    
    def setalphaone(self,alpha1):
        self._alpha1 = alpha1
    
    def setalphatwo(self, alpha2):
        self._alpha2 = alpha2
    
    def compute(self):
        #let's compute x1 and y1

        x_by_dt = (self._alpha * self._X0 - self._beta * self._Y0 * self._X0)
        y_by_dt = (self._delta * self._X0 * self._Y0 - self._gamma * self._Y0)

        X1 = self._X0 + (x_by_dt) * self._stepSize
        Y1 = self._Y0 + (y_by_dt) * self._stepSize

        self.X_VALUES.append(X1)
        self.Y_VALUES.append(Y1)

        for i in range(1,int((self.Iterations / self._stepSize))):

            self.time_list.append(i * self._stepSize)

            x_by_dt = (self._alpha * self.X_VALUES[i - 1] - self._beta * self.X_VALUES[i - 1] * self.Y_VALUES[i - 1])
            y_by_dt = (self._delta * self.X_VALUES[i - 1] * self.Y_VALUES[i - 1] - self._gamma * self.Y_VALUES[i - 1])

            X_I = self.X_VALUES[i - 1] + x_by_dt * self._stepSize
            Y_I = self.Y_VALUES[i - 1] + y_by_dt * self._stepSize

            self.X_VALUES.append(X_I)
            self.Y_VALUES.append(Y_I)

    def resetComputation(self):
    
        self.X_VALUES = []
        self.Y_VALUES = []
        self.time_list = [0, self.stepSize, 2 * self._stepSize]
    
    def competitive_Lotka_Volterra_compute(self):
        self.time_list = [0]
        self.X_VALUES.append(self._X0)
        self.Y_VALUES.append(self._Y0)

        for i in range(1, int(self.Iterations/self._stepSize)):
            self.time_list.append(i * self._stepSize)

            dx_by_dt = (self._r1 * self.X_VALUES[i - 1]) * (1 - ((self.X_VALUES[i - 1] + self.Y_VALUES[i - 1] * self._alpha1) / (self._K1)))
            dy_by_dt = (self._r2 * self.Y_VALUES[i - 1]) * (1 - ((self.Y_VALUES[i - 1] + self.X_VALUES[i - 1] * self._alpha2) / (self._K2)))

            X_I = self.X_VALUES[i - 1] + self._stepSize * dx_by_dt
            Y_I = self.Y_VALUES[i - 1] + self._stepSize * dy_by_dt


            self.X_VALUES.append(X_I)
            self.Y_VALUES.append(Y_I)

    def get_X_VALUES(self):
        return self.X_VALUES

    def get_Y_VALUES(self):
        return self.Y_VALUES

    def getTimeList(self):
        return self.time_list


def testMain2():
    gui1 = GUI()
    gui1.start()
    root.mainloop()

def testMain3():
    system = equations()

    system.setIterations(50)
    system.setR1(0.3)
    system.setR2(0.5)
    system.setK1(200)
    system.setK2(250)
    system.setalphaone(0.1)
    system.setalphatwo(0.2)

    system.setX0(35)
    system.setY0(30)

    system.competitive_Lotka_Volterra_compute()

    timeList = system.getTimeList()
    xValues = system.get_X_VALUES()
    yValues = system.get_Y_VALUES()

    trace1 = go.Scatter(x = timeList, y=yValues, mode='lines', name='Species 1')
    trace2 = go.Scatter(x = timeList, y=xValues, mode='lines', name='Species 2')

    # Create figure object and add traces
    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    # Update layout
    fig.update_layout(
        title= f'Population forecast with Lotka-Volterra',
        xaxis_title='Time',
        yaxis_title='Population size (# of animals)'
    )

    filename = 'render_competitive.png'
    pio.write_image(fig, filename)
    print(f'Plot saved as {filename}')

    

testMain2()


    

