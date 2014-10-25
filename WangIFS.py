__author__ = 'Wangj1'
# Written by Junlin Wang

from rgraphics import *
from random import randrange,choice
import numpy
import Koch_Curve
import wolframalpha
import xmlExtract
import xml.etree.cElementTree as ET
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class App:
    def __init__(self, master):
        # Initialization
        self.master = master
        self.notebook = ttk.Notebook(self.master)
        self.start = Point(-300, 0)
        self.color2 = 'white'
        self.lendict = xmlExtract.gettree()
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text = 'General')
        self.notebook.add(self.tab2, text = 'Koch Curve')

        # basic widget section in tab 1
        self.style = ttk.Style(self.master)
        self.style.configure("Title.TLabel",foreground = "#D0104c", font = 'gothics', cursor = "spider")
        self.mainlabel = ttk.Label(self.tab1, text = "Great IFS Explorer ", style = "Title.TLabel")
        self.theme = ttk.Style(self.tab1)
        self.theme.theme_use('xpnative')
        self.theme.configure("submit.TButton" ,width = 25, height = 10)
        self.submitButton = ttk.Button(self.tab1, text = "Submit", command=self.submitinput, style = "submit.TButton")
        self.saveButton = ttk.Button(self.tab1, text = "Save", command=self.save, style = "submit.TButton")
        self.graph = GraphWin(self.tab1, 700,700)
        self.graph.setBackground('black')
        self.label1 = ttk.Label(self.tab1, text = "trans")
        # color and drawing options
        self.row = 4
        self.number = 0
        self.cvar = tk.IntVar(self.master)
        self.dvar = tk.IntVar(self.master)
        self.colorcheck = ttk.Checkbutton(self.tab1, text = "Random Color", variable = self.cvar)
        self.drawoption = ttk.Checkbutton(self.tab1, text = "Instant Draw", variable = self.dvar)
        self.addinput = ttk.Button(self.tab1, text = " Add Inputs")
        self.addinput.bind("<Button-1>", lambda event: self.createInput(self.row, self.number))


        # Griding section for tab1
        self.notebook.grid(row = 1, column = 1)
        self.allinputs = []
        self.packedinputs = []

        self.createInput(4, self.number)
        self.createInput(5, self.number)
        self.createInput(6, self.number)
        self.createInput(7, self.number)
        self.createInput(8, self.number)

        self.mainlabel.grid(row = 0, column = 1, columnspan = 4, rowspan = 2)
        self.saveButton.grid(row = 3, column = 2, columnspan = 6)
        self.submitButton.grid(row = 2, column = 2, columnspan = 6, rowspan = 1)
        self.graph.grid(row = 1, column = 0, rowspan = 35, columnspan = 1)
        self.addinput.grid(row = 9, column = 6, columnspan = 4)
        self.colorcheck.grid(row = 10, column = 1, columnspan = 4)
        self.drawoption.grid(row = 10, column = 5, columnspan = 4)

        # widgets for tab2 (Koch Curve)
        self.tab2frame1 = tk.Frame(self.tab2)
        self.tab2frame2 = tk.Frame(self.tab2)
        self.graph2 = GraphWin(self.tab2frame1, 700,700)
        self.graph2.setBackground('black')
        self.graph2.setCoords(-600,-600,600,600)
        self.mainlabel2 = ttk.Label(self.tab2frame2, text = "Koch Curve", style = "Title.TLabel")
        self.submitButton2 = ttk.Button(self.tab2frame2, text = "Submit", command=self.submitinput2, style = "submit.TButton")
        self.cvar2 = tk.IntVar(self.master)
        self.dvar2 = tk.IntVar(self.master)
        self.levelLabel = tk.Label(self.tab2frame2, text = "Level:")
        self.angleLabel = tk.Label(self.tab2frame2, text = "Angle:")
        self.levelEntry = tk.Entry(self.tab2frame2)
        self.angleEntry = tk.Entry(self.tab2frame2)
        self.levelEntry.config(width = 8)
        self.angleEntry.config(width = 8)
        self.colorcheck2 = ttk.Checkbutton(self.tab2frame2, text = "Random Color", variable = self.cvar2)
        self.drawoption2 = ttk.Checkbutton(self.tab2frame2, text = "Instant Draw", variable = self.dvar2)
        self.lengthButton = ttk.Button(self.tab2frame2, text = "What's Length", command = self.calculateLength, style = "submit.TButton")
        self.lengthlabel = Text(Point(50, 460), text = '')
        self.lengthlabel.draw(self.graph2)

        # drawing section for tab 2 (Koch Curve)
        self.tab2frame1.grid(row = 0, column = 0, rowspan = 30)
        self.tab2frame2.grid(row = 0, column = 1)
        self.graph2.grid(row = 1, column = 0)

        self.mainlabel2.grid(row = 0, column = 0,columnspan = 3, pady = 1)
        self.submitButton2.grid(row = 2, column = 2, columnspan = 3, pady = 8)
        self.levelLabel.grid(row = 3, column = 1, padx = 4,pady = 8)
        self.angleLabel.grid(row = 3, column = 3, padx = 4,pady = 8)
        self.levelEntry.grid(row = 3, column = 2, padx = 4,pady = 8)
        self.angleEntry.grid(row = 3, column = 4, padx = 4,pady = 8)
        self.colorcheck2.grid(row = 4, column = 1, columnspan = 2, pady = 8)
        self.drawoption2.grid(row = 4, column = 4, columnspan = 2, pady = 8)
        self.lengthButton.grid(row = 5, column = 2, columnspan = 3, pady = 6)
    def submitinput(self):
        # Take all the inputs and draw the graph for the 1st tab
        inputs = []
        for i in self.allinputs:
            # package all the inputs
            temp = [i[0].get(), i[1].get(), i[2].get(), i[3].get(), i[4].get(), i[5].get()]
            inputs.append(temp)

        self.packedinputs = inputs
        for i in self.packedinputs:
            # convert everything from string to float
            for k in range(6):
                i[k] = float(i[k])

        dv = self.dvar.get()
        cv = self.cvar.get()
        a = self.packedinputs
        # draw a new graph -- the old one will be garbage-collected hopefully
        q = GraphWin(self.tab1,700,700, autoflush=False)
        q.setCoords(-600, -600, 600, 600)
        q.setBackground('black')
        q.grid(row = 1, column = 0, rowspan = 35, columnspan = 1)
        #a = [(94/115, 94/115, -2.5, -2.5, 1/2, 18.0/115), (0.01, 18/115, -2.5, -2.5, 1/2, 0), (37.0/115, 37.0/115, 40,40,37.0/115, 18.0/115), (40.0/115, 40.0/115, -41, -41, 1/2, 5.0/115)]

        # the drawing point -- you can watch it draw!
        p = Point(0, 0)
        cp = Circle(p, 2)
        cp.setOutline('yellow')
        cp.setFill('red')
        cp.draw(q)

        # Weighting the graph automatically
        problist = self.addprob(a)
        colors = self.colorlist(len(problist), cv)
        i = 0
        frequency = 105000

        # Draw the graph!
        while i < frequency:
            i += 1
            index = self.ranActions0(cp, problist, len(problist))
            q.plot(cp.getCenter().getX(), cp.getCenter().getY(), colors[index])
            if not dv:
                q.update()


        q.update()
    def createInput(self, row, num):
        # create a row of entries for more inputs
        self.number += 1

        d = [i for i in range(7)]
        for k in range(1, 7):
            # create four text entries and put their pointers in a list
            temp = ttk.Entry(self.tab1)
            temp.config(width = 5)
            d[k-1] = temp
            d[k-1].insert(0,'0.0')
            d[k-1].grid(row = row, column = k)
        # put them in a global list
        self.allinputs.append(d)
        temp1 = ttk.Button(self.tab1, text = 'delete')
        temp1.bind("<Button-1>", lambda event: self.delete(num))
        temp1.grid(row = row, column = 8)
        self.allinputs[num][6] = temp1

        # re-organize the GUI
        self.colorcheck.grid_forget()
        self.drawoption.grid_forget()
        self.addinput.grid_forget()
        self.row += 1
        self.addinput.grid(row = self.row, column = 6, columnspan = 4)
        self.colorcheck.grid(row = self.row + 1, column = 1, columnspan = 4)
        self.drawoption.grid(row = self.row + 1, column = 5, columnspan = 4)
    def delete(self, num):
        # delete a row of inputs
        for i in range(6):
            self.allinputs[num][i].delete(0, 'end')
            self.allinputs[num][i].insert(0, '0.0')

    def save(self):
        # save all your inputs in a text file
        # future improvement: users can input the file name
        a = open('IFScode.txt','w')
        for i in self.packedinputs:
            for k in range(6):
                a.write(str(i[k]) + ' ')
            a.write('\n')
    def addprob(self, lis):
        # adding probability weighting automatically by the area
        scale = []
        total = 0
        # scale contains the sum of scaling factors of each transformation
        for i in lis:
            scale.append(i[0] + i[1])
            total += i[0] + i[1]
        for i in range(len(lis)):
            prob = scale[i]//total
            for j in range(int(prob)):
                lis.append(lis[i])
        return lis
    def colorlist(self,num, cv):
        # make a random color list for a given index
        colorl = []
        if cv:
            for i in range(num):
                color = color_rgb(randrange(80,256), randrange(80,256), randrange(80, 256))
                colorl.append(color)
        elif not cv:
            for i in range(num):
                colorl.append('white')
        return colorl
    def quickActions(self,point, alist):
        # using matrix to calculate the new point
        matrix1 = numpy.zeros((2,2))
        matrix2 = numpy.zeros((2,1))
        matrix3 = numpy.zeros((2,1))
        matrix1[0][0] = alist[0] * numpy.cos(alist[2]/180.0 * numpy.pi)
        matrix1[0][1] = alist[1] * numpy.sin(alist[3]/180.0 * numpy.pi) * -1
        matrix1[1][0] = alist[0] * numpy.sin(alist[2]/180.0 * numpy.pi)
        matrix1[1][1] = alist[1] * numpy.cos(alist[3]/180.0 * numpy.pi)

        matrix2[0][0] = point.getCenter().getX()
        matrix2[1][0] = point.getCenter().getY()

        matrix3[0][0] = alist[4] * 600
        matrix3[1][0] = alist[5] * 600

        temp = matrix1.dot(matrix2)
        answers = temp + matrix3
        newx = answers[0][0]
        newy = answers[1][0]

        point.move(newx - point.getCenter().getX(), newy - point.getCenter().getY())

    def ranActions0(self,point, a, num):
        # a helper function that moves the new point
        index = randrange(0,num)
        self.quickActions(point,a[index])
        return index
    def contracolor(self):
        # produce a dark color and a light color
        color = color_rgb(randrange(150,256), randrange(150,256), randrange(150, 256))
        bcolor = color_rgb(randrange(0,100), randrange(0,100), randrange(0, 100))
        return color, bcolor
    def submitinput2(self):
        # Drawing function for tab2 (Koch Curve)
        # Error handling for level
        level = int(self.levelEntry.get())
        if level > 7:
            level = 7
        elif level < 0:
            level = 0

        angle = int(self.angleEntry.get())
        wangle = 0
        curlength = 1
        # the starting point
        self.start = Point(-300, 0)

        # setup the autoflash
        if self.dvar2.get():
            self.graph2 = GraphWin(self.tab2frame1, 700,700, autoflush=False)
        else:
            self.graph2 = GraphWin(self.tab2frame1, 700,700, autoflush=True)
        self.graph2.setBackground('black')

        self.graph2.setCoords(-600,-600,600,600)
        self.graph2.grid(row = 0, column = 0, rowspan = 40)

        #calculate the similarity and draws it on screen
        self.similarity()

        # determine the color option
        if self.cvar2.get():
            c, bc = self.contracolor()
            self.graph2.setBackground(bc)
            self.callme(level, angle/180.0 *numpy.pi, wangle/180.0 *numpy.pi, curlength, Koch_Curve.Length(angle),self.graph2)
            self.color2 = c


        elif not self.cvar2.get():
            self.graph2.setBackground('black')
            self.callme(level, angle/180.0 *numpy.pi, wangle/180.0 *numpy.pi, curlength, Koch_Curve.Length(angle),self.graph2)
            self.color2 = 'white'


        angle1 = 60 + int(self.angleEntry.get())
        angle2 = -60 + int(self.angleEntry.get())

    def callme(self, level, theta, angle, curlength, scale, win):
        # A recursive function that draws Koch Curve given by inputs
        if level == 0:
            end = self.line(win, angle, curlength, self.start, 600, self.color2)
            self.start = end

        else:
            # First segment
            self.callme(level - 1, theta, angle, curlength = curlength * scale, scale = scale, win = win)
            # Second segment
            angle2 = angle + theta
            self.callme(level - 1, theta, angle2, curlength = curlength * scale, scale = scale, win = win)
            # Third segment
            angle3 = angle - theta
            self.callme(level - 1, theta, angle3, curlength = curlength * scale, scale = scale, win = win)
            # Fourth segment
            self.callme(level - 1, theta,  angle, curlength = curlength * scale, scale = scale, win = win)
    def line(self, win, slope, length, oripoint, scale, color):
        # Draw the line with input point and color
        end = Point(oripoint.getX() + numpy.cos(slope) * length * scale, numpy.sin(slope) * length * scale + oripoint.getY())
        temp = Line(oripoint, end)
        temp.setFill(color)
        temp.draw(win)
        return end
    def similarity(self):
        # A function that calculate the similarity
        r = 1.0/(2 * numpy.cos(int(self.angleEntry.get())/180.0 * numpy.pi) + 2)
        n = 100
        NofR = 1.0/r * (4**(int(n - 1)))
        OverR = (1.0/r)**n
        similarity = numpy.log10(NofR)/numpy.log10(OverR)
        self.similarityLabel = Text(Point(500,550),"Similarity %0.3f" % (similarity))
        self.similarityLabel.setTextColor('white')
        self.similarityLabel.draw(self.graph2)
    def calculateLength(self):
        # A function that returns the length of the Koch Curve given by inputs
        # This function uses API from Wolframe Alpha, which gives various interesting results
        # I already have the length library of level inputs 1 - 7 and theta input 10 - 90.  So the program
        # doesn't need to ask wolframe alpha every time (which costs like 5 seconds)

        # If your input level or theta has never been inputted before, it will take 5 seconds, but once
        # it's benn inputted, the program will save that input so that next time it will be there.
        self.lengthlabel.undraw()
        a = int(self.angleEntry.get())
        level = int(self.levelEntry.get())
        segmentLength = 2.0 * numpy.cos(a/180.0 * numpy.pi) + 2
        base = 4.0/segmentLength
        length = base**level
        ininch = length * 6
        text = ''

        # if the input is already in the length library, just use it
        if 'finches%0.2f' % (ininch) in self.lendict.keys():

            text = self.lendict['finches%0.2f' % (ininch)]
            text = text.split('  ')
            temp = randrange(0, len(text))
            text = text[temp].replace('~~', '')

        # if the input is not in the length library, gets it from Wolframe Alpha and saves it.
        else:
            appid = 'KYKTRX-LJKP3HX2YQ'
            client = wolframalpha.Client(appid)
            tlist = ''
            res = client.query('how long is %0.2f' % (ininch) + ' inches')
            for pod in res.pods:
                if pod.text[1] == '~':
                    new = pod.text.encode('ascii', 'replace')
                    new = new.replace('?', '*')
                    tlist = tlist + new + ' '
            text = tlist.split('  ')
            temp = randrange(0, len(text))
            text = text[temp].replace('~~', '')

            self.tree = ET.parse('learninglength.xml')
            self.root = self.tree.getroot()
            new = ET.SubElement(self.root, 'finches%0.2f' % (ininch))
            new.text = tlist
            self.root.append(new)
            self.tree.write("learninglength.xml")
            self.lendict = xmlExtract.gettree()

        self.lengthlabel = Text(Point(10, 460), text)
        self.lengthlabel.setTextColor('white')
        self.lengthlabel.draw(self.graph2)

def reflectionbylinearf(x, y, lf):
    # reflect the image base on a linear line
    # vh is a linear function
    # Not implemented in the APP
    bag = []
    coe = []
    # extract the coefficients from the linear function
    for i in range(len(lf)):
        if lf[i] == 'x':
            for j in range(i + 2, len(lf)):
                coe.append(lf[j])
            break
        bag.append(lf[i])

    bag = int(''.join(bag))
    coe = int(''.join(coe))
    # calculate the slope of the perpendicular line
    nslope = -1.0/bag

    b = y - nslope * x

    neu = (b - coe)/(bag - nslope)
    # calculate the x-value and y-value of the reflected point
    newx = 2.0 * neu - x
    newy = newx * nslope + b
    return newx, newy





start = Point(-300, 0)
# main()
root = tk.Tk()
root.title("IFS")
root.geometry("1000x700")
newapp = App(root)
root.mainloop()
