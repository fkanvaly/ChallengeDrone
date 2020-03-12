from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


Data_3=[[10,10],[30,50],[20,10],[40,100]]


class Cluster:
    def __init__(self,obj_coor):
        self.obj_coor=obj_coor
    
    def assign(self):
        df = DataFrame(self.obj_coor)
        kmeans = KMeans(n_clusters=2).fit(df)
        labels=kmeans.labels_
        drones=[[],[]]
        for i in range (len(labels)):
            drones[labels[i]].append(self.obj_coor[i])
        return(drones)

    def send_command(self,client1,client2):
        obj=self.assign()
        
        for i in range(len(obj[0])):
            client1.send_message("go "+str(obj[0][i][0])+" "+str(obj[0][i][1]))
        for j in range(len(obj[1])):
            client2.send_message("go "+str(obj[0][j][0])+" "+str(obj[0][j][1]))
        

