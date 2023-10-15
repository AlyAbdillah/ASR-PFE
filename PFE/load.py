from faster_whisper import WhisperModel

model_list = ['tiny','base','small','medium','large-v1','large-v2']
model = WhisperModel(model_list[5], device='cpu', compute_type="int8")