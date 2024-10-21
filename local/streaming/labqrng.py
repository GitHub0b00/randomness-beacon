import numpy as np


# num_words means the number of bytes requsted for the random string.
def optical(gate_time, counter):

    # signal_type to be choosen from 'nim' and 'ttl'
    signal_type = 'nim'

    result = []

    # this line of code collect the random bits from the s15 timetagger
    [timestamp, pattern] = (counter.timestamp_acq_python(gate_time, signal_type))

    data = list(zip(pattern, timestamp))

    ch1 = np.zeros(len(data))
    ch2 = np.zeros(len(data))
    ch3 = np.zeros(len(data))

    # convert data into arrays. These arrays record the time stamps of each detection event.
    for i in range(len(data)):
        if data[i][0] == '00100':
            ch3[i] = float(data[i][1])
        if data[i][0] == '00010':
            ch2[i] = float(data[i][1])
        if data[i][0] == '00001':
            ch1[i] = float(data[i][1])
    # The above block of code is wrong. The correct version is attached as comments because it has not been tested in this file. The correct version was tested and used for data collection for randomness test, but it was not tested for deployment use in this file.
    # for i in range(len(data)):
    #     if data[i][0][2] ==  '1':
    #         ch3[i] = float(data[i][1])
    #     if data[i][0][3] == '1':
    #         ch2[i] = float(data[i][1])
    #     if data[i][0][4] == '1':
    #         ch1[i] = float(data[i][1])

    # For each timestamp from ch1 and ch2. If there is an detection event from ch3, between the immediate neighbors, who has timestamps that are closer than 5ns away, then it is considered as a coincidance. These coincidance timstamps are selected out and put into the coincidance array.
    coinch1 = np.zeros(len(data))
    ct1 = 0
    tot1 = 0
    for i in range(len(ch1)-1):
        if ch1[i] != 0:
            tot1 += 1
            if abs(ch3[i+1] - ch1[i]) < 5 or abs(ch3[i-1] - ch1[i]) < 5 or abs(ch3[i] - ch1[i]) < 5:
                coinch1[i] = ch1[i]
                ct1 += 1

    coinch2 = np.zeros(len(data))
    ct2 = 0
    tot2 = 0
    for i in range(1, len(ch2)-1):
        if ch2[i] != 0:
            tot2 += 1
            if abs(ch3[i+1] - ch2[i]) < 5 or abs(ch3[i-1] - ch2[i]) < 5 or abs(ch3[i] - ch2[i]) < 5:
                # print(ch3[i+1] - ch2[i], i)
                coinch2[i] = ch2[i]
                ct2 += 1
    
    # Now, from the coincidance arrays of timestamps, the coincidance of coincidance arrays can be obtained in the same way. This time, only the sum is needed.
    # The sum of coincidances denotes the total number of triple coincidance in the time window between the first timestamp and the last timestamp in the time stamp returned by the function from s-15 data collection line.
    coin = 0
    for i in range(1, len(coinch2)-1):  # This way, we are omitting the first and last bit of coinch2.
        if (abs(coinch2[i] - coinch1[i]) < 5 or abs(coinch2[i] - coinch1[i+1]) < 5 or abs(coinch2[i] - coinch1[i-1]) < 5) and coinch2[i] != 0:
            coin += 1
    # print(data, coinch1, coinch2, coin, ct1, ct2, tot1, tot2)
    print(coin, ct1, ct2, tot1, tot2)
        

    # Assemble the registered coincidance array for ch1 and ch2 into string of zeros and ones.
    string = ''
    for i in range(len(coinch2)):
        if coinch1[i] != 0 and coinch2[i] == 0:
            string += '1'
        if coinch2[i] != 0 and coinch1[i] == 0:
            string += '0'

    try:
        g2 = coin / (ct1 * ct2)  # coin denotes the sum of intensities for Intensity_ch1 * Intensity_ch2. In proper definition, both denominator and numerator need to be divided by the total number of "detection plus no-detection". This number will be simply 1 over the detection frequency. 
    except ZeroDivisionError:
        return string, ["None", "None", "None"]
#     # Gaurentee that enough bits of randomness are generated
#     if len(string) < (num_words * 8):
#         substr = '0' * (num_words*8 - len(string)) + string[-num_words*8:]
#         print('Not enough random bits generated from lab qrng')
#     else:
#         substr = string[-num_words*8:]

#     # Enumerate the random bits generated. For each 8-bits group, first, convert them into 10-based integer from 2-based. Then, input the 10-based integer into the chr function to return the ASCII character.
#     re = ''
#     for i in range(num_words):
#         if i == num_words - 1:
#             hex_ = chr(int(substr[-(num_words-i)*8:], 2))
#         else:
#             hex_ = chr(int(substr[-(num_words-i)*8:(-(num_words-i-1)*8)], 2))
#         re += hex_
#         if len(re.encode()) >= num_words:
#             break

    return string, [format(g2, '.3f'), format((ct1/tot1), '.3f'), format((ct2/tot2), '.3f')]  # string.encode()
