# tiny-script

## これは何

便利そうだし書きたいなと思って書いた and 他に適切な置き場所がわからない ものを適当にぶちこんでいます。CC0 License の範疇で適当に使っていただいて構いませんが何か不都合が起こっても責任は取れませんのでご了承ください。

## 内容

そのうち自分でも忘れそうなので書いておく

- `compro/atcoder_problems/fetch_specific_difficulty_problem_lists.py`
  - AtCoder Problems に収録されている、特定の範囲の diff を持つ問題を全取得して json, csv にする
  - 一度実行されたら Problems の API でゲットした中身を json で保存しておく
    - 2 回目以降に無駄に API を叩かないように
  
- `compro/marathon/calculate_scoresum.py`
  - マラソン系問題で得点の合計を簡単に得られるようにするやつ
  - generator, solution, tester コードがあることが前提
  - AtCoder の Introduction to Heuristics Contest 用に作ったので、他のコンテストで利用するなら得点取得パートを若干変える必要がある
    - 得点計算器の出力形式や Usage 等に依存するのでいい感じの一般化が不可能・・・

