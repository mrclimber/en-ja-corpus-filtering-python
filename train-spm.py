import sys
import sentencepiece as spm


def main():
    lang = sys.argv[1]
    if lang == "en":
        spm.SentencePieceTrainer.Train("--input=train.en --model_prefix=spm32k.en --vocab_size=32000 --character_coverage=1.0")
    elif lang == "ja":
        spm.SentencePieceTrainer.Train("--input=train.ja --model_prefix=spm32k.ja --vocab_size=32000 --character_coverage=0.9995")
    else:
        print("usage: python train-spm.py [en/ja]")


if __name__ == '__main__':
    main()
