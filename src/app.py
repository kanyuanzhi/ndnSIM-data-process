import networkx as nx
import matplotlib.pyplot as plt
import numpy


class Torus:
    def __init__(self, n):
        self.__n = n
        self.__nn = n * n
        self.torus_matrix = self.__generate_n_torus_matrix()
        self.torus = self.__generate_n_torus_network()
        self.torus_with_properties = self.__generate_torus_with_properties()

    def __generate_n_torus_matrix(self):
        torus_matrix = numpy.zeros((self.__nn, self.__nn))
        for i in range(self.__nn):
            if i % self.__n == 0:
                torus_matrix[i][i+1] = 1
                torus_matrix[i][i+self.__n-1] = 1
            else:
                if (i+1) % self.__n != 0:
                    torus_matrix[i][i+1] = 1
            if i < self.__n:
                torus_matrix[i][i+self.__n] = 1
                torus_matrix[i][i+(self.__n-1)*self.__n] = 1
            else:
                if i <= self.__nn - self.__n - 1:
                    torus_matrix[i][i+self.__n] = 1
        return torus_matrix

    def __generate_n_torus_network(self):
        G = nx.Graph()
        for i in range(self.__nn):
            G.add_node(i)

        for i in range(self.__nn):
            for j in range(i+1, self.__nn):
                if self.torus_matrix[i][j] == 1:
                    G.add_edge(i, j)
        return G

    def __generate_torus_with_properties(self):
        nodes = self.torus.nodes()
        edges = self.torus.edges()
        G = nx.Graph()
        for node in nodes:
            G.add_node(node, comment="NA", yPos=self.__n -
                       int(node/self.__n), xPos=node % self.__n+1)
        G.add_edges_from(edges, bandwidth="1Mbps",
                         metric="1", delay="10ms", queue="10")
        return G

    def save_to_txt(self):
        nodes = self.torus_with_properties.nodes(data=True)
        edges = self.torus_with_properties.edges(data=True)
        string = "router\n"
        for node in nodes:
            string = string + str(node[0]) + " " + node[1]["comment"] + \
                " " + str(node[1]["yPos"]) + " " + str(node[1]["xPos"]) + "\n"
        string = string + "\nlink\n"

        for edge in edges:
            string = string + str(edge[0]) + " " + str(edge[1]) + " " + edge[2]['bandwidth'] + \
                " " + edge[2]['metric'] + " " + \
                edge[2]['delay'] + " " + edge[2]['queue'] + "\n" 

        print string

        with open("torus-grid.txt","w") as f:
            f.write(string)


if __name__ == "__main__":
    gg = nx.Graph()
    gg.edges()
    T = Torus(10)
    G = T.torus

    nx.draw(G)
    path = nx.shortest_path(G)
    print path[0][99]

    #print G.edges(data=True)
    #print T.torus_with_properties.edges(data=True)

    #T.save_to_txt()
    #plt.show()
