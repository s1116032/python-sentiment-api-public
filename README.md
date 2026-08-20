# Sentiment API

![CI](https://github.com/s1116032/python-sentiment-api-public/actions/workflows/ci.yml/badge.svg)

這是一個極簡的文字情緒分類 API。

本專案的重點不在模型準確度，而在開發流程品質：  
透過 FastAPI、pytest、mypy、ruff、black 與 GitHub Actions，練習小型專案也能具備完整的測試、型別檢查與 CI 流程。

---

## 功能

- `POST /predict`：輸入文字，回傳情緒標籤與分數
- 使用 FastAPI async endpoint
- 使用 Pydantic 驗證輸入與輸出
- 使用 mock classifier，測試快速且不依賴外部模型
- 使用 pytest 測試 API、service 與 validation 邏輯
- 使用 black、ruff、mypy 維持程式碼品質
- 使用 GitHub Actions 自動執行檢查

---

## 技術

- Python 3.12
- FastAPI
- Pydantic
- pytest
- pytest-asyncio
- httpx
- pytest-mock
- black
- ruff
- mypy
- Makefile
- GitHub Actions

---

## 快速開始

安裝依賴：

```bash
make install
```

或：

```bash
uv sync --all-extras
```

啟動 API：

```bash
uv run uvicorn app.main:app --reload
```

開啟 Swagger UI：

```text
http://127.0.0.1:8000/docs
```

---

## API

### POST /predict

Request：

```json
{
  "text": "這個功能很棒"
}
```

Response：

```json
{
  "label": "positive",
  "score": 0.7
}
```

### Label

```text
positive
negative
neutral
```

### Score

```text
0.0 <= score <= 1.0
```

### Validation

- `text` 必填
- `text` 必須是 string
- `text` strip 後不可為空
- `text` 長度需為 1 到 500 字

---

## 測試

執行測試：

```bash
make test
```

或：

```bash
uv run pytest
```

測試涵蓋：

- service 層分類邏輯
- schema 驗證邏輯
- async API endpoint
- mock service 呼叫
- 空字串、空白字串、非字串、過長輸入等邊界情況

---

## 程式碼品質

格式化：

```bash
make format
```

執行 lint：

```bash
make lint
```

執行型別檢查：

```bash
make typecheck
```

執行全部檢查：

```bash
make check
```

`make check` 會依序執行：

```text
ruff
black --check
mypy
pytest
```

---

## CI

GitHub Actions 會自動執行：

```text
install dependencies
make lint
make typecheck
make test
```

CI 檔案位於：

```text
.github/workflows/ci.yml
```

PR 需要通過 CI 後才會合併。

---

## Git Flow

| 分支 | 用途 |
|---|---|
| `main` | 可釋出狀態 |
| `develop` | 整合分支 |
| `feature/*` | 功能分支 |

開發流程：

```text
develop -> feature/xxx -> PR to develop -> CI pass -> merge
```

釋出流程：

```text
develop -> main -> tag v0.1.0
```

---

## 專案結構

```text
sentiment-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── services/
│   │   └── sentiment.py
│   └── main.py
├── tests/
├── Makefile
├── pyproject.toml
└── README.md
```

## License
Copyright © 2026 hanwu910514.

詳情請參閱[Apache License 2.0](LICENSE)檔案
