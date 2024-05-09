# Objectives

### Implementar e comparar diversas forma de se obter normais de superfície através do método dda Principal component Analisys (PCA)

### Requeriments
### !pip install open3d opencv-python

import os
import numpy as np
import requests
import cv2
import open3d as o3d

print(o3d.__version__,'\n', cv2.__version__)

### Preparo do dados

response = requests.get("https://raw.githubusercontent.com/PointCloudLibrary/pcl/master/test/bunny.pcd")
if response.status_code==200:
    file = open("bunny.pcd", "w")
    file.write(response.text)
    file.close()

pcd = o3d.io.read_point_cloud("bunny.pcd")
### Min Max Norm of data
x = [ (v - np.asarray(pcd.points)[:,0].min())/(np.asarray(pcd.points)[:,0].max() - np.asarray(pcd.points)[:,0].min()) for v in np.asarray(pcd.points)[:,0] ]
y = [ (v - np.asarray(pcd.points)[:,1].min())/(np.asarray(pcd.points)[:,1].max() - np.asarray(pcd.points)[:,1].min()) for v in np.asarray(pcd.points)[:,1] ]
z = [ (v - np.asarray(pcd.points)[:,2].min())/(np.asarray(pcd.points)[:,2].max() - np.asarray(pcd.points)[:,2].min()) for v in np.asarray(pcd.points)[:,2] ]

np.asarray(pcd.points)[:,0] = x
np.asarray(pcd.points)[:,1] = y
np.asarray(pcd.points)[:,2] = z

### Center data
x_av = np.mean(np.asarray(pcd.points)[:,0])
y_av = np.mean(np.asarray(pcd.points)[:,1])
z_av = np.mean(np.asarray(pcd.points)[:,2])

np.asarray(pcd.points)[:,0] -= x_av
np.asarray(pcd.points)[:,1] -= y_av
np.asarray(pcd.points)[:,2] -= z_av

### Função pronta para estimar as normais
pcd.estimate_normals()
pcd.normalize_normals()

# Save bunch of images

eixos = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0,0,0])
# Visualizar (Não funciona notebooks jupyter ou colab)
vis = o3d.visualization.Visualizer()
vis.create_window(width=1200, height=900)
vis.add_geometry(pcd); vis.add_geometry(eixos)
vis.update_geometry(pcd); vis.poll_events(); vis.update_renderer()
ctr = vis.get_view_control()
opt = vis.get_render_option()
opt.point_show_normal = True
for i in range(100):
    ctr.rotate(50.0, 0.0)
    vis.update_geometry(pcd); vis.poll_events(); vis.update_renderer()
    vis.capture_screen_image(f"img{str(i).zfill(3)}.jpg")
vis.destroy_window()

image_folder = './'
video_name = 'video.mp4'
fps = 15
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, fps, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

# Save a video
image_folder = './'
video_name = 'video.mp4'
fps = 15
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, fps, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
