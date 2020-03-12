import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from time import sleep

class Map:
    def __init__(self, W=40, H=40):
        self.gymnase_longueur = W
        self.gymnase_largeur = H

        self.voitures = {}
        self.humains = {}
        self.zone_ombre ={}
        self.Drones = {}
        self.Autres = {}

    def plot(self, save = True, figure=None):
        
        if figure == None:
            figure = plt.figure(figsize=(10,10))
            
        plt.grid(True)
        plt.title('Carte 2D du parking')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(0, self.gymnase_largeur)
        plt.ylim(0, self.gymnase_longueur)
        plt.ion()
        plt.show()
        
        axes = plt.gca()
        axes.set_aspect('equal', adjustable='box')
        
        for r in self.voitures:
            axes.add_artist(self.voitures[r])
            rx, ry = self.voitures[r].get_xy()
            cx = rx + self.voitures[r].get_width()/2.0
            cy = ry + self.voitures[r].get_height()/2.0
            axes.annotate(r, (cx, cy), color='w', weight='bold', 
                        fontsize=6, ha='center', va='center')

        for r in self.humains:
            axes.add_artist(self.humains[r])
            rx, ry = self.humains[r].get_xy()
            cx = rx + self.humains[r].get_width()/2.0
            cy = ry + self.humains[r].get_height()/2.0
            axes.annotate(r, (cx, cy), color='w', weight='bold', 
                        fontsize=6 , ha='center', va='center')

        for r in self.Autres:
            axes.add_artist(self.Autres[r])
            rx, ry = self.Autres[r].get_xy()
            cx = rx + self.Autres[r].get_width()/2.0
            cy = ry + self.Autres[r].get_height()/2.0
            axes.annotate(r, (cx, cy), color='w', weight='bold', 
                        fontsize=6, ha='center', va='center')

        for r in self.zone_ombre:
            axes.add_artist(self.zone_ombre[r])

        for r in self.Drones:
            axes.add_artist(self.Drones[r])

        if save:
            figure.savefig("map2D.pdf")
            
    def add_to_map(self, obj, x, y):
        if obj == 'car':
            self.voitures['v %s' %(len(self.voitures)+1)] = mpatches.Rectangle((x,y), 2, 2, color = 'blue', alpha = 0.6)
        elif obj == 'person':
            self.humains['h %s' %(len(self.humains)+1)] = mpatches.Rectangle((x,y), 1, 1, color = 'red', zorder=3)
        elif obj == 'zone_ombre':
            self.zone_ombre['%s' %(len(self.zone_ombre)+1)] = mpatches.Rectangle((x,y), 2, 2, color = 'gray', hatch = '/', alpha = 0.6, zorder =0)
        elif obj == 'drone':
            self.Drones['%s' %(len(self.Drones)+1)] = mpatches.Circle((x,y), 0.3, color='magenta',zorder=2)
        else:
            self.Autres["%s_%s"%(obj,(len(self.Autres)+1))] = mpatches.Rectangle((x,y), 2, 2, color = 'black', alpha = 0.6)

if __name__ == "__main__":
    my_map = Map()
    my_map.plot_map()

    my_map.add_to_map('car', 3, 5)

    my_map.add_to_map('zone_ombre', 4,6)

    my_map.add_to_map('person', 7,7)

    my_map.add_to_map('zone_ombre', 9,11)

    my_map.add_to_map('drone', 1,1)

    my_map.add_to_map('drone', 37,1)

    my_map.add_to_map('drone' , 10, 12)

    my_map.add_to_map('chaise', 16,23)

    my_map.save()