# TASK

## English

### Add an override input path for the development Docker stack

Background:

- The current development stack can control mock sensors through HTTP.
- `capstone-center` override mode is not exposed through an HTTP endpoint in the development stack.
- Override currently reaches the center as a ZMQ message with `data_type="override_button"`.

Goal:

- Add a small Python entrypoint for local development that lets us toggle center override mode easily.
- The intended user experience is to trigger override from the host with a simple command or `curl`.

Suggested direction:

- Add a lightweight helper service or script dedicated to override input.
- The helper should publish the same message shape that `capstone-center` already expects.
- Keep the implementation development-only for now.

Expected behavior:

- Override ON sends an override message equivalent to `status="override"`.
- Override OFF sends a message equivalent to `status="active"`.
- The development stack should make this easy to call repeatedly during manual testing.

Acceptance criteria:

- A developer can turn override ON and OFF without using the visual harness.
- The change works with the current development Docker stack.
- The approach is documented in the development README.

## 日本語

### development 用 Docker stack から override を入力できる経路を追加する

背景:

- 現在の development stack では、mock sensor は HTTP で操作できる。
- しかし `capstone-center` の override mode には、development stack から直接触るための HTTP エンドポイントがない。
- override は今のところ `data_type="override_button"` の ZMQ メッセージとして center に届く実装になっている。

目的:

- ローカル開発用として、center の override mode を簡単に切り替えられる小さな Python エントリポイントを追加する。
- 利用者視点では、host から簡単なコマンドまたは `curl` で override を操作できる状態にしたい。

進め方の候補:

- override 入力専用の軽量な helper service または script を追加する。
- helper は、`capstone-center` が今すでに受け取れるメッセージ形式をそのまま publish する。
- まずは development 専用の実装として扱う。

期待する挙動:

- Override ON で `status="override"` 相当のメッセージを送る。
- Override OFF で `status="active"` 相当のメッセージを送る。
- development stack 上で手動テスト中に何度でも簡単に呼べる。

完了条件:

- visual harness を使わなくても、開発者が override を ON/OFF できる。
- 変更が現在の development Docker stack で動作する。
- 使い方が development README に追記されている。
