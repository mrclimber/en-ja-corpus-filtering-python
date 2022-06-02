import sys
import os
import glob
import numpy as np
import sentencepiece as spm
import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf
from langdetect import detect
import re


def del_string_length(f_in_en, f_in_ja, f_out_en, f_out_ja):

    cnt = 0
    for en_text, ja_text in zip(f_in_en, f_in_ja):
        en_text_strlen = en_text.replace(' ', '')
        ja_text_strlen = ja_text.replace(' ', '')
        if (30 <= len(en_text_strlen) <= 200) and (15 <= len(ja_text_strlen) <= 100):
            f_out_en.write(en_text)
            f_out_ja.write(ja_text)
            cnt += 1
    
    return cnt


def del_subword(f_in_en, f_in_ja, f_out_en, f_out_ja):

    model_en = spm.SentencePieceProcessor(model_file = "/home/honda/data/spm32k.en.model")
    model_ja = spm.SentencePieceProcessor(model_file = "/home/honda/data/spm32k.ja.model")

    cnt = 0
    for en_text, ja_text in zip(f_in_en, f_in_ja):
        en_sen = " ".join(model_en.encode(en_text.strip(), out_type=str))
        ja_sen = " ".join(model_ja.encode(ja_text.strip(), out_type=str))
        n_en = en_sen.count(' ') + 1
        n_ja = ja_sen.count(' ') + 1
        if (10 <= n_en < 55) or (10 <= n_ja < 55):
            f_out_en.write(en_text)
            f_out_ja.write(ja_text)
            cnt += 1

    return cnt


def del_character_type(f_in_en, f_in_ja, f_out_en, f_out_ja):

    p_en = re.compile('[a-zA-Z]+')
    p_ja = re.compile('[\u3041-\u309F]+|[\u30A1-\u30FF]+|[\u4E00-\u9FD0]+')

    cnt = 0
    for en_text, ja_text in zip(f_in_en, f_in_ja):
        en_text_type = en_text.replace(' ', '').replace(',', '').replace('.', '')
        ja_text_type = ja_text.replace(' ', '').replace('、', '').replace('。', '')
        en_result = ''.join(p_en.findall(en_text_type))
        ja_result = ''.join(p_ja.findall(ja_text_type))
        ratio_en = int(len(en_result) / len(en_text_type) * 100)
        ratio_ja = int(len(ja_result) / len(ja_text_type) * 100)
        if (ratio_en >= 90) and (ratio_ja >= 80):
            f_out_en.write(en_text)
            f_out_ja.write(ja_text)
            cnt += 1

    return cnt


def del_langdetect(f_in_en, f_in_ja, f_out_en, f_out_ja):

    cnt = 0
    for en_text, ja_text in zip(f_in_en, f_in_ja):
        if (detect(en_text) == 'en') and (detect(ja_text) == 'ja'):
            f_out_en.write(en_text)
            f_out_ja.write(ja_text)
            cnt += 1

    return cnt


def del_mUSE(f_in_en, f_in_ja, f_out_en, f_out_ja, f_out_mUSE_sim):
    
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")
    
    cnt = 0
    for en_text, ja_text in zip(f_in_en, f_in_ja):
        en_vec = embed(en_text)
        ja_vec = embed(ja_text)
        similarity = np.inner(en_vec, ja_vec)

        if 0.4 <= similarity < 0.7:
            f_out_en.write(en_text)
            f_out_ja.write(ja_text)
            f_out_mUSE_sim.write(str(similarity[0][0]) + "\n")
            f_out_mUSE_sim.write(en_text)
            f_out_mUSE_sim.write(ja_text)
            f_out_mUSE_sim.write(s)
            cnt += 1

    return cnt

def del_LaBSE(f_in_en, f_in_ja, f_out_en, f_out_ja, f_out_LaBSE_sim):

    def normalization(embeds):
        norms = np.linalg.norm(embeds, 2, axis=1, keepdims=True)
        return embeds/norms

    preprocessor = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder-cmlm/multilingual-preprocess/2")
    encoder = hub.KerasLayer("https://tfhub.dev/google/LaBSE/2")
    
    cnt = 0
    for en_text, ja_text in zip(f_in_en, f_in_ja):
        en_sen = tf.constant([en_text])
        ja_sen = tf.constant([ja_text])

        en_embeds = encoder(preprocessor(en_sen))["default"]
        ja_embeds = encoder(preprocessor(ja_sen))["default"]
        en_embeds = normalization(en_embeds)
        ja_embeds = normalization(ja_embeds)

        similarity = np.matmul(en_embeds, np.transpose(ja_embeds))
        
        if 0.7 <= similarity < 0.9:
            f_out_en.write(en_text)
            f_out_ja.write(ja_text)
            f_out_LaBSE_sim.write(str(similarity[0][0]) + "\n")
            f_out_LaBSE_sim.write(en_text)
            f_out_LaBSE_sim.write(ja_text)
            cnt += 1

    return cnt


def main():

    args = sys.argv
    for s in args[1:]:
        if s != "string_length" and s != "subword" and s != "character_type" and s != "langdetect" and s != "mUSE" and s!= "LaBSE":
            print("正しい手法番号が選択されていません")
            sys.exit()

    file_name = "/home/honda/test/data/train"
    
    for i, s in enumerate(args[1:]):
        if i == 0:
            f_in_en = open(file_name + ".en")
            f_in_ja = open(file_name + ".ja")
        else:
            f_in_en = open(file_name + "-result" + str(i) + ".en")
            f_in_ja = open(file_name + "-result" + str(i) + ".ja")
        
        f_out_en = open(file_name + "-result" + str(i+1) + ".en", 'w')
        f_out_ja = open(file_name + "-result" + str(i+1) + ".ja", 'w')

        if s == "string_length":
            cnt = del_string_length(f_in_en, f_in_ja, f_out_en, f_out_ja)
            print("string_length 実行後の文対量：" + str(cnt))
        elif s == "subword":
            cnt = del_subword(f_in_en, f_in_ja, f_out_en, f_out_ja)
            print("subword 実行後の文対量：" + str(cnt))
        elif s == "character_type":
            cnt = del_character_type(f_in_en, f_in_ja, f_out_en, f_out_ja)
            print("character_type 実行後の文対量：" + str(cnt))
        elif s == "langdetect":
            cnt = del_langdetect(f_in_en, f_in_ja, f_out_en, f_out_ja)
            print("langdetect 実行後の文対量：" + str(cnt))
        elif s == "mUSE":
            f_out_mUSE_sim= open(file_name + "-mUSE-similarity", 'w')
            cnt = del_mUSE(f_in_en, f_in_ja, f_out_en, f_out_ja, f_out_mUSE_sim)
            f_out_mUSE_sim.close()
            print("mUSE 実行後の文対量：" + str(cnt))
        elif s == "LaBSE":
            f_out_LaBSE_sim = open(file_name + "-LaBSE-similarity", 'w')
            cnt = del_LaBSE(f_in_en, f_in_ja, f_out_en, f_out_ja, f_out_LaBSE_sim)
            f_out_LaBSE_sim.close()
            print("LaBSE 実行後の文対量：" + str(cnt))
        
        f_in_en.close()
        f_in_ja.close()
        f_out_en.close()
        f_out_ja.close()

    os.rename(file_name + "-result" + str(len(args)-1) + ".en", file_name + "-result.en")
    os.rename(file_name + "-result" + str(len(args)-1) + ".ja", file_name + "-result.ja")
    for file_name in  glob.glob(file_name + "-result????"):
        os.remove(file_name)
     

if __name__ == '__main__':
    main()