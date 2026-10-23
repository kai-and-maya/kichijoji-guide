# kichijoji-guide

Kai & Mayaの案内サービスのWebページです。GitHub Pagesで公開しています。

- 英語トップ：https://kai-and-maya.github.io/kichijoji-guide/
- 日本語トップ：https://kai-and-maya.github.io/kichijoji-guide/ja/
- 英語ガイド：https://kai-and-maya.github.io/kichijoji-guide/guide/
- 日本語ガイド：https://kai-and-maya.github.io/kichijoji-guide/ja/guide/

## 運用の決まり

- 内容の正はこのWeb版です。紙の資料（フライヤー、地図、小冊子）は、内容が確定してからまとめて反映します。
- 紙とWebで意図して変えている所は、別の引き継ぎ資料に書いておきます。紙に反映するときは、そのメモで差分を確かめます。
- 店名や店の写真は、店の了承を取ってから載せます。
- 写真の枠は、URLの末尾に `?draft` を付けたときだけ表示します。公開ページに偽物の写真や感想は入れません。

## 更新のしかた

1. 文は `tools/build.py` の中にまとめてあります。英語と日本語が並んでいるので、両方を直します。
2. リポジトリの直下で `python3 tools/build.py .` を実行すると、4つのページが作り直されます。
3. 送る前に、スマホの幅で表示を確かめます。日本語の文はtextlintで確認します。
4. 送ると、数分でそのまま公開されます。送る前に必ず内容を確認します。

HTMLのファイルを直接書き換えると、次にスクリプトを実行したときに消えます。直すのはスクリプトの側です。
