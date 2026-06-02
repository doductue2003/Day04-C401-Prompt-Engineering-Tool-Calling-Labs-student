# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật.

## Team

- Team: Zone10-team2
- Members: 
    Nguyễn Thái Dương - 2A202600547
    Trần Quang Thanh - 2A202600620 
    Đõ Đức Tuệ - 2A202600900
- Provider/model: Gemini (gemini-3.5-flash, gemini-2.5-flash); OpenAI/OpenRouter also tested but limited by quota/credits.

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent: tìm tin theo từ khóa hoặc theo tài khoản, đọc URL, tổng hợp thành markdown digest, và (tùy xác nhận) gửi bản tin lên Telegram. Hỗ trợ tìm paper arXiv và tìm trong tài liệu nội bộ.

**Link dùng thử (deploy):**

> Chạy `streamlit run app.py` để mở UI local. (Nếu đã deploy, dán URL ở đây.)

## A2. Tool agent có

Các tool đang được đăng ký và sử dụng trong agent:

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Gửi câu hỏi/mở vòng hỏi bổ sung khi thiếu thông tin | không |
| timeline | Lấy bài đăng gần đây của 1 tài khoản (screenname) | không |
| social_search | Tìm bài đăng trên mạng xã hội theo từ khóa (Latest/Top) | không |
| lookup | Tra cứu web / tin tức theo query + timeframe | không |
| fetch | Lấy nội dung từ một URL | không |
| format | Biên tập các item thành markdown digest | không |
| send | Gửi text tới Telegram (chỉ khi `confirmed=true`) | không (bonus) |
| policy | Tìm trong tài liệu nội bộ (company_policy) | không (bonus) |
| papers | Tìm bài trên arXiv | không (bonus) |
| paper_text | Tải và trích text từ arXiv PDF | không (bonus) |
| crypto_price | Lấy giá hiện tại của crypto | không |
| echo | Trả lại nguyên văn `text` (test tool, side-effect free) | có |

## A3. Câu hỏi mẫu để thử

1. "Gửi message kiểm tra qua Telegram bot: 'Đây là tin nhắn thử nghiệm từ UI chat.' Tôi xác nhận gửi."
2. "Echo this: 'hello team'" (kiểm tra routing đến `echo`)
3. "Tìm bài báo về 'evaluation of research agents' và show 1 title" (kiểm tra `papers`)
4. "Tóm tắt trang https://openai.com/blog" (kiểm tra `fetch` + `format`)

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Baseline run | 0.00 | 0.70 | runs\v0_B_base_openrouter_20260602T142806360184.json |
| v1 | system_prompt.md + tools.yaml | AI guesses args and sends without confirmation | 0.70 | 0.90 | runs\v1_B_base_openrouter_20260602T150548285161.json |
| v2 | system_prompt.md | AI fails to ask yes_no for send and ignores cancellation in multi-turn | 0.90 | 0.95 | runs\v2_B_base_openrouter_20260602T154433866753.json |
| v3 | system_prompt.md | M06 failed in v2 due to weak negation rule; stronger negation rule applied (trade-off) | 0.95 | 0.90 | runs\v3_B_base_openrouter_20260602T160426889590.json |

Notes: Use the run JSON files to extract `prompt_hash`, `tools_hash`, and the detailed per-case failures for each run.

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| (populate from runs) | (see run JSON) | (actual tool_calls) | (observed_mismatch / failures) | (edit `system_prompt.md` or `artifacts/tools.yaml`) |

Action: open the run JSON (e.g., `runs/v1_...json`) and for each failed case copy `results[*].result.failures` and `results[*].result.observed_mismatch` here, then add the fix applied in the next version.

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn). All cases were added; expected behaviors are below and results are pending until group eval is run.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01 | Send to Telegram with explicit confirmation | `send` with `text` and `confirmed=true` | pending (created)
| G02 | arXiv search routing | `papers` with query & max_results=1 | pending
| G03 | Multi-turn: follow-up then lookup | `lookup` with topic=news, timeframe=day | pending
| G04 | Routing to echo test tool | `echo` with text | pending
| G05 | social_search routing and args | `social_search` Latest OpenAI | pending
| G06 | Fetch URL then format | `fetch` for URL then `format` | pending
| G07 | Internal policy search | `policy` with policy_area=source_citation | pending
| G08 | Crypto price routing | `crypto_price` coin_id=bitcoin | pending
| G09 | Multi-turn cancel send (negation) | no tool call after user cancels | pending
| G10 | Lookup timeframe enforcement | `lookup` with timeframe=month | pending

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "Gửi tin nhắn kiểm tra: 'Hello from UI'" | `send` -> `send_telegram` (sent) | sample transcript | sent (see `transcripts/sample.transcript.json`)
| 2 | "Echo: 'abc123'" | `echo` -> echoed 'abc123' | sample transcript | echoed (see `transcripts/sample.transcript.json`)

If you run live with `python chat.py --provider openrouter --version v3` more transcripts will be generated under `transcripts/`.

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | transcripts/sample.transcript.json | `send` performed and Telegram API returned `sent` in sample transcript | Requires `confirmed=true`; ensure tokens not leaked
| echo (test tool) | data/eval_group.json + tools/echo | Echo tool returned expected value for test cases | Side-effect free — safe for eval
| UI (Streamlit) | local run | Streamlit UI routes to `run_model_tool_loop` and shows tool logs/expanders | Deploy only with safe keys and rate limits

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?

	- Routing guidance, explicit examples of correct arg shapes (e.g., timeframe values), confirmation and negation handling, and explicit prohibition of side-effectful actions without `confirmed=true`.

- Which fixes belonged in `tools.yaml`?

	- Make parameter schemas stricter (required fields, enums for timeframe), improve tool descriptions to teach routing, and include example args to guide the model.

- Which failure needed manual review instead of automatic grading?

	- Any `send` that posts to an external channel must be manually reviewed for safety/intent. Also ambiguous user intents and negation cases should be manually inspected.

- What would you improve next?

	- Automate smoke tests using `echo` for routing checks, expand `data/eval_group.json` with adversarial examples (negation, partial URLs), and add CI steps to run `scripts/preflight_provider.py` and a minimal eval on push.

