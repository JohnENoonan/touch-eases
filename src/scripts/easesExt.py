import math

def clamp(num, min_value, max_value):
	return max(min(num, max_value), min_value)

def yFromT(t, E, F, G, H):
	return (E * (t * t * t) + F * (t * t) + G * t + H)

def xFromT(t, A, B, C, D):
	return (A * (t * t * t) + B * (t * t) + C * t + D)

def slopeFromT(t,A,B,C):
	return (1.0 / (3.0 * A * t * t + 2.0 * B * t + C))

class EasesExt:

	c1 = 1.70158
	c2 = c1 * 1.525
	c3 = c1 + 1
	c4 = (2 * math.pi) / 3
	c5 = (2 * math.pi) / 4.5

	def __init__(self, ownercomp):
		self.ownercomp = ownercomp
		self.table = op("easing_list")

		# create method list
		method_list = [method for method in dir(EasesExt) if method.startswith('Ease') ]
		
		self.table.clear()
		for method in method_list:
			self.table.appendRow([method])

		op("replicator1").par.recreateall.pulse()

	def bounceOut(self, x):
		"""
		bounce helper
		"""
		n1 = 7.5625
		d1 = 2.75

		if (x < 1 / d1):
			return n1 * x * x
		elif (x < 2 / d1):
			x -= 1.5 / d1
			return n1 * x * x + 0.75
		elif (x < 2.5 / d1):
			x -= 2.25 / d1
			return n1 * x * x + 0.9375
		else:
			x -= 2.625 / d1
			return n1 * x * x + 0.984375

	def CubicBezier(self, x, firstx, firsty, lastx, lasty, tx=1.0, ty=1.0):
		"""
		Implmentation taken from https://github.com/armadillu/ofxAnimatable/blob/main/src/ofxAnimatable.cpp
		x: tween value
		first[x,y]: first control points
		last[x,y]: last control points
		"""
		y0a = 0.00      # initial y
		x0a = 0.00      # initial x
		y1a = firsty    # 1st influence y
		x1a = firstx    # 1st influence x
		y2a = lasty     # 2nd influence y
		x2a = lastx     # 2nd influence x
		y3a = ty        # final y
		x3a = tx        # final x

		A = x3a - 3.0 * x2a + 3.0 * x1a - x0a
		B = 3.0 * x2a - 6.0 * x1a + 3.0 * x0a
		C = 3.0 * x1a - 3.0 * x0a
		D = x0a

		E = y3a - 3.0 * y2a + 3.0 * y1a - y0a
		F = 3.0 * y2a - 6.0 * y1a + 3.0 * y0a
		G = 3.0 * y1a - 3.0 * y0a
		H = y0a

		# Solve for t given x (using Newton-Raphelson), then solve for y given t.
		# Assume for the first guess that t = x.
		currentt = x
		nRefinementIterations = 5
		for i in range(nRefinementIterations):
			currentx = xFromT (currentt,A,B,C,D)
			currentslope = slopeFromT(currentt,A,B,C)
			currentt -= (currentx - x)*(currentslope)
			currentt = clamp(currentt, 0.0, 1.0)
	
		return yFromT(currentt,E,F,G,H)

	#### eases ####
	
	def EaseInQuad(self, x): 
		return x * x
	
	def EaseOutQuad(self, x): 
		return 1 - (1 - x) * (1 - x)

	def EaseInOutQuad(self, x): 
		return 2 * x * x if (x < 0.5) else 1 - pow(-2 * x + 2, 2) / 2
	
	def EaseInCubic(self, x):
		return x * x * x
	
	def EaseOutCubic(self, x): 
		return 1 - pow(1 - x, 3)
	
	def EaseInOutCubic(self, x):
		return 4 * x * x * x if (x < 0.5) else 1 - pow(-2 * x + 2, 3) / 2
	
	def EaseInQuart(self, x): 
		return x * x * x * x
	
	def EaseOutQuart(self, x):
		return 1 - pow(1 - x, 4)
	
	def EaseInOutQuart(self, x):  
		return 8 * x * x * x * x if (x < 0.5) else 1 - pow(-2 * x + 2, 4) / 2
	
	def EaseInQuint(self, x):
		return x * x * x * x * x
	
	def EaseOutQuint(self, x):
		return 1 - pow(1 - x, 5)
	
	def EaseInOutQuint(self, x): 
		return 16 * x * x * x * x * x if (x < 0.5) else 1 - pow(-2 * x + 2, 5) / 2

	def EaseInSine(self, x):
		return 1 - math.cos((x * math.pi) / 2)

	def EaseOutSine(self, x):
		return math.sin((x * math.pi) / 2)

	def EaseInOutSine(self, x):
		return -(math.cos(math.pi * x) - 1) / 2

	def EaseInExpo(self, x):
		return 0 if (x == 0) else pow(2, 10 * x - 10)
	
	def EaseOutExpo(self, x): 
		return 1 if (x < 1) else 1 - pow(2, -10 * x)
	
	def EaseInOutExpo(self, x):
		if x == 0:
			return 0
		elif x == 1:
			return 1
		elif x < .05:
			return pow(2, 20 * x - 10) / 2
		else:
			return (2 - pow(2, -20 * x + 10)) / 2
	
	def EaseInCirc(self, x):
		return 1 - math.sqrt(1 - pow(x, 2))
	
	def EaseOutCirc(self, x):
		return math.sqrt(1 - pow(x - 1, 2))
	
	def EaseInOutCirc(self, x):
		if x < 0.5:
			return (1 - math.sqrt(1 - pow(2 * x, 2))) / 2
		else:
			return (math.sqrt(1 - pow(-2 * x + 2, 2)) + 1) / 2
	
	def EaseInBack(self, x):
		return EasesExt.c3 * x * x * x - EasesExt.c1 * x * x
	
	def EaseOutBack(self, x): 
		return 1 + EasesExt.c3 * pow(x - 1, 3) + EasesExt.c1 * pow(x - 1, 2)
	
	def EaseInOutBack(self, x):
		if x < 0.5:
			return (pow(2 * x, 2) * ((EasesExt.c2 + 1) * 2 * x - EasesExt.c2)) / 2
		else:
			return (pow(2 * x - 2, 2) * ((EasesExt.c2 + 1) * (x * 2 - 2) + EasesExt.c2) + 2) / 2
	
	def EaseInElastic(self, x):
		if x == 0:
			return 0
		elif x == 1:
			return 1
		else:
			return -pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * EasesExt.c4)
	
	def EaseOutElastic(self, x):
		if x == 0:
			return 0
		elif x == 1:
			return 1
		else:
			return pow(2, -10 * x) * math.sin((x * 10 - 0.75) * EasesExt.c4) + 1
	
	def EaseInOutElastic(self, x):
		if x == 0:
			return 0
		elif x == 1:
			return 1
		elif x < 0.5:
			return -(pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * EasesExt.c5)) / 2
		else:
			return (pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * EasesExt.c5)) / 2 + 1
	
	def EaseInBounce(self, x): 
		return 1 - self.bounceOut(1 - x)
	
	def EaseOutBounce(self, x):
		return self.bounceOut(x)

	def EaseInOutBounce(self, x):
		if x < 0.5:
			return (1 - self.bounceOut(1 - 2 * x)) / 2
		else: 
			return (1 + self.bounceOut(2 * x - 1)) / 2

	def EaseSwift(self, x):
		return self.CubicBezier(x, 0.444, 0.013, 0.188, 0.956)

	def EaseParabola(self, x):
		return (math.sin(2 * math.pi * (x - 1/4)) + 1) / 2