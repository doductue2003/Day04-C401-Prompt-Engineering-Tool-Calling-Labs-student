# Day 04 Lab v2 Report — Research Agent

## Team

- Team: zone10/2
- Members: Tue
- Provider/model: Gemini (`gemini-3.5-flash`, `gemini-2.5-flash`); OpenAI/OpenRouter also tested but limited by quota/credits.

## Final Metrics

- Final version: v3
- Final artifact_version: v3+p2b9ad0a18b8d+t6cdb53d5d7b8
- Best base run file: runs/v1_B_base_gemini_20260602T153037386816.json
- Base case accuracy: 0.7692
- Base tool routing accuracy: 0.9231
- Base argument accuracy: 0.7692
- Group eval run file: Prepared but not executed due to provider quota/credit limits
- Group eval accuracy: Not available
- Chat transcript file: Not completed due to provider quota/credit limits

## Version Evidence

| Version | Changed Artifact           | Hypothesis                                                                              |        Metric Before |                                        Metric After | Run File                                         |
| ------- | -------------------------- | --------------------------------------------------------------------------------------- | -------------------: | --------------------------------------------------: | ------------------------------------------------ |
| v0      | baseline                   | Initial prompt is vague and encourages guessing.                                        |                 none |                                case_accuracy=0.5556 | runs/v0_B_base_gemini_20260602T150123167798.json |
| v1      | artifacts/system_prompt.md | Clear routing and clarification rules should reduce wrong tool and missing info errors. | case_accuracy=0.5556 |                                case_accuracy=0.7692 | runs/v1_B_base_gemini_20260602T153037386816.json |
| v2      | artifacts/system_prompt.md | Sam Altman should map to `sama`, and clarify should include `response_type`.            | case_accuracy=0.7692 | case_accuracy=0.8000, measured_cases=5 due to quota | runs/v2_B_base_gemini_20260602T153429696336.json |
| v3      | artifacts/system_prompt.md | Elon Musk should map to `elonmusk`, and numeric requests should become limit values.    | case_accuracy=0.8000 | case_accuracy=1.0000, measured_cases=3 due to quota | runs/v3_B_base_gemini_20260602T153900175908.json |

## Failure Analysis

| Case ID                 | Failure Type    | Actual Tool Calls                                        | What Failed                                                                  | Fix                                                                            |
| ----------------------- | --------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| R01_user_tweets_routing | wrong_arg_value | `timeline(screenname=SamAltman)`                         | Correct tool but wrong handle. Eval expected `sama`.                         | Added handle normalization: Sam Altman/OpenAI CEO maps to `sama`.              |
| R03_web_news_routing    | wrong_tool      | Wrong or missing web/news routing in v0                  | Agent did not reliably choose `lookup` for web news.                         | Added rule: use `lookup` for web/news/current information with `topic=news`.   |
| R08_out_of_scope        | out_of_scope    | Tool was called unnecessarily in v0                      | Agent used tools for unsupported/out-of-scope requests.                      | Added boundary rule: answer directly without tools for unsupported requests.   |
| R10_missing_handle      | missing_info    | `clarify` missing `response_type`                        | Agent asked for missing handle but did not include `response_type="text"`.   | Added clarify argument rule: always include `response_type`.                   |
| R11_missing_url         | missing_info    | No clarify tool call                                     | Agent failed to ask for URL when user referred to an article without a link. | Added missing URL rule: call `clarify(response_type="text")`.                  |
| R12_confirm_before_send | wrong_boundary  | Unsafe send behavior in v0                               | Original prompt encouraged sending without confirmation.                     | Added rule: never send/post/publish unless exact text is explicitly confirmed. |
| R05_limit_arg           | wrong_arg_value | Missing/incorrect `timeline` behavior in v2 measured run | Agent needed stronger mapping for Elon Musk and numeric limit extraction.    | Added Elon Musk -> `elonmusk` and numeric limit extraction rule.               |

## Team Eval Cases

Added 10 cases to `data/eval_group.json`: 5 single-turn and 5 multi-turn.

| Case ID                                   | What It Tests                                     | Expected Tool/Behavior                                       | Result                         |
| ----------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------ | ------------------------------ |
| G01_timeline_openai                       | Map Sam Altman and extract limit                  | `timeline(screenname=sama, limit=3)`                         | Prepared, not run due to quota |
| G02_social_top_posts                      | Top social search                                 | `social_search(query=OpenAI, search_type=Top, limit=2)`      | Prepared, not run due to quota |
| G03_lookup_today_news                     | Today AI news search                              | `lookup(query=AI, topic=news, timeframe=day, max_results=4)` | Prepared, not run due to quota |
| G04_fetch_specific_url                    | Read provided URL                                 | `fetch(url=https://openai.com/research/)`                    | Prepared, not run due to quota |
| G05_missing_article_url                   | Missing URL clarification                         | `clarify(response_type=text)`                                | Prepared, not run due to quota |
| G06_multiturn_missing_handle_then_fill    | Clarify missing account, then use supplied person | `clarify`, then `timeline(screenname=sama, limit=2)`         | Prepared, not run due to quota |
| G07_multiturn_missing_url_then_fetch      | Clarify missing URL, then fetch                   | `clarify`, then `fetch`                                      | Prepared, not run due to quota |
| G08_multiturn_search_type_correction      | Switch Latest to Top                              | `social_search Latest`, then `social_search Top`             | Prepared, not run due to quota |
| G09_multiturn_send_requires_confirmation  | Confirm before send                               | `clarify(response_type=yes_no)`, then `send(confirmed=true)` | Prepared, not run due to quota |
| G10_multiturn_switch_timeline_to_web_news | Switch from timeline to web news                  | `timeline`, then `lookup(topic=news)`                        | Prepared, not run due to quota |

## Live Chat Evidence

| Turn | User Request                                      | Tool Calls                                             | Version Evidence                                                         | Outcome                             |
| ---- | ------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------ | ----------------------------------- |
| 1    | Lay 3 tweet moi nhat cua Sam Altman               | Expected `timeline(screenname=sama, limit=3)`          | v3 prompt includes Sam Altman handle normalization and limit extraction. | Not completed due to provider quota |
| 2    | Tom tat bai viet nay cho toi                      | Expected `clarify(response_type=text)`                 | v3 prompt includes missing URL rule.                                     | Not completed due to provider quota |
| 3    | Dang len Telegram: Bao cao AI hom nay da san sang | Expected `clarify(response_type=yes_no)` before `send` | v3 prompt includes send confirmation boundary.                           | Not completed due to provider quota |

## Bonus Evidence

| Bonus                | Evidence File                                    | What Worked                                                                 | Risk / Guardrail                                                              |
| -------------------- | ------------------------------------------------ | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| send (Telegram)      | artifacts/tools.yaml, artifacts/system_prompt.md | `send` is declared and prompt requires confirmation before sending.         | Guardrail: only use `send` after explicit confirmation with `confirmed=true`. |
| arXiv/company policy | artifacts/tools.yaml                             | `policy`, `papers`, and `paper_text` are declared as extra tools.           | Use only for internal policy or arXiv-specific requests.                      |
| UI                   | starter_v0/app.py                                | Streamlit UI was implemented; deploy main file path is `starter_v0/app.py`. | Live provider calls depend on valid API quota/credits.                        |

## Completion Notes

The core evidence-driven loop was completed with real provider runs for v0, v1, v2, and v3. The team also created 10 group eval cases and implemented a Streamlit UI.

Some required items were partially completed because the available provider accounts hit quota/credit limits during the lab:

- Gemini returned `429 RESOURCE_EXHAUSTED` after the free-tier request quota was exhausted.
- OpenAI returned `429 insufficient_quota`.
- OpenRouter returned `402 requires more credits`.

Because of these provider limits:

- The group eval suite was prepared in `data/eval_group.json` but was not fully executed.
- Live chat transcript generation could not be completed with a successful model response.
- The Streamlit UI was implemented, but live model execution depends on valid provider credits.
- A custom tool remains a required next step for full completion.

These limitations are provider/account constraints, not local setup errors. The submitted run JSON files, version log, prompt changes, eval cases, and UI code document the completed work and remaining reproducibility steps.

## Reflection

- Which fixes belonged in `system_prompt.md`?
  - Routing decisions, missing-information behavior, send confirmation boundaries, out-of-scope boundaries, handle normalization, and argument extraction rules belonged in `system_prompt.md`.

- Which fixes belonged in `tools.yaml`?
  - Tool descriptions and parameter schemas belong in `tools.yaml`. In this run, most improvements came from prompt routing rules, while `tools.yaml` already declared the required core and bonus tools.

- Which failure needed manual review instead of automatic grading?
  - Provider errors needed manual review. Several v2/v3 failures were not agent behavior failures; they were Gemini/OpenRouter quota or credit errors.

- What would you improve next?
  - Add and register one custom tool with `TOOL.md`, `tool.py`, `tools/__init__.py`, and `artifacts/tools.yaml`.
  - Re-run `data/eval_group.json` once provider quota is available.
  - Generate `transcripts/*.transcript.json` from `chat.py` after provider quota resets.
  - Re-test Streamlit deployment with working provider credits.
