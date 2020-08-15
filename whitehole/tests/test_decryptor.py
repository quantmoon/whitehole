# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 18:40:27 2020

@author: HELI
"""

import whitehole as wh

dcrypt= wh.Decryptor(repo_path= 'C:/Users/HELI/data/zarr/', 
          symbol='FB', 
          date="2018-12-31", 
          full_day=True, 
          save=True,
          storage_path='C:/Users/HELI/data/csvdata/')

dcrypt.run_decryptor()


