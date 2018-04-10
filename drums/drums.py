from flask import Flask

app = Flask(__name__, static_url_path='/static')
from pydub import AudioSegment

drum_kit={
    "clhat":    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
    "crash":    [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    "hightom":  [0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
    "midtom":   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "lowtom":   [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
    "kick":     [1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0],
    "ophat":    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "snare":    [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0]
}
import os


def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


# print (os.path.join(app.root_path, 'sound', "mu.mp3")
# old = AudioSegment.from_file(os.path.join(app.root_path, 'sound', "bb.wav"))
# old=old+15
# old.export(os.path.join(app.root_path, 'sound', 'musicc.wav'), format='wav')

@app.route('/guitar')
def hello_world():

    kk = 250
    cnt=16000/kk
    ass = AudioSegment.silent(duration=cnt * kk)

    second_of_silence = AudioSegment.silent(duration=1000)
    for i in range(0, cnt):
        j = i
        i = i % 16
        comm = None
        for key in drum_kit:
            if (drum_kit[key][i] == 1):
                if (comm == None):
                    comm = AudioSegment.from_file(os.path.join(app.root_path, 'sound', key+".wav"))
                else:
                    sd = AudioSegment.from_file(os.path.join(app.root_path, 'sound', key+".wav"))
                    comm = comm.overlay(sd)

        if (comm != None):
            comm = AudioSegment.silent(duration=j * kk) + comm
            ass = ass.overlay(comm)
    ass.export(os.path.join(app.root_path, 'sound', 'combined.wav'), format='wav')

    old=None

    try:
        old = AudioSegment.from_file(os.path.join(app.root_path, "music.wav"))
    except:
        pass
    if old != None:
        ass=ass.overlay(old)

    ass.export(os.path.join(app.root_path, 'sound', 'music.wav'), format='wav'
    return 'done'

@app.route('/slower')
def slow_world():
    old=None
    try:
        old = AudioSegment.from_file(os.path.join(app.root_path,'sound',  "mu.mp3"))
    except:
        pass
    if old==None:
        return 'ndone'
    slow_sound = speed_change(old, 0.75)
    slow_sound = slow_sound[:len(slow_sound)*3/4]
    slow_sound.export(os.path.join(app.root_path, 'sound', 'musicslow.wav'), format='wav')
    return 'done'

@app.route('/faster')
def fast_world():
    old = None
    print (os.path.join(app.root_path, 'sound', "mu.mp3"))
    old = AudioSegment.from_file(os.path.join(app.root_path, 'sound', "mu.mp3"))

    if old == None:
        return 'ndone'

    fast_sound = speed_change(old, 2.0)
    fast_sound=fast_sound*2
    fast_sound.export(os.path.join(app.root_path, 'sound', 'musicfast.wav'), format='wav')
    return 'done'

if __name__ == '__main__':
    app.run(port=5555)
