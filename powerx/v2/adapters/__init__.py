from .llamacpp import LlamaCppAdapter
from .transformers_text import TransformersTextAdapter
from .text_classification import TextClassificationAdapter
from .whisper import WhisperAdapter
from .kokoro import KokoroAdapter

ADAPTERS = {
    "llamacpp": LlamaCppAdapter,
    "transformers_text_generation": TransformersTextAdapter,
    "transformers_text_classification": TextClassificationAdapter,
    "whisper": WhisperAdapter,
    "kokoro": KokoroAdapter,
}
