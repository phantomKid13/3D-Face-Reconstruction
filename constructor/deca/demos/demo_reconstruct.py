import os, sys
import cv2 
import numpy as np
from time import time
from scipy.io import savemat
import argparse
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decalib.deca import DECA
from decalib.datasets import datasets 
from decalib.utils import util
from decalib.utils.config import cfg as deca_cfg

def main(args):
    savefolder = "/gdrive/MyDrive/Face_Reconstruction/constructor/deca/results"
    device = 'cuda'
    os.makedirs(savefolder, exist_ok=True)

    # load test images 
    testdata = datasets.TestData(args, iscrop=True, face_detector='fan')

    # run DECA
    deca_cfg.model.use_tex = True
    deca = DECA(config = deca_cfg, device=device)
    # for i in range(len(testdata)):

    if(len(testdata)>1):
      Dir=os.path.join(savefolder,"sequence")
      
      if(os.path.isdir(Dir)):
        for filename in os.listdir(Dir):
          f = os.path.join(Dir, filename)
          if os.path.isfile(f):
            os.remove(f)
      else:
        os.makedirs(Dir,exist_ok=True)

    for i in tqdm(range(len(testdata))):
        name = testdata[i]['imagename']
        images = testdata[i]['image'].to(device)[None,...]
        codedict = deca.encode(images)
        opdict, visdict = deca.decode(codedict) #tensor
     
        if(len(testdata)==1):
          os.makedirs(os.path.join(savefolder, name), exist_ok=True)
        # -- save results
        depth_image = deca.render.render_depth(opdict['transformed_vertices']).repeat(1,3,1,1)
        visdict['depth_images'] = depth_image
        #cv2.imwrite(os.path.join(savefolder, name, name + '_depth.jpg'), util.tensor2image(depth_image[0]))
        
        if(len(testdata)>1):
          deca.save_obj(os.path.join(savefolder, "sequence", name + '.obj'), opdict)
          continue
          
        deca.save_obj(os.path.join(savefolder, name, name + '.obj'), opdict)