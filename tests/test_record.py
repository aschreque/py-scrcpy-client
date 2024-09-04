import tempfile
from time import sleep
from io import BytesIO

import av
from av import Packet
from pydub import AudioSegment

from scrcpy import Client , Recording_mode  , EVENT_FRAME

packet_queue : list[Packet] = list()
def on_audio_stream(buffer: list[Packet]) :

    for packet in buffer :

        packet.stream = out_stream

        packet_queue.append ( packet )

        # output.mux ( packet )
    print ( f"write buffer {len ( buffer )}" )

    pass

file_path = "stream.flac"
inmemoryfile = BytesIO()
inmemoryfile.name = file_path
output = av.open ( inmemoryfile,  mode = "w"  )
out_stream = output.add_stream ( codec_name = "flac", rate = 48000, options = {'channels' : '1', 'sample-rate': '48000'} )



# Create client
client = Client ( device = "emulator-5554" , recording_mode = Recording_mode.NO_VIDEO )
client.add_listener ( EVENT_FRAME , on_audio_stream )
client.start ( threaded = True )

sleep ( 10 )
client.stop ()
sleep ( 0.5 )


for packet in packet_queue :
        output.mux(packet)

output.close ()

with open("record.flac", "wb") as flac_file:
    flac_file.write(inmemoryfile.getbuffer())



with tempfile.NamedTemporaryFile (suffix=".flac", prefix="audio_record",) as temp :
    temp.write(inmemoryfile.getbuffer())
    audio_file_path = temp.name
    print (audio_file_path)

    print("Detecting voice...")
    seg = AudioSegment.from_file(audio_file_path)
    seg = seg.set_sample_width(2).set_channels(1).set_frame_rate(48000)
    seg = seg.apply_gain ( -seg.max_dBFS )
    print (f"resampling audio file {len(seg)}")
    seg.export("resampled.mp3")