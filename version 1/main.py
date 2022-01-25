import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")


from GameObjects import *


allGrains = []

backgroundColor = darkGray

cellSize = [8, 8]

class World:
	def __init__(self):
		self.CreateGrid()

	def CreateGrid(self):
		self.grid = [((x % (width // cellSize[0])) * cellSize[0], (x // (width // cellSize[0])) * cellSize[1]) for x in range((width // cellSize[0]) * (height // cellSize[1]))]

	def GetIndex(self, x, y):
		x //= cellSize[0]
		y //= cellSize[1]
		return x + (y * width // cellSize[0])

	def Draw(self):
		return 
		for cell in self.grid:
			if type(cell) == tuple:
				pg.draw.rect(screen, red, (cell[0] + 1, cell[1] + 1, 2, 2))
			else:
				pg.draw.rect(screen, red, (cell.x + 1, cell.y + 1, 2, 2))

	def SetPos(self, x1, y1, x2, y2):
		self.grid[self.GetIndex(x2, y2)] = self.grid[self.GetIndex(x1, y1)]
		pos = ((self.GetIndex(x2, y2) % (width // cellSize[0])) * cellSize[0], (self.GetIndex(x2, y2) // (width // cellSize[0])) * cellSize[1])  

		self.grid[self.GetIndex(x1, y1)] = ((self.GetIndex(x1, y1) % (width // cellSize[0])) * cellSize[0], (self.GetIndex(x1, y1) // (width // cellSize[0])) * cellSize[1])

		return pos

	def SwapPos(self, x1, y1, x2, y2):
		tempObj = self.grid[self.GetIndex(x2, y2)]
		
		self.grid[self.GetIndex(x2, y2)] = self.grid[self.GetIndex(x1, y1)]
		
		self.grid[self.GetIndex(x1, y1)] = tempObj

		pos = (self.grid[self.GetIndex(x2, y2)].y, self.grid[self.GetIndex(x1, y1)].y)
		return pos

	def Update(self):
		for grain in allGrains:
			grain.Update()
			grain.CheckDensity()

	def AddGrain(self, x, y, grain):
		if type(self.grid[self.GetIndex(x, y)]) == tuple:
			if 0 <= x < width and 0 <= y < height:
				self.grid[self.GetIndex(x, y)] = grain
				return True
			else:
				allGrains.remove(grain)
				return False
		else:
			allGrains.remove(grain)
			return False

	def Erase(self, x, y):
		if self.grid[self.GetIndex(x, y)] != tuple:
			self.grid[self.GetIndex(x, y)] = ((self.GetIndex(x, y) % (width // cellSize[0])) * cellSize[0], (self.GetIndex(x, y) // (width // cellSize[0])) * cellSize[1])


class Grain:
	def __init__(self, x, y, density, color):
		self.x, self.y = x, y
		self.density = density

		self.color = color

		AddToListOrDict([allGrains], self)

	def Draw(self):
		pg.draw.rect(screen, self.color, (self.x, self.y, cellSize[0], cellSize[1]))

	def CheckDensity(self):
		if self.y - cellSize[1] < height and world.GetIndex(self.x, self.y - cellSize[1]) < len(world.grid):
			matAbove = world.grid[world.GetIndex(self.x, self.y - cellSize[1])]
			if type(matAbove) in solidTypes and type(self) not in solidTypes:
				if matAbove.density > self.density:
					pos = world.SwapPos(matAbove.x, matAbove.y, self.x, self.y)
					self.y = pos[0]
					matAbove.y = pos[1]

	def Kill(self):
		if self in allGrains:
			allGrains.remove(self)

		if self in world.grid:
			world.Erase(self.x, self.y)


class Sand(Grain):
	def __init__(self, x, y, density=10, color=yellow):
		super().__init__(x, y, density, color)

	def Update(self):
		if self.y + cellSize[1] < height and world.GetIndex(self.x, self.y + cellSize[1]) < len(world.grid): 
			if type(world.grid[world.GetIndex(self.x, self.y + cellSize[1])]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x, self.y + cellSize[1])
				self.y = min(pos[1], height)
				return
			else:
				if self.y + (cellSize[1] * 2) < height:
					if type(world.grid[world.GetIndex(self.x, self.y + (cellSize[1] * 1))]) != tuple and type(world.grid[world.GetIndex(self.x, self.y + (cellSize[1] * 2))]) != tuple:
						if self.x - cellSize[0] >= 0:
							if type(world.grid[world.GetIndex(self.x - cellSize[0], self.y + cellSize[1])]) == tuple:
								pos = world.SetPos(self.x, self.y, self.x - cellSize[0], self.y + cellSize[1])
								self.x = pos[0]
								self.y = min(pos[1], height)
								return

						if self.x + cellSize[0] < width:
							if type(world.grid[world.GetIndex(self.x + cellSize[0], self.y + cellSize[1])]) == tuple:
								pos = world.SetPos(self.x, self.y, self.x + cellSize[0], self.y + cellSize[1])
								self.x = pos[0]
								self.y = min(pos[1], height)
								return


class Water(Grain):
	def __init__(self, x, y, density=5, color=lightBlue):
		super().__init__(x, y, density, color)
	
	def Update(self):
		if self.y + cellSize[1] < height and world.GetIndex(self.x, self.y + cellSize[1]) < len(world.grid): 
			if type(world.grid[world.GetIndex(self.x, self.y + cellSize[1])]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x, self.y + cellSize[1])
				self.y = min(pos[1], height)
				return
			else:
				if self.y + (cellSize[1] * 2) < height: 
					if type(world.grid[world.GetIndex(self.x, self.y + (cellSize[1] * 2))]) == tuple:
						if self.x - cellSize[0] >= 0:
							if type(world.grid[world.GetIndex(self.x - cellSize[0], self.y + cellSize[1])]) == tuple:
								pos = world.SetPos(self.x, self.y, self.x - cellSize[0], self.y + cellSize[1])
								self.x = pos[0]
								self.y = min(pos[1], height)
								return

						if self.x + cellSize[0] < width:
							if type(world.grid[world.GetIndex(self.x + cellSize[0], self.y + cellSize[1])]) == tuple:
								pos = world.SetPos(self.x, self.y, self.x + cellSize[0], self.y + cellSize[1])
								self.x = pos[0]
								self.y = min(pos[1], height)
								return

		if self.x - cellSize[0] >= 0:
			if type(world.grid[world.GetIndex(self.x - cellSize[0], self.y)]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x - cellSize[0], self.y)
				self.x = pos[0]
				return

		if self.x + cellSize[0] < width:
			if type(world.grid[world.GetIndex(self.x + cellSize[0], self.y)]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x + cellSize[0], self.y)
				self.x = pos[0]
				return


class Wood(Grain):
	def __init__(self, x, y, density=-10000, color=(56, 27, 8)):
		super().__init__(x, y, density, color)

	def Update(self):
		pass


class Fire(Grain):
	def __init__(self, x, y, density=10, lifeSpan=20, color=red):
		super().__init__(x, y, density, color)

		self.timeAlive = 0
		self.lifeSpan = lifeSpan

	def Update(self):
		self.timeAlive += 1

		if self.timeAlive >= self.lifeSpan:
			self.Kill()
			world.AddGrain(self.x, self.y, Smoke(self.x, self.y))


class Smoke(Grain):
	def __init__(self, x, y, density=10, color=lightBlack):
		super().__init__(x, y, density, color)

	def Update(self):
		if self.y - cellSize[1] >= 0 and world.GetIndex(self.x, self.y - cellSize[1]) < len(world.grid): 
			if type(world.grid[world.GetIndex(self.x, self.y - cellSize[1])]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x, self.y - cellSize[1])
				self.y = max(pos[1], 0)
				return
			else:
				if self.y - (cellSize[1] * 2) < height:
					if type(world.grid[world.GetIndex(self.x, self.y - (cellSize[1] * 1))]) != tuple and type(world.grid[world.GetIndex(self.x, self.y - (cellSize[1] * 2))]) != tuple:
						if self.x - cellSize[0] >= 0:
							if type(world.grid[world.GetIndex(self.x - cellSize[0], self.y - cellSize[1])]) == tuple:
								pos = world.SetPos(self.x, self.y, self.x - cellSize[0], self.y - cellSize[1])
								self.x = pos[0]
								self.y = max(pos[1], 0)
								return

						if self.x + cellSize[0] < width:
							if type(world.grid[world.GetIndex(self.x + cellSize[0], self.y - cellSize[1])]) == tuple:
								pos = world.SetPos(self.x, self.y, self.x + cellSize[0], self.y - cellSize[1])
								self.x = pos[0]
								self.y = max(pos[1], 0)
								return

		if self.x - cellSize[0] >= 0:
			if type(world.grid[world.GetIndex(self.x - cellSize[0], self.y)]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x - cellSize[0], self.y)
				self.x = pos[0]
				return

		if self.x + cellSize[0] < width:
			if type(world.grid[world.GetIndex(self.x + cellSize[0], self.y)]) == tuple:
				pos = world.SetPos(self.x, self.y, self.x + cellSize[0], self.y)
				self.x = pos[0]
				return



def DrawLoop():
	screen.fill(backgroundColor)

	world.Draw()

	for grain in allGrains:
		grain.Draw()

	DrawAllGUIObjects()

	mouse.Draw()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	mouse.HandleEvent(event)


def Update():
	world.Update()

	mouse.Update()


liquidTypes = [Water]
solidTypes = [Sand, Wood]

world = World()


class Mouse:
	def __init__(self, radius, colors):
		self.pos = pg.mouse.get_pos()
		self.radius = radius
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

		self.radiusMin = cellSize[0]
		self.radiusMax = 16 * cellSize[0]

		self.material = "Sand"

		pg.mouse.set_visible(False)

	def Draw(self):
		DrawRectOutline(self.borderColor, (self.pos[0] - 2, self.pos[1] - 2, self.radius + 4, self.radius + 4), 2)

	def Update(self):
		self.pos = (pg.mouse.get_pos()[0] + (cellSize[0] - (pg.mouse.get_pos()[0] % cellSize[0])) - cellSize[0], pg.mouse.get_pos()[1] + (cellSize[1] - (pg.mouse.get_pos()[1] % cellSize[1])) - cellSize[0])

		if pg.mouse.get_pressed()[0]:
			for i in range(self.radius // cellSize[0]):
				for j in range(self.radius // cellSize[1]):
					x = self.pos[0] + (cellSize[0] - (self.pos[0] % cellSize[0])) + ((i - 1) * cellSize[0])
					y = self.pos[1] + (cellSize[1] - (self.pos[1] % cellSize[1])) + ((j - 1) * cellSize[1])
					
					self.AddMaterial(x, y)

	def AddMaterial(self, x, y):
		try:
			if self.material == "Sand":
				world.AddGrain(x, y, Sand(x, y))
			elif self.material == "Water":
				world.AddGrain(x, y, Water(x, y))
			elif self.material == "Wood":
				world.AddGrain(x, y, Wood(x, y))
			elif self.material == "Fire":
				world.AddGrain(x, y, Fire(x, y))
			elif self.material == "Smoke":
				world.AddGrain(x, y, Smoke(x, y))
			elif self.material == "Eraser":
				world.Erase(x, y)
		except:
			pass

	def HandleEvent(self, event):
		if event.type == pg.KEYDOWN:
			if event.key == K_EQUALS:
				if self.radius < self.radiusMax:
					self.radius = int(min(self.radiusMax, self.radius * 2))

			if event.key == K_MINUS:
				if self.radius > self.radiusMin:
					self.radius = int(max(self.radiusMin, self.radius // 2))

			if event.key == K_1:
				self.material = "Sand"

			if event.key == K_2:
				self.material = "Water"

			if event.key == K_3:
				self.material = "Wood"

			if event.key == K_4:
				self.material = "Fire"
			
			if event.key == K_5:
				self.material = "Smoke"

			if event.key == K_0:
				self.material = "Eraser"


mouse = Mouse(cellSize[0] * 2, (white, black))

while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()

	# print(clock.get_fps())

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()
