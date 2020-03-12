import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2

from object_detection_yolo import *
from Map2D import Map

from camera import Camera
import structure
import processor
import features

fx = 1840.7105821048197
fy = 1835.4712842276044
cx = 1258.4333584930628
cy = 985.893747793618

# Load names of classes
classesFile = "yolo/coco.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

out_of_camera = lambda K, points: np.dot(np.linalg.inv(K), points)

K = np.array([  [fx, 0, cx],
                [0, fx, cy],
                [0, 0, 1]] )

def reconstruct(img1, img2): 
    pts1, pts2, features2 = features.find_correspondence_points(img1, img2)
    points1 = processor.cart2hom(pts1)
    points2 = processor.cart2hom(pts2)

    # Calculate essential matrix with 2d points.
    # Result will be up to a scale
    # First, normalize points
    points1n = out_of_camera(K, points1)
    points2n = out_of_camera(K, points2)
    E = structure.compute_essential_normalized(points1n, points2n)
    print('Computed essential matrix:', (-E / E[0][1]))

    # Given we are at camera 1, calculate the parameters for camera 2
    # Using the essential matrix returns 4 possible camera paramters
    P1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    P2s = structure.compute_P_from_essential(E)

    ind = -1
    for i, P2 in enumerate(P2s):
        # Find the correct camera parameters
        d1 = structure.reconstruct_one_point(
            points1n[:, 0], points2n[:, 0], P1, P2)

        # Convert P2 from camera view to world view
        P2_homogenous = np.linalg.inv(np.vstack([P2, [0, 0, 0, 1]]))
        d2 = np.dot(P2_homogenous[:3, :4], d1)

        if d1[2] > 0 and d2[2] > 0:
            ind = i

    P2 = np.linalg.inv(np.vstack([P2s[ind], [0, 0, 0, 1]]))[:3, :4]

    return points1, points2, P1, P2, features2

if __name__ == "__main__":
    img1 = cv2.imread('data/1.jpg')
    img2 = cv2.imread('data/2.jpg')

    my_Map = Map()
    
    points_1_tmp, points_2_tmp, P1,P2, features2 = reconstruct(img1, img2)
    
    (boxes1, ids1), tmp_1 = detect(img1.copy())
    (boxes2, ids2), tmp_2 = detect(img2.copy())
    
    positions = []
    fig = plt.figure(1, figsize=(100,100))
    for i in range(boxes1.shape[0]):
        class_name = classes[ids1[i]]
        
        c,r,w,h = boxes1[i]
        mask1 = np.zeros(img1.shape,np.uint8)
        mask1[r:r+h,c:c+w] = img1[r:r+h,c:c+w]
        
        try:
            pts1, pts2, match = features.fast_correspondence_points(mask1, img2, features2)
        except :
            print("Error in find correspondacnce")
            continue
        
        points1 = processor.cart2hom(pts1)
        points2 = processor.cart2hom(pts2)
        
        # #! plot
        plt.subplot(boxes1.shape[0], 1, i+1)
        plt.imshow(match)
        
        #! get triangulation
        points1n = out_of_camera(K, points1)
        points2n = out_of_camera(K, points2)
        tripoints3d = structure.linear_triangulation(points1n, points2n, P1, P2)
        
        if tripoints3d.shape[1]==0: continue
        
        position = np.mean(tripoints3d, axis=1)[:-1]
        positions.append(position.tolist())
        
        my_Map.add_to_map(class_name, position[0], position[1] )
    
    plt.show()
        
    # positions = np.array(positions)

    figure_map = plt.figure(figsize=(10,10))
    my_Map.plot(figure=figure_map)
    plt.show()
    
    
    # fig = plt.figure()
    # fig.suptitle('3D reconstructed', fontsize=16)
    # plt.plot(positions[:,0], positions[:,1], 'b.')
    # plt.show()
    