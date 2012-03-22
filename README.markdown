README
======
ステータス: とりあえず動いた

注意
----
* **ブラウザのクッキー情報を無理矢理触るので、間違ってブラウザがおかしくなっても知りません**
* **Dropboxを使った共有を使用する場合は、データを保存しているDropboxフォルダをくれぐれも公開しないように。もしプレミアムアカウントとかだったら大変なことになるかも知れません。**

I'm sorry, but this application (and documentation) will support only Japanese.

概要
----
ニコニコ動画のログインは一つのブラウザからからのみという仕様に対抗すべく開発された超特殊対ニコニコ決戦(以下略です

機能
----
マルチOS、マルチブラウザを対象にいろんな方法でセッションを共有します。

### サポートする(つもりの)OS
* Windows
* Mac OSX

### サポートする(つもりの)ブラウザ
* Chrome
* Firefox
* (余裕があれば)Internet Explorer

### サポートする(つもりの)共有方法
* Dropbox経由

#### 一瞬思いついた共有方法(実装予定無し)

* Google Docs経由
* 自鯖

必要なもの(準備)
---------
Python 3.x

### Windowsユーザーの方へ
PythonはWindowsにデフォルトでは入っていません。

[64bit](http://www.python.org/ftp/python/3.2.2/python-3.2.2.amd64.msi)
[32bit](http://www.python.org/ftp/python/3.2.2/python-3.2.2.msi)
この辺からどうぞ。*.py拡張子のファイルのアイコンが変わってれば大丈夫です。

### Mac OS Xユーザーの方へ
MacはデフォルトでPython 2.xは入ってるんですけど、3.x系がねぇ・・・

[インストーラ](http://www.python.org/ftp/python/3.2.2/python-3.2.2-macosx10.6.dmg)を使って入れるか、[MacPorts](http://www.macports.org/)や[Homebrew](http://mxcl.github.com/homebrew/)等のお好きなパッケージマネージャで入れて`python3`でインタプリタが起動できるようにしておいてください。
使い方
-----
### Windows
`bin`フォルダの中にある`Dokonico.py`ファイルをダブルクリックすれば、ちっちゃい画面が出てきますので、Showで現在見えているセッション情報を表示、Syncで実際に同期を実行します。

### Mac OS X
`bin/dokonico`をTerminalから実行してください。
その際、サブコマンドshowまたはsyncを指定してください。
別に`bin/Dokonico.py`を実行してもWindowsの場合同様GUIも出るはずです。

設定
---
`etc/config.json`ファイルを編集してください。JSONファイルになっています。
**今のところ有効なのは、/dropbox/dirオプションぐらいで、これは共有に使用するDropboxフォルダを指定できます。ただし、'~'文字は自分のホームディレクトリに展開されます**



その他
-----
* テストにnosetestsを使っています