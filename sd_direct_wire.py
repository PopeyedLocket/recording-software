''' NOTES:

    TO DO:

        NOW:

            find a way to record

                test current way of recording before you get into CLI stuff
                    current way of recording doesn't have lag which is good
                    it does sound weird in the .wav file though
                        slightly mitigated with amplification
                    the playback with numpy arrays sounds the same though
                        see test_wav_to_sd_outputstream.py
                        can multiple streams go to the same output to play multiple things
                        through the headphones?
                            ... if not, could we sum the numpy arrays and
                            ... give that to one stream and send that to
                            ... the output?

                I should probably get the comp. Mic input set up before CLI stuff
                    need to be able to sing and play guitar simultaniously
                        hear both through the headphones
                        record both
                            in 2 separate files and 1 combined file
                        hopefully the mic won't pick up the guitar to much ...
                            ... if it does, theres mics you can buy for <= $10
                                    https://www.google.com/search?tbm=shop&q=microphone&tbs=vw:l,mr:1,root_cat:530633,cat:234,price:1,ppr_max:90,init_ar:SgVKAwjqAUoHsgQECMmxIA%3D%3D&sa=X&ved=0ahUKEwiV48rbwovjAhVXOs0KHfDFBU4QvSsIrQMoAA&biw=1299&bih=641


                i want to be able to say:
                    ns <name (string)> = new song w/ <name>
                    os <name (string)> = open song w/ <name>
                    vs = view songs
                    nt <name(s) (string)> = new track(s) w/ name(s) = <name(s)>
                    dt <name(s) (string)> = delete track w/ name(s) = <name(s)>
                    ti <input_device_id (int)>  = set track input device
                    to <output_device_id (int)> = set track output device (can sounddevice have multiple output devices?)
                    vd = view all i/o devices
                    mt <name(s) (string)> <> = mute track(s) on specified output devices
                        by default all tracks are played
                    vt <name(s) (string)> --verbose = view track(s) w/ name(s) if no names provoded, default is to view all tracks
                        name
                        input_device_id
                        list of output_device_ids it will play on
                        list of output_device_ids its muted on
                        effects put on it
                        recording(s) start_time, end_time, duration
                    rt (<name (string)> <start_time (int)> <end_time (int)>)(s) = record on track(s) w/ <name(s)>
                        if no names provided, record on all tracks
                        start_time default = 0.000
                        end_time default is infinity
                        during recording, all tracks will be audible unless they are muted

                    help = display all these commands

                    it would also be great if all this UI stuff was independent of sounddevice so I could potentially switch to another library later

                    a.py shows how to print over the current line
                        might be useful to make a very simple CLI when running this script

            also make plot be over time


        LONG TERM:


            set up pedal
                probably just need to create another InputStream w/ sounddevice with a callback function (does InputStream have a callback function? If not, gotta find some way to access the raw data)
                In the callback function (or whatever data stream) there will be a boolean thats constantly being updated, find a way to interpret that to set another global boolean to turn distortion on/off


            setup 2i2 to work with a mic and a guitar
                why does it say the 2i2 only has 2 channels? shouldn't it be 4?

                for now just use computer's mic (and create a 2nd sd.Stream)


            right now sd.default.latency = 'low' in order to decrease latency.

                found here: https://stackoverflow.com/questions/39990274/too-high-latency-while-trying-to-manipulate-sound-arrays-using-sounddevice-in-py

                it does this by decreasing the length of the numpy array 'indata' (from 512 to 128)
                which decreases the quality of the sound (idk why)

                I want to find a way to decrease latency without decreasing sound quality as much.
                Possible solutions are:

                    use:
                        multiprocessing/async-io/etc to do more shit in parallel/concurrently
                            https://realpython.com/async-io-python/#the-10000-foot-view-of-async-io
                            https://docs.python.org/3.4/library/multiprocessing.html?highlight=process
                            https://realpython.com/python-concurrency/

                            i need to find some way to determine whihc parts of the code are currently
                            taking how long and what is waiting on what to run, ect. before I can have
                            any idea how to improve it this way

                        research sd.default.latency (maybe theres a way to set it to 'medium low' or something to put it at 256, maybe 256 wont have noticable latency and quality will be pretty good too)

                        maybe it could just do linear interpolation of the 128 indata and put it back to 512 (or 1024 lol XD)
                            or maybe something smoother than linear interpolation


            make basic frequency chart (aka spectrogram)
                no Key interpretation
                see spectrogram.py


            figure out what 'indata' numpy array represents
                create a new script thats just an OutputStream (to headphones)
                create numpy arrays that are a sine wave with specific note's freqency (middle C)
                plot it over time
                see if the pitch in the headphones matches the pitch on your guitar (don't forget to tune it)
                dig into spectogram.py to figure out how it determines frequency value


            figure out why right headphone data is just static
                right now the hack is simply to copy the left-headphone data into the right
                however from testing it by downloading classical_music.wav files from online
                and playing it through the headphones and outputting the data to the console,
                its clear the data should not be the same in both head phones

                perhaps plot the left and right data on the same plot (one line red, one line blue)
                and see their difference, maybe they're not that different and you just need to
                randomly change the right one a bit from the left to get rid of that chorus sound

                This is why
                https://support.focusrite.com/hc/en-gb/articles/206849779-Why-is-my-microphone-guitar-only-on-the-left-
                https://electronics.stackexchange.com/questions/241610/mono-jack-output-to-stereo-headphones-how-to-send-the-mono-signal-to-both-side
                https://www.reddit.com/r/Advice/comments/470w29/how_do_i_convert_mono_output_to_stereo_so_that_i/
                    this one recommended this:
                        https://www.radioshack.com/products/radioshack-1-8-stereo-jack-to-1-4-mono-plug-adapter#.VstnrDu6EAM.mailto
                    but i think thats what I have?
                        reddit also recommeded a "Y Cord" (aka cheap adapter)

    THOUGHTS:

        I'm worried that:

            when I try to create/copy-in effects for this
            it will increase the latency to much
                does numpy use C in its backend?

            it won't be able to record 2 inputs and output them simulatniously

        It would be cool to create an effect like the piano pedal where you can hold it down
        and whatever notes are played when its held down are elongated even when you stop
        holding the note

        It would be cool if the Program could figure out what time signature you're playing
        in by simply listening to you play
            as a musician your time signature is going to fluctuate slightly ...
            and you could set it to either go with it (because maybe you want the song to speed up or slow down)
            or you could tell it to stick with whatever time signature it first identified (to keep you the musician on track)

            it would be nice if this was then played back in the headphones or displayed with a blinking light on the pedal or with some display on the computer screen

            this could be useful for
            having the computer properly time the switch from 1 effect to another (triggered with foot pedal), thus allowing the musician to press the pedal slightly before the

        It would be cool if it could Identify what key you are playing in and
        display horizontal lines on the screen for each note in the key
            and when you stop playing the lines go away

            ... having horizontal and vertical lines (for key and time sig. respectivewly) appear on a black screen when you start playing and disappearing when you stop would be dope!!!!

        It would be cool if you could pre-set the algorithm to apply various
        effects at various points in the song (identified with AI)

        keep messing around with effects


    '''


import queue
import sys
import timeit

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=10)
import sounddevice as sd
sd.default.latency = 'low'
plotdata = np.zeros(128)
# print(plotdata)
# print(plotdata.shape)
# sys.exit()



SAMPLERATE = 44100

RECORDING = True


# mapping = [c - 1 for c in CHANNELS]  # Channel numbers start with 1
q = queue.Queue()

# used for recording all the data
# all_data = np.array([[0.0, 0.0]])
all_data = []

cubic = lambda x : x - (1/3)*(x**3)

alpha = 5000
arctan = lambda x : (2 / np.pi) * np.arctan(alpha * x)

# https://dsp.stackexchange.com/questions/13142/digital-distortion-effect-algorithm
f = lambda x : \
    np.where(
        x > 0,
        1.0 - np.exp(-x),
        -1.0 + np.exp(x))

# def audio_callback(indata, frames, time, status):
def audio_callback(indata, outdata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""

    # outdata[:] = indata  # this wires input directly into output
    # for some reason the right headphone data is just a bunch of static
    # so I copied the left headphone data (which is good) into the right

    # # clean:
    # outdata[:] = 10 * np.repeat(indata[:,0][:,np.newaxis], 2, 1)


    # # distortion effects:

    # # full wave rectifier
    # # "negative values are set to their positive equivalent" (paraphrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/full-wave-rectification/
    # outdata[:] = 10 * np.repeat(np.absolute(indata[:,0])[:,np.newaxis], 2, 1)

    # # half wave rectifier
    # # "negative values are set to zero" (paraphrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/full-wave-rectification/
    # # https://stackoverflow.com/questions/3391843/how-to-transform-negative-elements-to-zero-without-a-loop
    # outdata[:] = 10 * np.repeat(np.clip(indata[:,0], a_min=0, a_max=None)[:,np.newaxis], 2, 1)

    # # infinite clipping
    # # "all positive values are set to the maximum value, and all negative values are set to the minimum value." (para-phrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/infinite-clipping/
    # # https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html
    # outdata[:] = 0.05 * np.repeat(np.where(indata[:,0][:,np.newaxis] > 0, 1.0, -1.0), 2, 1)

    # hard clipping
    # "if signal goes above max, its set to max; it if goes below min, its set to min" (paraphrased)
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/hard-clipping/
    # this will propably give a clean sound when nothing is being played
    amplitude = 500.0
    threshold = 0.0005
    outdata[:] = amplitude * \
        np.repeat(
            np.clip(
                indata[:,0],
                a_min=-threshold,
                a_max=threshold,
                out=indata[:,0])[:,np.newaxis],
            2, 1)
    # print(outdata[:,0][:,np.newaxis].shape)

    # # soft clipping
    # # "same as hard clippling but with smooth curve instead" (paraphrased)
    # # cubic fuction:    output = input - (1 / 3)*input^3
    # # arc tan function: output = 2 / pi * arctan(alpha*input)
    # #     "alpha" values typically range from 1 to 10. If alpha is way more than 10, softclippling approaches infinite clipping
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/soft-clipping/
    # amplitude = 100.0
    # left_indata = indata[:,0][:,np.newaxis]
    # outdata[:] = amplitude * \
    #     np.repeat(
    #         # cubic(left_indata),
    #         # arctan(left_indata),
    #         f(left_indata),
    #         2, 1)
    

    # # bit crushing
    # # "round signal to -1, 0, or 1 (or any combo you want)" (para-phrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/bit-crushing/
    # amplitude = 100.0
    # threshold = 0.0005
    # left_indata = indata[:,0][:,np.newaxis]
    # hard_clipping = np.clip(left_indata, a_min=-threshold, a_max=threshold)
    # in_range = np.logical_and(-threshold < hard_clipping, hard_clipping < threshold)
    # outdata[:] = amplitude * \
    #     np.repeat(
    #         # 10 * (10e6 * left_indata).astype(int) / 10e7,
    #         np.where(
    #             in_range,
    #             0, hard_clipping),
    #         2, 1)
    # # print(outdata[:,0][:,np.newaxis].shape)

    if RECORDING:
        all_data.append(outdata.copy())

    # print('outdata')
    # print(outdata.shape)
    # print(outdata)

    # # used to verify outdata still has same precision indata has
    # print(np.format_float_scientific(outdata[0][0], unique=False, precision=15))

    # # Fancy indexing with mapping creates a (necessary!) copy:
    # # q.put(outdata[::DOWNSAMPLE, mapping])
    # q.put(outdata[:,0][:,np.newaxis])

# def update_plot(frame):
#     """This is called by matplotlib for each plot update.

#     Typically, audio callbacks happen more frequently than plot updates,
#     therefore the queue tends to contain multiple blocks of audio data.

#     """
#     # global plotdata
#     # while True:
#     #     try:
#     #         data = q.get_nowait()
#     #     except queue.Empty:
#     #         break
#     #     # print(data.shape)
#     #     # print(data)
#     #     # print()

#     #     # shift = len(data)
#     #     # plotdata = np.roll(plotdata, -shift, axis=0)
#     #     # plotdata[-shift:, :] = data

#     #     plotdata = data
#     # for column, line in enumerate(lines):
#     #     # line.set_ydata(plotdata[:, column])
#     #     line.set_ydata(plotdata)
#     plotdata = q.get_nowait()

#     # print(outdata.shape)

#     # recording eventually gets laggy this way
#     # global all_data
#     # all_data = np.concatenate((all_data, outdata))
#     # all_data += outdata.tolist()
#     # print(len(all_data))


#     for column, line in enumerate(lines):
#         line.set_ydata(plotdata)
#     return lines

s = sd.Stream(
    device=(4, 4),
    samplerate=SAMPLERATE,
    channels=2,
    callback=audio_callback)

# fig, ax = plt.subplots()
# lines = ax.plot(plotdata)
# # ax.set_ylim((-10.0, 10.0))
# ax.set_ylim((-0.5, 0.5))
# ax.yaxis.grid(True)
# ani = FuncAnimation(fig, update_plot, interval=50, blit=True)

with s:
    input()
    # plt.show()
    # while True:
    #     user_input = input()
    #     if user_input == 'r':
    #         if RECORDING:
    #             RECORDING = False
    #         else:
    #             all_data = []
    #             RECORDING = True
    #     if user_input == 'p':
    #         if PLAYING:
    #             PLAYING = False

# save recorded data to .wav and .txt files
if RECORDING:

    all_data = 20 * np.reshape(
        all_data,
        (len(all_data)*len(all_data[0]), 2))
    wav2 = 'wav2.wav'
    import soundfile as sf
    sf.write(wav2, all_data, SAMPLERATE)

    fn = 'txt2.txt'  # this is just to compare .wav to raw numpy array
    open(fn, 'w').close() # clear file
    f = open(fn, 'w')
    for i, v in enumerate(all_data):
        f.write('%s\n' % v)
        if i > 100:
            break



