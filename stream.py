from elevenlabs import generate, stream

audio_stream = generate(
    text="Tune in... I'm sad for a real-time streaming voice!",
    stream=True
)

stream(audio_stream)