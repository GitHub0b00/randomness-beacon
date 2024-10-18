import numpy as np
import usbcount_class as UC
import time
import json
import os
import pickle
import datetime
import hashlib
import pymongo
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA512
from Cryptodome.PublicKey import RSA
from db_var import *


def init():
    pass

def main(opt_restart):
    numberofpulses = 1000000000
    client = pymongo.MongoClient(ip_address)


    dic_prev = dict()
    dic_prev['uri'] = None
    dic_prev['outputValue'] = None 

    
    if opt_restart == 'continue':
        if os.path.exists('data.json'):
            print('found old pulse in the folder')
            # os.system("scp -i 'Keypair/NUSPC5287.pem' data.json ubuntu@ec2-18-139-114-157.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/deployment/MDB")
            os.system("scp -i 'Keypair/test_db.pem' data.json ubuntu@13.213.139.55:/home/ubuntu/MDB")
            print('old json pulse has been sent to aws ec2 remote server')
            with open('data.json') as file:
                dic_prev = json.load(file)
                chainIndex = dic_prev['chainIndex']
                pulseIndex = dic_prev['pulseIndex'] + 1
        else:
            print('There is no previous pulse stored in the folder, a new chain will be started per reference requirement')
            pulseIndex = 1
            chainIndex = int(input("Please type in the new chain index:\n")) #This would need to be automated here by querying the database
    
    if opt_restart == 'new':
        pulseIndex = 1
        chainIndex = int(input("Please type in the new chain index:\n"))

    # Generate Private Key and Public Key ####Should pack into function
    key = RSA.generate(4096)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()

    init_dac0 = os.system('./qrng3/apps/setdac -v 35000 -d /dev/ioboards/qrng_t30')
    init_dac1 = os.system('./qrng3/apps/setdac -v 35000 -d /dev/ioboards/qrng_t31')

    # Control the time to start at exact minute
    print('waiting for the exact minute')
    time.sleep(60 - datetime.datetime.now(tz=datetime.timezone.utc).second)
    print(f'start to generate pulse at {datetime.datetime.now(tz=datetime.timezone.utc)}')

    for _ in range(numberofpulses):
        
        status = '0'

        timee_ = datetime.datetime.now(tz=datetime.timezone.utc)
        startmin = timee_.minute
        starthour = timee_.hour

        dic_cur = dict()
        # The implementation here is different from the document to ensure that pulse one has a local   random value. In the documentation, it was said that pulse one should have local random value to be default all zeros.
        if pulseIndex == 1: 
            status = '01'
            # for i in range(1024):                
            # Problem: We have 512 digits of 0 and 1 but it is not 512 bits in memory.
            # st += str(np.random.choice([0, 1]))
            out1_0 = os.system('./qrng3/apps/sampleadc -d /dev/ioboards/qrng_t30 -m1 -b -n 64 -o outputfiletest0') # out1 is not used. This variable can be deleted, leaving only the os.system part.
            # out1_op = optical(128, counter)
            out1_1 = os.system('./qrng3/apps/sampleadc -d /dev/ioboards/qrng_t31 -m1 -b -n 64 -o outputfiletest1')

            with open('outputfiletest0', 'rb') as f:
                st0 = f.read()
            with open('outputfiletest1', 'rb') as f:
                st1 = f.read()
                
            os.remove('outputfiletest0')
            os.remove('outputfiletest1')

            if os.path.exists('outputfiletest0'):
                print('s15 output file 0 not deleted')
            if os.path.exists('outputfiletest1'):
                print('s15 output file 1 not deleted')

            if len(st0) != 128 or len(st1) != 128:  #To add more security percautions. Here 128 numbers means 128 bytes, means 1024 bits
                print(f"ChainId: {chainIndex}, PulseId: {pulseIndex}. Not Enough Random Bytes from QRNG, Length of String is {len(st)} from s15, {len(out1_op)} from the lab")
                chainIndex += 1
                continue
            # LocalRandomValue
            dic_cur['localRandomValue'] = hashlib.sha512(st0[:64]+st1[:64]).hexdigest()
            pre = hashlib.sha512(st0[64:]+st1[64:]).hexdigest()#st[512:] #Note that pre is always a hash value. Even though it is passed into another hash function to create precommitmentValue
            dic_cur['precommitmentValue'] = hashlib.sha512(pre.encode('ISO-8859-1')).hexdigest()
        else:
            out2_0 = os.system('./qrng3/apps/sampleadc -d /dev/ioboards/qrng_t30 -m1 -b -n 32 -o outputfiletest0') # out2 is not used. This variable can be deleted, leaving only the os.system part.
            # out2_op = optical(64, counter)
            out2_1 = os.system('./qrng3/apps/sampleadc -d /dev/ioboards/qrng_t31 -m1 -b -n 32 -o outputfiletest1')
            
            with open('outputfiletest0', 'rb') as f:
                st0 = f.read()
            with open('outputfiletest1', 'rb') as f:
                st1 = f.read()
            
            os.remove('outputfiletest0')
            os.remove('outputfiletest1')

            if os.path.exists('outputfiletest0'):
                print('s15 output file 0 not deleted')
            if os.path.exists('outputfiletest1'):
                print('s15 output file 1 not deleted')

            if len(st0) != 64 or len(st1) != 64:  #To add more security percautions. 64 numbers -> 64 bytes -> 512 bits
                print(f"ChainId: {chainIndex}, PulseId: {pulseIndex}. Not Enough Random Bytes from QRNG, Length of String is {len(st)} from s15, {len(out2_op)} from the lab")
                chainIndex += 1
                continue
            # dic_cur['localRandomValue'] = pre
            try:
                dic_cur['localRandomValue'] = pre
            except NameError:
                if os.path.exists('next_locrand.pkl'):
                    status = '0'
                    with open('next_locrand.pkl', 'rb') as f:
                        pre = pickle.load(f)
                        dic_cur['localRandomValue'] = pre #os.environ['NEXT_LOCAL_RANDOM']
                else:
                    status = '1'
                    dic_cur['localRandomValue'] = 'The lrv for computation of the pre commitment value from the previous pulse is not found'
            #hashlib.sha512(pre.encode('ISO-8859-1')).hexdigest() #dic_prev['precommitmentValue']
            pre = hashlib.sha512(st0+st1).hexdigest() #update pre to be the latest random string, hashed #st #update pre to be the latest random string. #Note that pre is always a hash value. Even though it is passed into another hash function to create precommitmentValue
            dic_cur['precommitmentValue'] = hashlib.sha512(pre.encode('ISO-8859-1')).hexdigest()
        
        # delete the previously saved local random value to make sure the file has new values saved in the next 2 lines.
        if os.path.exists('next_locrand.pkl'):
            os.remove('next_locrand.pkl')
        
        with open('next_locrand.pkl', 'wb') as f: #serialize the local random value for the next pulse into the pickle file in case of program failure.
            pickle.dump(pre, f)

        #URI
        #To be added more fields in URI
        dic_cur['uri'] = 'https://www.quantum-entropy.sg/rng/chainIndexandpulseIndex?chainIndex=' + str(chainIndex) + '&pulseIndex=' + str(pulseIndex)
        dic_cur['pulseIndex'] = pulseIndex
        dic_cur['chainIndex'] = chainIndex

        # TimeStamp
        # obtain UTC timestamp
        t = datetime.datetime.now(tz=datetime.timezone.utc)
        tt = str(t).replace(' ', 'T')[:-12] + str(round(t.microsecond / 1000)) + 'Z'
        dic_cur['timeStamp'] = tt
        dic_cur['year'] = t.year
        dic_cur['month'] = t.month
        dic_cur['day'] = t.day
        dic_cur['hour'] = t.hour
        dic_cur['minute'] = t.minute
        
        if pulseIndex != 1:
            time_diff = (((int(dic_cur['year'])-int(dic_prev['year'])) * 365 * 24 * 60) + ((int(dic_cur['month'])-int(dic_prev['month'])) * 30 * 24 * 60) + ((int(dic_cur['day'])-int(dic_prev['day'])) * 24 * 60) + ((int(dic_cur['hour'])-int(dic_prev['hour'])) * 60) + (int(dic_cur['minute'])-int(dic_prev['minute'])))
            if time_diff > 1:
                status = '1' + status
            else:
                status = '0' + status

        t_prevhour = t - datetime.timedelta(hours=1)

        #Skip list dictionaries.
        # minute (previous) skip list

        lst = []
        previous = dict()
        previous['uri'] = dic_prev['uri']#'www.www.www'
        previous['type'] = 'previous'
        previous['value'] = dic_prev['outputValue']

        # hour skip list
        hr = dict()

        try:
            dic_prev['hour']
            flag = True
        except KeyError:
            flag = False

        if flag:
            hour = dic_prev['hour']
            skip_hour = list(client[database_name][collection_name].find({'chainIndex': dic_prev['chainIndex'], 'hour': hour, 'day': dic_prev['day'], 'month': dic_prev['month'], 'year': dic_prev['year']}).sort("minute", 1).limit(1))
            if len(skip_hour) == 0:
                hr['uri'] = "ERROR_NO_RECORD_FOUND"
                hr['type'] = 'hour'
                hr['value'] = "ERROR_NO_RECORD_FOUND"
            else:
                dic_hour = skip_hour[0]
                hr['uri'] = dic_hour['uri']
                hr['type'] = 'hour'
                hr['value'] = dic_hour['outputValue']

        else:
            hr['uri'] = "THIS_IS_THE_FIRST_PULSE_OR_HOUR_DID_NOT_FOUND"
            hr['type'] = 'hour'
            hr['value'] = "THIS_IS_THE_FIRST_PULSE_OR_HOUR_DID_NOT_FOUND"


        # day skip list
        day = dict()

        try:
            dic_prev['day']
            flag = True
        except KeyError:
            flag = False

        if flag:
            daay = dic_prev['day']
            skip_day = list(client[database_name][collection_name].find({'chainIndex': dic_prev['chainIndex'], 'day': daay, 'month': dic_prev['month'], 'year': dic_prev['year']}).sort([("hour", 1), ("minute", 1)]).limit(1))
            if len(skip_hour) == 0:
                day['uri'] = "ERROR_NO_RECORD_FOUND"
                day['type'] = 'hour'
                day['value'] = "ERROR_NO_RECORD_FOUND"
            else:
                dic_day = skip_day[0]
                day['uri'] = dic_day['uri']
                day['type'] = 'day'
                day['value'] = dic_day['outputValue']

        else:
            day['uri'] = "THIS_IS_THE_FIRST_PULSE_OR_DAY_DID_NOT_FOUND"
            day['type'] = 'day'
            day['value'] = "THIS_IS_THE_FIRST_PULSE_OR_DAY_DID_NOT_FOUND"


        # month skip list
        mth = dict()

        try:
            dic_prev['month']
            flag = True
        except KeyError:
            flag = False

        if flag:
            month = dic_prev['month']
            skip_month = list(client[database_name][collection_name].find({'chainIndex': dic_prev['chainIndex'], 'month': month, 'year': dic_prev['year']}).sort([("day", 1), ("hour", 1), ("minute", 1)]).limit(1))
            if len(skip_hour) == 0:
                mth['uri'] = "ERROR_NO_RECORD_FOUND"
                mth['type'] = 'month'
                mth['value'] = "ERROR_NO_RECORD_FOUND"
            else:
                dic_month = skip_month[0]
                mth['uri'] = dic_month['uri']
                mth['type'] = 'month'
                mth['value'] = dic_month['outputValue']

        else:
            mth['uri'] = "THIS_IS_THE_FIRST_PULSE_OR_MONTH_DID_NOT_FOUND"
            mth['type'] = 'month'
            mth['value'] = "THIS_IS_THE_FIRST_PULSE_OR_MONTH_DID_NOT_FOUND"


        # year skip list
        yrs = dict()

        try:
            dic_prev['year']
            flag = True
        except KeyError:
            flag = False

        if flag:
            year = dic_prev['year']
            skip_year = list(client[database_name][collection_name].find({'chainIndex': dic_prev['chainIndex'], 'year': year}).sort([("month", 1), ("day", 1), ("hour", 1), ("minute", 1)]).limit(1))
            if len(skip_year) == 0:
                yrs['uri'] = "ERROR_NO_RECORD_FOUND"
                yrs['type'] = 'month'
                yrs['value'] = "ERROR_NO_RECORD_FOUND"
            else:
                dic_year = skip_year[0]
                yrs['uri'] = dic_year['uri']
                yrs['type'] = 'year'
                yrs['value'] = dic_year['outputValue']

        else:
            yrs['uri'] = "THIS_IS_THE_FIRST_PULSE_OR_YEAR_DID_NOT_FOUND"
            yrs['type'] = 'month'
            yrs['value'] = "THIS_IS_THE_FIRST_PULSE_OR_YEAR_DID_NOT_FOUND"

        chainIn = dic_cur['chainIndex']

        lst.append(previous)
        lst.append(hr)
        lst.append(day)
        lst.append(mth)
        lst.append(yrs)

        dic_cur['listValues'] = lst

        #Generate the signature based on all previous fields
        message = ''
        for value in dic_cur.values():
            if type(value) is list:
                for val in value:
                    for v in val.values():
                        if v is not None:
                            message += v
            else:
                message += str(value)
        message = message.encode('ISO-8859-1')

        key = RSA.import_key(open('private.pem').read())
        h = SHA512.new(message)
        signature = pkcs1_15.new(key).sign(h)
        dic_cur['signatureValue'] = signature.hex()

        allfields = ''
        for value in dic_cur.values():
            if type(value) is list:
                for val in value:
                    for v in val.values():
                        if v is not None:
                            allfields += v
            else:
                allfields += str(value)

        dic_cur['outputValue'] = hashlib.sha512(allfields.encode('ISO-8859-1')).hexdigest()
        dic_cur['status'] = status
        dic_prev = dic_cur.copy()
        
        # Send pulse to remote machine
        if os.path.exists('data.json'):
            os.remove('data.json')
            if not os.path.exists('data.json'):
                print('previous pulse data removed from the current folder')
        
        with open('data.json', 'w') as outfile:
            json.dump(dic_cur, outfile)
        
        if os.path.exists('data.json'):
            print('new pulse data added to the current folder')
        
        if os.path.exists('data.json'):
            os.system("scp -i 'Keypair/test_db.pem' data.json ubuntu@13.213.139.55:/home/ubuntu/MDB")
            print('json data is sent to aws ec2 remote server')
        else:
            print(f'json data not found in the current folder at around {datetime.datetime.now(tz=datetime.timezone.utc).hour}, minute: {datetime.datetime.now(tz=datetime.timezone.utc).minute}, second: {datetime.datetime.now(tz=datetime.timezone.utc).second}')
        
        # Insert pulse to local database
        client[database_name][collection_name].insert_one(dic_cur)
        print(f'Pulse was inserted at around hour: {datetime.datetime.now(tz=datetime.timezone.utc).hour}, minute: {datetime.datetime.now(tz=datetime.timezone.utc).minute}, second: {datetime.datetime.now(tz=datetime.timezone.utc).second}')

        # Time Control Block
        # Check if the current loop has taken more than 1 minute
        timee_ = datetime.datetime.now(tz=datetime.timezone.utc)
        finishmin = timee_.minute
        finishhour = timee_.hour
        if finishmin != startmin:
            print('Loop took longer than 1 minute')
        else:
            # wait until te full minute is reached
            time.sleep(60-datetime.datetime.now(tz=datetime.timezone.utc).second)
        
        pulseIndex += 1

        print(f'progress: {_}/1000000000')

if __name__ == "__main__":
    # ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    # print("I'm at IP " + ip)
    print("run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    print("to launch the api locally")
    
    opt_restart = ''
    while opt_restart != 'new' and opt_restart != 'continue':
        opt_restart = input('Please decide if we hope to continue from the last pulse before the system crashed, type new to start a new chain, type continue to continue from the last pulse in this folder:\n')
    
    main(opt_restart)
