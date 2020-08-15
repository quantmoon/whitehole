# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 14:48:14 2020

@author: HELI
"""
import csv
from datetime import datetime
import pandas as pd
import numpy as np
from dateutil import parser
import sys
import re
import xarray as xr

class BaseDecryptor(object):
    """
    General Decryptor Functions
    
    1. trading_calendar(): 
        - upload trading days as datetimes.
    2. extract_date_available_marker(): 
        - match trading NYSE days with input days.
    3. range_time():
        - makes range-time based on 'str' hours input.
    4. read_zarr():
        - get np.array infomration from zarr files.
    """
    def trading_calendar():
        """
        Gets trading days based on NYSE Calendar.
        """
        #extend limits of csv extension
        csv.field_size_limit(10**9)
        
        #open trading calendar file
        with open("./trading_calendar_NYSE.csv") as td:
            reader = csv.reader(td)
            dates_string = list(reader)[0][0]
            dates_list = re.split(r";",dates_string)
            
        #transform as datetime.date() each string date
        return [datetime.strptime(
            j.split("T")[0],'%Y-%m-%d').date() 
                for j in dates_list]

    def extract_date_available_market(self, 
                                      start_, 
                                      end_, 
                                      trd_cal_=trading_calendar()):
        """
        Match NYSE trading calendar days with input days.
        """
        #define start and endDate as datetime
        startDate=datetime.strptime(start_,'%Y-%m-%d')
        endDate=datetime.strptime(end_,'%Y-%m-%d')
        
        #check if both are the same dates
        if startDate == endDate:
            
            #assign single startdate as date() only
            list_pre = [startDate.date()]
            
            #find min nearest date to set a benchmark 
            date = min(
                trd_cal_, key= lambda x: abs(x - list_pre[0])
            )
            
            #check if nearest is the same as input date
            if date == list_pre[0]:
                idx = [trd_cal_.index(date)]
                return [trd_cal_[idx[0]].strftime('%Y-%m-%d')]         
            #if not is the same
            else:
                print("No trading days at {}".format(
                    startDate.date())
                     )
                sys.exit()
        #if input dates are different 
        else:
            #check nearest date to start date
            date = min(
                trd_cal_, key=lambda x: abs(x - startDate.date())
            )
            idx_1 = trd_cal_.index(date)
            
            #check nearest date to end date
            date = min(
                trd_cal_, key=lambda x: abs(x - endDate.date())
            )
            idx_2 = trd_cal_.index(date)
            
            #make range of dates
            resulted_dates_range = trd_cal_[idx_1:idx_2+1]
            
            #check if range of dates is less than 1 (no dates)
            if len(resulted_dates_range)<1:
                print("No trading days in {} to {}".format(
                    startDate.date(), 
                    endDate.date())
                     )
                sys.exit()
                
            #if there is at least one trading day
            else:
                return [result_date_.strftime('%Y-%m-%d') 
                        for result_date_ in resulted_dates_range]  

    def range_time(self, date, init, last):
        """
        Makes range-time based on 'str' hours input.
        """
        #avoid space issues
        init = init.replace(" ","")
        last = last.replace(" ","")
        
        #check if both are the same
        if init == last:
            print("No range among time bounds")
            sys.exit()

        
        #transform 'init' string into datetime
        _initialization = datetime.timestamp(
                parser.parse(
                        date + " " + init
                        )
                ) * (10**3)
        
        #transform 'last' string into datetime
        _finalization = datetime.timestamp(
                parser.parse(
                        date + " " + last
                        )
                ) * (10**3)
        
        #return tuple of information
        return (_initialization, _finalization)
    
    def read_zarr(self, 
                  file,
                  date, 
                  initialization_step, 
                  finalization_step):
        """
        Get np.array infomration from zarr files.
        
        Important:
        
        Zarr files will be transformed as xarray.Dataset.
        
        To know about xarray, please check:
        http://xarray.pydata.org/en/stable/why-xarray.html 
        """
        #open zarr
        data=xr.open_zarr(file).sel(date=date)
        
        #check if there is dates 
        if data.timestamp.shape[0] == 0:
            print('No stored data for this stock/heartbeat')
            sys.exit()
            
        print(data.timestamp.where(data.timestamp >0).dropna(dim='coords').values[-100:])
        #segmentation based on time init and time last
        data = data.where(
            data.timestamp>=initialization_step, 
            drop=True).where(
            data.timestamp<finalization_step,
            drop=True
        )
        
        #set ts (timestamp), prices and values arrays
        ts = data.timestamp.values
        prices = data.value.values
        volume = data.vol.values
        
        #construct a useful 2D array of shape(#ticks, 3)
        return np.dstack(
            (ts,prices,volume)
        ).reshape(prices.shape[0], 3)

class Decryptor(BaseDecryptor):
    """
    Main Decryptor Class.
    
    Summarize: 
        Transform xarray.Dataset information into a useful format.
    Results:
        Generates a numpy, pd.DataFrame or a .txt format to save.
    
    Parameters
    ----------
    * repo_path: path directory where the zarr-files are located
    * symbol: string of stock symbol ID (e.g., Apple INC = AAPL)
    * date: string of single date as "YYYY-MM-DD"
    * start_date: initial string date as "YYYY-MM-DD" 
    * end_date: final string date as "YYY-MM-DD"
    * save: bool to access saving data as .txt files 
    * dataframe: bool that transforms output in a dataframe
    * storage_path: path directory where .txt files will be saved
    
    Output
    ------
    Output 1:
        *np.array() with shape(#ticks, 3).
        * pd.Dataframe with shape(#ticks,3). 
          Columns: 'ts','price','vol'
        * .txt file in path directory as pd.Dataframe structure.
    """
    def __init__(self, 
                 repo_path,
                 symbol,
                 date = None, 
                 start_date = None, 
                 end_date = None, 
                 full_day = False, 
                 start_time = None, 
                 end_time = None, 
                 save = False, 
                 dataframe = False,
                 storage_path = None):
        
        #defining parameters
        self.repo_path = repo_path
        self.symbol = symbol
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.full_day = full_day
        self.start_time = start_time
        self.end_time = end_time
        self.save = save
        self.dataframe = dataframe
        self.storage_path = storage_path
        
        #check if full_day is requested
        if self.full_day:
            self.start_time = '9:30'
            self.end_time = '16:00'
        
        #check if single 'date' is requested
        if self.date is not None:
            self.start_date = self.date
            self.end_date = self.date
        
        #check if 'save' request is active without path for storage
        if self.save and self.storage_path is None:
            print("Define 'storage_path' direction to save data.")
            sys.exit()
            
    def run_decryptor(self):
        """
        Decryptor Function
        
        Evaluates informations requirements.
        
        Select final result format:
            - 'save = True': .txt file in 'storage_path'
            - 'save = False':
                - 'dataframe = True': returns pd.DataFrame
                - 'dataframe = False': returns np.array(n_days, 3)
        """
        #get range of dates
        range_dates = self.extract_date_available_market(
            self.start_date,
            self.end_date
        )
        
        #iteration over dates
        for date_ in range_dates:
            #path for calling information
            path = self.repo_path+"/"+self.symbol.lower(
            ).replace(" ","")+".zarr"
            
            #define init_time and fin_time
            init_time, fin_time = self.range_time(
                date_, 
                self.start_time, 
                self.end_time
            )
            
            #define np.array of shape (#ticks,3)
            np_result = self.read_zarr(
                path, 
                date_, 
                init_time, 
                fin_time
            )
            
            #check if save is requested
            if self.save: 
                result_ = pd.DataFrame(
                    np_result,
                    columns=["ts","price","vol"]
                ).set_index('ts')
                nameFile = self.symbol+"_"+date_
                result_.to_csv(self.storage_path+nameFile+'.txt')   
                print("{} {} saved".format(self.symbol, date_))
                #save and return None
                return None
            
            #check if dataframe is requested
            if self.dataframe:
                result_ = pd.DataFrame(np_result,
                                       columns=["ts","price","vol"])
                #return dataframe 
                return result_
            #return np.array with shape(#ticks,3) 
            return np_result
        
