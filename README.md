# 3d-avatar — 実装別カタログ

既存リポジトリは変更・削除せず、確定コミットのソースを追加整理した public ソース分類モノレポです。各実装は独立フォルダです。共通アプリへ統合・API互換化したものではありません。

## どこから見る？

- [ryo-body-scan-walk](implementations/ryo-body-scan-walk/README.md) — 写真テクスチャ付きスキンメッシュ＋手続き歩行。起動は同フォルダの [RUN.md](implementations/ryo-body-scan-walk/RUN.md)。
- [lhm-body-room-walk](implementations/lhm-body-room-walk/README.md) — LHM Gaussian アバターを部屋で表示・歩行。起動は同フォルダの [RUN.md](implementations/lhm-body-room-walk/RUN.md)。
- [video-pose-twin](implementations/video-pose-twin/README.md) — 録画姿勢・カメラ連携のアバター表示。起動は同フォルダの [RUN.md](implementations/video-pose-twin/RUN.md)。
- [ryo-avatar-demo-backup](implementations/ryo-avatar-demo-backup/README.md) — 説明・描画・物体操作の複数アバターデモ集。起動は同フォルダの [RUN.md](implementations/ryo-avatar-demo-backup/RUN.md)。
- [ryo-primer-live](implementations/ryo-primer-live/README.md) — カタログ選択型 Q&A＋計算スケッチ＋音声。起動は同フォルダの [RUN.md](implementations/ryo-primer-live/RUN.md)。
- [avatar-generalized-sketch-v2](implementations/avatar-generalized-sketch-v2/README.md) — 一般化スケッチの改良統合版。起動は同フォルダの [RUN.md](implementations/avatar-generalized-sketch-v2/RUN.md)。
- [avatar-generalized-sketch](historical/avatar-generalized-sketch/README.md) — v1（履歴。v2との比較用）。起動は同フォルダの [RUN.md](historical/avatar-generalized-sketch/RUN.md)。
- [avatar-inflation-demo](implementations/avatar-inflation-demo/README.md) — 閉じた輪郭の inflation をアバターで見せる。起動は同フォルダの [RUN.md](implementations/avatar-inflation-demo/RUN.md)。
- [avatar-source-sketch-bridge](implementations/avatar-source-sketch-bridge/README.md) — 元スケッチとアバターの連携。起動は同フォルダの [RUN.md](implementations/avatar-source-sketch-bridge/RUN.md)。
- [avatar-sketch-rendering-study](implementations/avatar-sketch-rendering-study/README.md) — 描画・表示方法の比較実験。起動は同フォルダの [RUN.md](implementations/avatar-sketch-rendering-study/RUN.md)。

## 実装の区分と限界

基本は desktop WebGL／Web サーバーでのプロトタイプです。Unity/Quest 実機に移植したという意味ではありません。各 README に元の方式、起動コマンド、検証済み範囲があります。モデル推論・3D生成アルゴリズムは [3d-generation](https://github.com/ryosuzuki/3d-generation)、追跡プラットフォームは [image-tracking](https://github.com/ryosuzuki/image-tracking) に分類。アバターと部屋の一体型デモはソース重複を承知で実用単位を保持しています。

このカタログの検証はソース同一性・JS/Python構文・復元情報です。元のデモ動画は元 README のリンクを利用。新しい実機テストやAI呼び出しはしていません。

## 再現性

`source-index.json` と各 `CATEGORY-SNAPSHOT.json` にコミット、Git blob、ソースSHA-256、公開用ソース検証情報を記録。`python3 scripts/verify-snapshots.py` でコピー同一性を検査。素材はご自身で用意してください（ASSETS.md）。

完了状態: main-integrated を目標。所有者: category consolidation worker。権威あるパス: 本リポジトリの全追加ファイル。元リポジトリの作業ツリーは untouched。

## 認証

API 機能は `OPENAI_API_KEY`（OpenAI）または `TYPESAFE_API_KEY`（旧 Jev）を環境変数で設定。元の私用認証経路は公開版から外しています。個人スキャンを公開していません。
