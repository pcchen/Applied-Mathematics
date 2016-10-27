import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import time


def zero(x):
	return 0
def slope_one(x, b=0):
	return x+b
def slope_minus_one(x, b=19):
	return b-x
def slope_one_third(x, b=0):
        return x/3 + b
def sin(x):
	return np.sin(x*12/180*np.pi)
def cos(x):
	return np.cos(x*12/180*np.pi)

fig = plt.figure()
ax = fig.gca(projection="3d")
plt.ion()

class plate:
	def __init__(self, sides=4, length=10):
		self.sides=sides
		self.w=length
		self.h=length
		self.dots=[]
	
	def set_points(self):
		if self.sides == 4:
			self.dots = np.zeros(shape=(self.w, self.h))
		elif self.sides == 0:
			for i in range(self.w+1):
				if i == 0:
					nums = 1
					self.dots = [[0]]
				else:
					nums = 2**(2*i)
					self.dots.append([0]*nums)

	def set_BC(self, f_xu=zero, f_xl=zero, f_yu=zero, f_yl=zero):
		if self.sides == 4:
			x_max = self.w
			y_max = self.h
			for i in range(x_max):
				self.dots[i][0] = f_xu(i)
			for i in range(x_max):
				self.dots[i][y_max-1] = f_xl(i)
			for i in range(y_max):
				self.dots[0][i] = f_yu(i)
			for i in range(y_max):
				self.dots[x_max-1][i] = f_yl(i)
		elif self.sides == 0:
			l = len(self.dots[-1])
			for i in range(l):
				self.dots[-1][i] = f_xu(i)

	def average(self, error=0.001):
		is_balance = True
		if self.sides == 4:
			row = self.w
			col = self.h
			for i in range(row-2):
				i += 1
				for j in range(col-2):
					j += 1
					tmp = (self.dots[i-1][j] + self.dots[i+1][j] + self.dots[i][j-1] + self.dots[i][j+1])/4
					if abs(tmp - self.dots[i][j]) > error:
						self.dots[i][j] = tmp
						is_balance = False
		elif self.sides == 0:
			radius = self.w
			tmp = 0
			for i in range(radius):
				i = radius - i
				dot_num = len(self.dots[i]) 
				if i == 0:
					for j in range(self.dots[i+1]):
						tmp += dots[i+1][j]
					if abs(tmp/4 - self.dots[i][0]) > error:
						self.dots[i][0] = tmp
						is_balance = False
				elif i == 1:
					for j in range(dot_num):
						tmp = (self.dots[i-1][0] + self.dots[i+1][j*2] + self.dots[i][j-1] + self.dots[i][(j+1)%4])/4
						if abs(tmp - self.dots[i][j]) > error:
							self.dots[i][j] = tmp
							is_balance = False
				else:
					for j in range(dot_num):
						if j%2 == 0:
							tmp = (self.dots[i-1][j//2] + self.dots[i+1][j*2] + self.dots[i][j-1] + self.dots[i][(j+1)%dot_num])/4
						else:
							avg = (self.dots[i-1][j//2] + self.dots[i-1][j//2+1])/2
							tmp = (avg + self.dots[i+1][j*2] + self.dots[i][j-1] + self.dots[i][(j+1)%dot_num])

						if abs(tmp -self.dots[i][j]):
							self.dots[i][j] = tmp
							is_balance = False

def draw_plate(num, plate, error):
		if plate.sides == 4:
			xs = np.arange(1, plate.w+1)
			ys = np.arange(1, plate.h+1)
			X, Y = np.meshgrid(xs, ys)
		ax.clear()
		plate.average(error)
		surf = ax.plot_surface(X, Y, plate.dots, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)


sides = int(input("Sides:"))
length = int(input("Length:"))
error = float(input("Error:"))

pl = plate(sides, length)
pl.set_points()
##set_BC(dots, slope_one, slope_one, slope_minus_one, slope_minus_one)
pl.set_BC(cos, cos, cos, cos)


ani = animation.FuncAnimation(fig, draw_plate, fargs=(pl, error), interval=100)
plt.show()
##pl.dynamic_draw(error)
