# remote-shoot-dropbox

サンゴの水槽の様子を撮影し、その画像をDropboxに保存するプログラム.

## 使い方

1. [ここのサイトを参考にして](https://laboratory.kazuuu.net/get-a-developer-account-to-use-the-dropbox-api/)Dropboxのクラウドに保存するためのトークンを取得する
2. インターネット接続したラズパイにwebカメラを接続する
3. ラズパイにこのスクリプトたちを保存する
4. Dropboxに`sango/remote_ovseration`, `config`フォルダを作成し、`config`フォルダに`config.json`を保存する
5. ラズパイ上で管理者権限でinterval.pyを実行する(これで[crontab](https://www.server-memo.net/tips/crontab.html)にsango_capture_dropbox.pyが登録される)

## 参考文献

- https://laboratory.kazuuu.net/get-a-developer-account-to-use-the-dropbox-api/
- https://www.server-memo.net/tips/crontab.html
