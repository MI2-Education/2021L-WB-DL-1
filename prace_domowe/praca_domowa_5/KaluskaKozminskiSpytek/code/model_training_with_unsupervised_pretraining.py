# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 18:15:43 2019

@author: Reza Azad
"""
from __future__ import division
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import models as M
import unsupervised_autoencoder_architecture as p
import numpy as np
from keras.callbacks import ModelCheckpoint, TensorBoard,ReduceLROnPlateau
from keras import callbacks
import pickle

import tensorflow as tf

# config = tf.compat.v1.ConfigProto(gpu_options =
#                          tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# # device_count = {'GPU': 1}
# )
# config.gpu_options.allow_growth = True
# session = tf.compat.v1.Session(config=config)
# tf.compat.v1.keras.backend.set_session(session)
####################################  Load Data #####################################
folder = './processed_data/'
tr_data    = np.load(folder+'data_train.npy')
tr_mask    = np.load(folder+'Train_maska.npy')
tr_data    = np.expand_dims(tr_data, axis=3)
tr_mask    = np.expand_dims(tr_mask, axis=3)

print('Dataset loaded')

tr_data   = tr_data /255.

print('dataset Normalized')

print(tr_data.shape)

# Build model
model = M.BCDU_net_D3(input_size = (512,512,1))
#model.summary()


p.pretrain(model, (512,512,1), tr_data)

print('Training')
batch_size = 2
nb_epoch   = 1


mcp_save = ModelCheckpoint('weight_lung', save_best_only=True, monitor='val_loss', mode='min')
reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, epsilon=1e-4, mode='min')
history = model.fit(tr_data,tr_mask,
              batch_size=batch_size,
              epochs=nb_epoch,
              shuffle=True,
              verbose=1,
              validation_split=0.2, callbacks=[mcp_save, reduce_lr_loss] )
  
print('Trained model saved')
with open('hist_lung', 'wb') as file_pi:
        pickle.dump(history.history, file_pi)



