# en-ja-corpus-filtering-python

## 使い方
この説明での訓練データ及びサブワード分割の訓練はJParaCrawlを使っていると想定しています。
### 前準備
1. 以下のコマンドを実行し、訓練データをdataディレクトリ内に置きます。
```bash
$ wget http://www.kecl.ntt.co.jp/icl/lirg/jparacrawl/release/2.0/bitext/en-ja.tar.gz
$ tar xzvf en-ja.tar.gz
$ cut -f3 en-ja/en-ja.bicleaner05.txt > data/train.en
$ cut -f4 en-ja/en-ja.bicleaner05.txt > data/train.ja
```
2. ノイズ削除方法のひとつとしてSentencePieceを利用するので、インストールしていない場合はSentencePieceをインストールし、サブワード分割の訓練を行います。
```bash
$ pip install sentencepiece
$ python data/train-spm.py en
$ python data/train-spm.py ja
```
### 実行
以下のようなコマンドを入力して実行します。
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

### 結果
実行が終了したとき、設定した「file_name」に“-result.[en/ja]”を付けたファイルがコーパスフィルタリングを行ってノイズを削除したデータとして出力されます。

また、「mUSE」「LaBSE」を実行した場合、以下のように類似度とそれに対応した英語文・日本語文が書かれたファイルが、「file_name」に“-[mUSE/LaBSE]-similarity”という名前で出力されます。
```bash
[similarityの出力例]
類似度A
Aの英語文
Aの日本語文
類似度B
Bの英語文
Bの日本語文
…
```
