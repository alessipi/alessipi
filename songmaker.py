from psonic import *
from threading import *
import csv, pathlib, time
#definition of the volume values of the tracks 
vol_main=2
vol_bass=0.3
#here starts the program
file=pathlib.Path(__file__).with_name("data.csv")
data=list()
rolls=list()
pitchs=list()
yaws=list()
magns=list()
lats=list()
longs=list()
ndvis=list()
scale=["G", "A", "B", "D", "E"]
with open(file, newline='') as csvfile:
    """open the csv file"""
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        data.append(row)
data=data[441:593]
for row in data:
    """in this part it takes the data of the csv file and separate it into 6 lists for each value, except the ndvi"""
    row= str(row)[1:-1].split("\"")
    lat=row[8][1:-3].split("/1")
    long=row[16][1:-3].split("/1")
    roll, pitch, yaw, magn, lat, long= float(row[1][14:-4]), float(row[3][3:-4]), float(row[5][3:-1]), float(row[6][1:-1]), float(lat[0])+(float(lat[1][1::])+(float(lat[2][1::])/600))/60, float(long[0])+(float(long[1][1::])+(float(long[2][1::])/600))/60
    rolls.append(roll)
    pitchs.append(pitch)
    yaws.append(yaw)
    magns.append(magn)
    lats.append(lat)
    longs.append(long)
ndvif=data[::4]+data[148]
for row in ndvif[:-1]:
    """here we catch the 4 value of ndvi and put it in a list"""
    row= str(row)[1:-1].split("\"")
    try:
        sus= row[21][1:-1].split(",\', \'")
        for ndvi in sus:
            ndvis.append(float(ndvi))
    except: 
        None
def main_instr(ndvis, scale):
    """this function create the music track of the main instrument, made with the FM synthesizer of Sonic Pi"""
    for ndvi in ndvis:
        if ndvi<=0.4:
            oct= '4' if int(ndvi//0.08)<4 else '5'
            synth(FM, note = ":"+scale[int(ndvi//0.08)-1]+oct, amp=vol_main )
            sleep(0.5)
        elif ndvi<=1:
            oct= '5' if int((ndvi-0.4)//0.12)<4 else '6'
            synth(FM, note = ":"+scale[int((ndvi-0.4)//0.12)-1]+oct, amp=vol_main )
            sleep(0.5)
        elif ndvi<=2:
            oct= '6' if int((ndvi-1)//0.2)<4 else '7'
            synth(FM, note = ":"+scale[int((ndvi-1)//0.2)-1]+oct, amp=vol_main )
            sleep(0.5)
        else:
            synth(FM, note = ":G7", amp=vol_main )
            sleep(0.5)
def bass_instr(lats, scale):
    """this function create the music track of the bass, a sort of, made with the SQUARE synthesizer of Sonic Pi"""
    for lat in lats:
        if lat<=29:
            oct= '0' if int((lat-19)//2)<4 else '1'
            synth(SQUARE, note = ":"+scale[int((lat-19)//2)-1]+oct, amp=vol_bass)
            sleep(0.5)
        elif lat<=39:
            oct= '1' if int((lat-29)//2)<4 else '2'
            synth(SQUARE, note = ":"+scale[int((lat-29)//2)-1]+oct, amp=vol_bass)
            sleep(0.5)
        else: 
            oct= '2' if int((lat-19)//2)<4 else '3'
            synth(SQUARE, note = ":"+scale[int((lat-39)//2)-1]+oct, amp=vol_bass)
            sleep(0.5)
def drum_instr(pitchs, rolls, yaws, magns):
    for i in range (152):
        """this function create the music track of the drums, made of the sample pack of Sonic Pi"""
        sample(DRUM_BASS_SOFT, amp=(pitchs[i]/300))
        sample(DRUM_SNARE_SOFT, amp=(rolls[i]/300))
        sample(DRUM_CYMBAL_CLOSED, amp=(yaws[i]/400), pan=-1)
        sample(DRUM_CYMBAL_CLOSED, amp=(magns[i]/400), pan=1)
        sleep(0.5)
#the function below starts recording the track 
start_recording()
#in this part we put together the 3 music track, more or less at the same time
main = Thread(name='producer', target=main_instr, args=(ndvis, scale))
bass = Thread(name='consumer1', target=bass_instr, args=(lats, scale))
drum = Thread(name='consumer1', target=drum_instr, args=(pitchs, rolls, yaws, magns))
main.start()
bass.start()
drum.start()
time.sleep(86)
#the 2 functions below stop the recording process and save the music track in .wav 
stop_recording()
save_recording(str(pathlib.Path(__file__).with_name("astropi_song.wav")))