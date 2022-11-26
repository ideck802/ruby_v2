from threading import Timer
import speech_recognition as sr
import pvporcupine
import pyaudio
import alsaaudio
import struct
import time
import lights

porcupine = None
pa = pyaudio.PyAudio()
audio_stream = None

# api key for picovoice, for porcupine keyword recognition
picovoice_key = None

mic = sr.Microphone()
recog = sr.Recognizer()
mixer_record = alsaaudio.Mixer('Capture')

# text that would be said to hail Ruby
# (changing these doesn't change what is recognized)
hail_texts = ['Ruby listen', 'Hey Ruby']

translate_speech = None

# manually drop the mic volume for a bit to make the listener
# think that someone stopped talking
def timeout():
    print('timeout')
    base_vol = mixer_record.getvolume(alsaaudio.PCM_CAPTURE)[0]
    mixer_record.setvolume(base_vol-50)
    time.sleep(3)
    mixer_record.setvolume(base_vol)


# (called from index)
# starts loop and brings feedback for interpreting incoming text
def stt_init(interperet_speech):
    global translate_speech
    translate_speech = interperet_speech
    start_stt()

# start the loop that listens for a hotword/trigger word to be said
def start_stt():
    run_stt = True

    porcupine = pvporcupine.create(
        access_key = picovoice_key,
        keyword_paths=['./key_files/ruby-listen_en_raspberry-pi_v2_1_0.ppn', './key_files/hey-ruby_en_raspberry-pi_v2_1_0.ppn']
    )

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while run_stt:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            run_stt = False
            porcupine.delete()
            audio_stream.close()
            lights.flash(2)
            reset_audio_level()
            print('Yes?')
            lights.pulsing_start()
            translate_speech(hail_texts[keyword_index])
            timeout_timer = Timer(8, timeout)
            timeout_timer.start()
            translate_speech(listen_for_commands(timeout_timer))
            lights.flashing_stop()
            #lights.off()
            start_stt()

# listen for a longer, more detailed command    
def listen_for_commands(timeout_timer):
    #mic = sr.Microphone()

    with mic as source:
        audio = recog.listen(source)
        lights.pulsing_stop()
        print('Got it! Now to recognize it...')
        lights.flashing_start()
        try:
            value = recog.recognize_google(audio)
            print('You said ' + value)
            timeout_timer.cancel()
            return value

        except sr.UnknownValueError:
            print('Oops! Didn\'t catch that')
        except sr.RequestError as e:
            print('Uh oh! Couldn\' request results; ' + e)

def reset_audio_level():
    print('A moment of silence, please...')
    with mic as source:
        recog.adjust_for_ambient_noise(source)
        print('Set minimum energy threshold to ' + str(recog.energy_threshold))