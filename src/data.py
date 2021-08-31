import graph_tools as gt
from loguru import logger
import numpy as np

class Dataset():
	def __init__(self, dirname, time, step=1, stride=1, load_feature=False):
		self.graphs = []
		self._vertices = set()
		unmerged_graphs = []

		for t in range(time):
			filename = '{}/{}'.format(dirname, str(t))
			unmerged_graphs.append(self.load_graph(filename))

		for t in range(0, time - step + 1, stride):
			merged_graph = self.merge(unmerged_graphs[t : t + step])
			self.graphs.append(merged_graph)

		self.vertices = list(self._vertices)
		self.vertex2index = {n: i for i, n in enumerate(self.vertices)}

	def __len__(self):
		return self.graphs.__len__()

	def __getitem__(self, idx):
		return self.graphs.__getitem__(idx)

	def load_graph(self, filename):
		graph = gt.Graph(directed=False)
		f = open(filename, 'r')

		for line in f.readlines():
			fields = line.split(' ')
			n = fields[0]

			if not n in self._vertices:
				self._vertices.add(n)

			if not graph.has_vertex(n):
				graph.add_vertex(n)

			for v, w in zip(fields[1::2], fields[2::2]):
				w = float(w)

				if v == n:
					logger.warning("loopback edge ({}, {}) detected".format(v, n))

				if not v in self._vertices:
					self._vertices.add(v)

				if not graph.has_vertex(v):
					graph.add_vertex(v)

				if not graph.has_edge(n, v):
					graph.add_edge(n, v)
					graph.set_edge_weight(n, v, w)

		f.close()
		return graph

	def merge(self, graphs):
		ret = gt.Graph(directed=False)

		for g in graphs:
			for v0, v1 in g.edges():
				w = g.get_edge_weight(v0, v1)

				if not ret.has_vertex(v0):
					ret.add_vertex(v0)
				if not ret.has_vertex(v1):
					ret.add_vertex(v1)
				if not ret.has_edge(v0, v1):
					ret.add_edge(v0, v1)
					ret.set_edge_weight(v0, v1, w)
				else:
					new_w = w + ret.get_edge_weight(v0, v1)
					ret.set_edge_weight(v0, v1, new_w)

		return ret
