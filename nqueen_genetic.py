import numpy as np
import sys
from random import shuffle


nQueens = 8
STOP_CTR = 28
MUTATE = 0.1
MUTATE_FLAG = True
MAX_ITER = 100000
POPULATION = None

class nqueen_problem:
	def __init__(self):
		self.sequence = None
		self.fitness = None
		self.survival = None
	def setSequence(self, val):
		self.sequence = val
	def setFitness(self, fitness):
		self.fitness = fitness
	def setSurvival(self, val):
		self.survival = val
	def getAttr(self):
		return {'sequence':self.sequence, 'fitness':self.fitness, 'survival':self.survival}

def fitness(dna = None):

	clashes = 0;
	row_col_clashes = abs(len(dna) - len(np.unique(dna)))
	clashes += row_col_clashes

	# calculate diagonal clashes
	for i in range(len(dna)):
		for j in range(i,len(dna)):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(dna[i] - dna[j])
				if(dx == dy):
					clashes += 1
	return 28-clashes


def generatedna():
	# randomly generates a sequence of board states.
	global nQueens
	init_distribution=list(range(nQueens))
	#init_distribution = np.arange(nQueens)
	np.random.shuffle(init_distribution)
	return init_distribution

def generatePopulation(self,population_size = 100):
	global POPULATION

	POPULATION = population_size
	pop=[]
	population = [nqueen_problem() for i in range(population_size)]
	for i in range(population_size):
		#flg=1
		p=generatedna()
		if len(pop) > 2:
			while p in pop:
				np.random.shuffle(p)
		pop.append(p)		
		population[i].setSequence(p)
		population[i].setFitness(fitness(population[i].sequence))		

	return population


def getParent():
	globals()	
	parent1, parent2 = None, None
	
	summation_fitness = np.sum([x.fitness for x in population])
	lenp=len(population)	
	for each in population:
		each.survival = each.fitness/(summation_fitness*1.0)
		parent1_random = np.random.randint(lenp)
		parent2_random = np.random.randint(lenp)
		parent1=population[parent1_random]
		parent2=population[parent2_random]

	if parent1 is not None and parent2 is not None:
		return parent1, parent2
	else:
		sys.exit(-1)

def reproduce_crossover(parent1, parent2):
	globals()
	n = len(parent1.sequence)
	b = np.random.randint(n, size=1)
	c = b[0]
	child = nqueen_problem()
	child.sequence = []	
	child.sequence.extend(parent1.sequence[0:c])
	for i in parent2.sequence[c:]:
		if i in child.sequence:
			continue
		child.sequence.append(i)
	for j in range(n):
		if j in child.sequence:
			continue
		child.sequence.append(j)		
	child.setFitness(fitness(child.sequence))
	return child


def mutate(child):
	if child.survival:	    
		if child.survival < MUTATE:
			child.sequence=np.random.shuffle(child.sequence)
	return child

def GA(iteration):
	#print (" #"*10 ,"Executing Genetic  generation : ", iteration , " #"*10)
	globals()
	newpopulation = []
	pop =[]
	for i in range(len(population)):
		parent1, parent2 = getParent()
		child = reproduce_crossover(parent1, parent2)
		cnt=0
		while child.sequence in pop:
			child = reproduce_crossover(parent2, parent1)
			cnt+=1
			if cnt > 10 and cnt < 20:
				child = reproduce_crossover(parent1, parent2)
			if cnt >= 20 and cnt <=100:
				shuffle(child.sequence)
			if cnt > 100:
				break;
		pop.append(child.sequence)

		if(MUTATE_FLAG):
			child = mutate(child)
		newpopulation.append(child)
	return newpopulation


def stop():
	globals()
	fitnessvals = [pos.fitness for pos in population]
	if STOP_CTR in fitnessvals:
		return True
	if MAX_ITER == iteration:
		return True
	return False

population = generatePopulation(100)

iteration = 0;
while not stop():
	# keep iteratin till  you find the best position
	population = GA(iteration)
	iteration +=1 
for each in population:
	if each.fitness == 28:
		print (each.sequence)
		break