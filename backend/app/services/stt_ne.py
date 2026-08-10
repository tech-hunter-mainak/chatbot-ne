import warnings

import librosa
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

warnings.filterwarnings("ignore")

MODEL_NAME = "MWirelabs/ne-asr"
AUDIO_FILE = "audio.wav"

# Change this if required
LANGUAGE = "welsh"

torch.set_grad_enabled(False)
torch.set_num_threads(2)

device = torch.device("cpu")

print("Loading processor...")
processor = WhisperProcessor.from_pretrained(MODEL_NAME)

print("Loading model...")
model = WhisperForConditionalGeneration.from_pretrained(
    MODEL_NAME,
    low_cpu_mem_usage=True
)

print("Applying dynamic quantization...")
model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8,
)

model.to(device)
model.eval()

model.generation_config.language = LANGUAGE
model.generation_config.task = "transcribe"

print("Loading audio...")

audio, sr = librosa.load(
    AUDIO_FILE,
    sr=16000,
    mono=True,
)

chunk_seconds = 30
chunk_size = chunk_seconds * sr

result = []

print("Transcribing...")

for start in range(0, len(audio), chunk_size):
    chunk = audio[start:start + chunk_size]

    inputs = processor(
        chunk,
        sampling_rate=16000,
        return_tensors="pt",
    )

    input_features = inputs.input_features.to(device)

    with torch.no_grad():
        predicted_ids = model.generate(
            input_features,
            max_new_tokens=256,
        )

    text = processor.batch_decode(
        predicted_ids,
        skip_special_tokens=True,
    )[0]

    result.append(text)

print("\n===========================")
print("FINAL TRANSCRIPTION")
print("===========================\n")
print(" ".join(result))