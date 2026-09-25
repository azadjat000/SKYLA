# Voice

The voice subsystem is an adapter boundary, not a dashboard prerequisite. Configure `SKYLA_AUDIO_DEVICE` and retain the native Airdopes rate with `SKYLA_SAMPLE_RATE=8000`; resampling belongs after capture. A production adapter should use PipeWire capture, 30 ms VAD frames, configurable pre-roll/silence/max utterance, then faster-whisper. Wake-word detection must remain optional so continuous test mode works without it.
