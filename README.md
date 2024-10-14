# Music Center DB Generator

概要
---
Android向け [Sony Music Center](https://play.google.com/store/apps/details?id=com.sony.songpal&hl=ja) アプリのプレイリストに、MPC-HC/MPC-BEのプレイリスト(.mpcpl形式)を追加する。  
Music Centerのプレイリストは.db形式のファイルで管理されているため、Python sqlite3を使用する。

動作環境
---
- Windows 10 22H2 64bit
- MPC-HC(clsid2版) 2.3.1以降
- Python 3.11.8 64bit
    - 追加モジュール不要
- Xperia Ace III SO-53C(Android 14)

使い方
---
1. PC側の楽曲ファイルを以下の構造で保存する。  
`[任意のフォルダ]\[アーティスト名(フォルダ)]\[アルバム名(フォルダ)]\[曲名(ファイル)]`
1. スマホ側の楽曲ファイルを以下の構造で保存する。  
`PC\SO-53C\SDカード\Music\[アーティスト名(フォルダ)]\[アルバム名(フォルダ)]\[曲名(ファイル)]`
    - ※1 スマホをPCと接続して確認したパス。
    - ※2 microSDに保存する想定のため、内部ストレージは想定していません。
    - ※3 PC側とアーティスト名以降のパスは揃えてください。
1. スマホ側でMusic Centerで任意のプレイリストをひとつ作成する。
1. Music Centerのアプリは念のため終了しておく。
1. 以下のファイルをこのリポジトリをチェックアウトしたフォルダに置く。  
`PC\SO-53C\内部共有ストレージ\MusicCenter\metadata.db`
1. `smc_db_gen.bat` に任意のMPC-HC/MPC-BEのプレイリスト(.mpcpl形式)をD&D。
1. 処理が完了したら`使い方5.`でコピーしてきたファイルをコピー元へ上書き。

使用上の注意
---
- 手元にある環境以外ではテストしていないため、変更したdbファイルが読み込めない等の不具合が発生する可能性があります。
- `metadata.db` を上書きしてもすぐに反映されないため、何度かアプリを再起動してください。
- Music Centerの仕様？で不適切なデータは削除されるようです。

ライセンス
---
MIT Licence
