import streamlit as st
from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_stream
from mne import create_info
from mne.io import RawArray
import numpy as np

st.title("Real-Time EEG Data from Muse")

# Mencari perangkat Muse yang tersedia
muses = list_muses()
if muses:
    st.write("Starting Muse stream...")
    stream(muses[0]['address'])

    # Mencari stream LSL yang dikirim oleh Muse
    streams = resolve_stream('type', 'EEG')

    # Membuat inlet untuk menangkap data EEG
    inlet = StreamInlet(streams[0])

    # Info tentang data EEG (4 channel pada 256 Hz)
    info = create_info(ch_names=['TP9', 'AF7', 'AF8', 'TP10'], sfreq=256, ch_types='eeg')

    st.write("Menangkap data EEG...")
    
    # Membuat container Streamlit untuk menampilkan data
    chart = st.line_chart([], use_container_width=True)
    
    # Streaming loop
    while True:
        # Mendapatkan sample EEG (4 channel data)
        sample, timestamp = inlet.pull_sample()
        
        # Mengonversi data menjadi format yang dapat diolah
        data = np.array(sample).reshape((4, 1))
        
        # Menampilkan data EEG secara real-time
        raw = RawArray(data, info)
        df = raw.to_data_frame()  # Convert to DataFrame for Streamlit
        chart.line_chart(df, use_container_width=True)
else:
    st.write("Tidak ada perangkat Muse yang ditemukan.")
