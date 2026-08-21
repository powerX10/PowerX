from powerx.v2.adapters import ADAPTERS

def test_zip2_adapters_present():
    for key in ["llamacpp","transformers_text_generation","transformers_text_classification","whisper","kokoro"]:
        assert key in ADAPTERS
