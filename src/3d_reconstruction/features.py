import cv2
import numpy as np

def filter_points(points, area):
    idx_filter = []
    x_lim,y_lim,w,h=area
    for i in range(points.shape[1]) : 
        x, y = points[:2,i]
        if (x<x_lim+w and x>x_lim) and (y<y_lim+h and y>=y_lim) :
            idx_filter.append(i)
    return idx_filter
    
def find_correspondence_points(img1, img2, area1=None, area2=None):
    
    # sift = cv2.xfeatures2d.SURF_create()
    sift = cv2.xfeatures2d.SIFT_create(	edgeThreshold = 50)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(
        cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), None)
    kp2, des2 = sift.detectAndCompute(
        cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), None)

    # Find point matches
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply Lowe's SIFT matching ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)

    src_pts = np.asarray([kp1[m.queryIdx].pt for m in good])
    dst_pts = np.asarray([kp2[m.trainIdx].pt for m in good])

    # Constrain matches to fit homography
    retval, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 100.0)
    mask = mask.ravel()

    # We select only inlier points
    pts1 = src_pts[mask == 1]
    pts2 = dst_pts[mask == 1]

    return pts1.T, pts2.T, (kp2, des2)


  
def fast_correspondence_points(img1, img2, features2, area1=None, area2=None):
    training_image = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    training_gray = cv2.cvtColor(training_image, cv2.COLOR_RGB2GRAY)

    test_image = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    test_gray = cv2.cvtColor(test_image, cv2.COLOR_RGB2GRAY)

    sift = cv2.xfeatures2d.SIFT_create(	edgeThreshold = 50)

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(training_gray, None)
    kp2, des2 = features2

    # Find point matches
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply Lowe's SIFT matching ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)

    kp_1 = np.asarray([kp1[m.queryIdx] for m in good])
    kp_2 = np.asarray([kp2[m.trainIdx] for m in good])

    src_pts = np.asarray([kp1[m.queryIdx].pt for m in good])
    dst_pts = np.asarray([kp2[m.trainIdx].pt for m in good])

    # Constrain matches to fit homography
    retval, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 100.0)
    mask = mask.ravel()

    # We select only inlier points
    kp1 = kp_1[mask == 1]
    kp2 = kp_2[mask == 1]

    pts1 = src_pts[mask == 1]
    pts2 = dst_pts[mask == 1]

    result= []
    for i in range(kp1.shape[0]):
        result.append(cv2.DMatch(i, i, 1))

    img_match = cv2.drawMatches(training_image, kp1, test_image, kp2,result, None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    
    return src_pts.T, dst_pts.T, img_match
