# #!/usr/bin/python

import matplotlib.pyplot as plt
import multiprocessing as mp

class Graphs(mp.Process):

	def __init__(self, name, array, players_names, queue):
		super(Graphs, self).__init__()

		self.queue = queue
		self._stop_event = mp.Event()
		self.names = name
		self.array = array
		self.players_names = players_names

	def run(self):
		self.fig = plt.figure()
		self.fig.canvas.mpl_connect('close_event',self.stop)
		
		plt.title(self.name +' over game played',loc='center')
		plt.xlabel('# of Games Played')
		plt.ylabel('number of ' + self.name)
		
		plt.plot(self.array)
		plt.legend(labels=self.players_names)
		self.queue.put("Graph {0}'".format(self.names))
		plt.show()


	def stop(self,*evt):
		self._stop_event.set()

if __name__ == '__main__':

	import time

	g = Graphs('m''lady',[1])

	g.start()
	i=0
	while 0:
		time.sleep(1)
		i = i+1
		print (i)
