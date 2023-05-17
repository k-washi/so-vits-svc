import time,pdb
import tqdm
from time import time as ttime
import os
from pathlib import Path
import logging
import argparse
from cluster.kmeans import KMeansGPU
import torch
import numpy as np
from sklearn.cluster import KMeans

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from time import time as ttime
import pynvml,torch

def train_cluster(in_dir, n_clusters, use_minibatch=True, verbose=False,use_gpu=False):#gpu_minibatch真拉，虽然库支持但是也不考虑
    logger.info(f"Loading features from {in_dir}")
    features = []
    nums = 0
    for path in tqdm.tqdm(in_dir.glob("*.soft.pt")):
    # for name in os.listdir(in_dir):
    #     path="%s/%s"%(in_dir,name)
        features.append(torch.load(path,map_location="cpu").squeeze(0).numpy().T)
        # print(features[-1].shape)
    features = np.concatenate(features, axis=0)
    print(nums, features.nbytes/ 1024**2, "MB , shape:",features.shape, features.dtype)
    features = features.astype(np.float32)
    logger.info(f"Clustering features of shape: {features.shape}")
    t = time.time()
    if(use_gpu==False):
        if use_minibatch:
            kmeans = MiniBatchKMeans(n_clusters=n_clusters,verbose=verbose, batch_size=4096, max_iter=80).fit(features)
        else:
            kmeans = KMeans(n_clusters=n_clusters,verbose=verbose).fit(features)
    else:
            kmeans = KMeansGPU(n_clusters=n_clusters, mode='euclidean', verbose=2 if verbose else 0,max_iter=500,tol=1e-2)#
            features=torch.from_numpy(features)#.to(device)
            labels = kmeans.fit_predict(features)#

    print(time.time()-t, "s")

    x = {
            "n_features_in_": kmeans.n_features_in_ if use_gpu==False else features.shape[0],
            "_n_threads": kmeans._n_threads if use_gpu==False else 4,
            "cluster_centers_": kmeans.cluster_centers_ if use_gpu==False else kmeans.centroids.cpu().numpy(),
    }
    print("end")

    return x

if __name__ == "__main__":
    res=train_cluster("/data/docker/dataset/12b-co256tensor",1000,use_minibatch=False,verbose=False,use_gpu=True)
    pdb.set_trace()