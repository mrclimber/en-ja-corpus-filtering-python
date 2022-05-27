# corpus-filtering-python

## 使い方
この説明での訓練データ及びサブワード分割の訓練はJParaCrawlを使っていると想定しています。
### 前準備
1. 以下のコマンドを実行し、訓練データをdataディレクトリ内に置く。
```bash
$ wget http://www.kecl.ntt.co.jp/icl/lirg/jparacrawl/release/2.0/bitext/en-ja.tar.gz
$ tar xzvf en-ja.tar.gz
$ cut -f3 en-ja/en-ja.bicleaner05.txt > data/train.en
$ cut -f4 en-ja/en-ja.bicleaner05.txt > data/train.ja
```
2. ノイズ削除方法のひとつとしてSentencePieceを利用するので、インストールしていない場合はSentencePieceをインストールし、サブワード分割の訓練を行う。
```bash
$ pip install sentencepiece
$ python data/train-spm.py en
$ python data/train-spm.py ja
```
### 実行
以下のようなコマンドを入力して実行する。
```bash
$ python corpus-filtering.py string_length subword
```
ノイズ削除方法は複数選択が可能で、以下の表にノイズの削除方法とそれに対応したコマンドライン引数の入力を示す。
|  ノイズの削除方法  |  コマンドライン引数  |
| ---- | ---- |
|  文字数で判断  |  string_length  |
|  単語数で判断  |  subword  |
|  文字種の割合で判断  |  character_type  |
|  言語判定ツールで判断  |  langdetect  |
|  多言語文符号化器（mUSE）で判断  |  mUSE  |
|  多言語文符号化器（LaBSE）で判断  |  LaBSE  |

表の上の3つの手法は実行時間が下の3つに比べて比較的に短いので、複数の手法で実行する場合は先に選択することで全体の実行時間を減らすことができます。
