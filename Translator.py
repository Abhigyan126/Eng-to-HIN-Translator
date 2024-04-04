from transformers import AutoTokenizer
from transformers import TFAutoModelForSeq2SeqLM, DataCollatorForSeq2Seq

class Translator():
    def __init__(self) -> None:
        pass
    def Translate(self, input_text):
        model_checkpoint = "Helsinki-NLP/opus-mt-en-hi"
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        model = TFAutoModelForSeq2SeqLM.from_pretrained("tf_model")
        tokenized = tokenizer([input_text], return_tensors='np')
        out = model.generate(**tokenized, max_length=128)
        with tokenizer.as_target_tokenizer():
            text = tokenizer.decode(out[0], skip_special_tokens=True)
        return text