# Backup State Design - 001-simple-login-app

## Mục tiêu

Cơ chế backup state cho workflow MyHarness phải giúp khôi phục đúng vị trí đang làm việc khi context sắp hết, không làm mất tiến độ, và không cần đọc lại toàn bộ lịch sử hội thoại.

## Nguyên tắc

- Lưu ít nhưng đủ để resume chính xác.
- Tách state nhỏ, context canonical và checkpoint lịch sử.
- Mỗi lần backup phải có thể khôi phục được bước đang chạy, artifact gần nhất, và các quyết định quan trọng.
- Không lưu secret, token thật, hoặc nội dung chat dài không cần thiết.

## Các file cần lưu

### 1. `state.yaml`
Dùng cho trạng thái chạy tối thiểu và resume nhanh.

Nên lưu:
- `run_id`
- `feature_id`
- `state` (`RUNNING`, `PAUSED`, `FAILED`, `COMPLETE`)
- `last_completed_step`
- `completed_steps`
- `failed_step`
- `retry_counts` theo step/gate
- `token_summary`
  - `total_input`
  - `total_output`
  - `estimated_cost_usd`
- `last_checkpoint_at`
- `checkpoint_version`

### 2. `run-context.yaml`
Dùng làm context canonical của workflow.

Nên lưu:
- `feature-id`, `module-id`, `module-keyword`, `module-short-name`
- `mode`, `language`
- `tech-stack`
- trạng thái từng step
- đường dẫn artifact gần nhất của từng step
- verdict/retries của các review gate
- các metric quan trọng của từng step

### 3. `checkpoint.md` hoặc `checkpoint.jsonl`
Dùng làm snapshot mốc để backup khi context sắp đầy.

Nên lưu:
- timestamp thực
- step hiện tại
- artifact vừa tạo
- quyết định vừa chốt
- issue còn mở
- next step
- note ngắn cho người/agent kế tiếp

### 4. `pipeline-completion.md` và `token-report.md`
Dùng làm hậu kiểm cuối run.

Nên lưu:
- tổng bước đã chạy
- tổng retry
- tổng assumption
- các gate bị escalate
- health score
- token efficiency

## Khi nào phải lưu backup

### Bắt buộc lưu ngay sau các mốc sau
- Sau khi hoàn tất mỗi step.
- Sau mỗi lần review gate trả `REJECTED` hoặc `APPROVED_WITH_CONDITIONS`.
- Sau khi sửa xong issue và trước khi re-run review.
- Sau khi tạo artifact lớn mới: spec, plan, DD, tasks, testcases, implementation, report.
- Trước khi dispatch bước có rủi ro cao: implement, test, launch.
- Trước khi chuyển sang bước tiếp theo nếu context đã dài hoặc nhiều vòng retry.

### Lưu theo ngưỡng context
- 70% context budget: tạo checkpoint snapshot ngắn.
- 85% context budget: tạo checkpoint đầy đủ hơn, kèm tóm tắt next inputs.
- 95% context budget: ép ghi checkpoint đầy đủ và dừng để resume sau.

## Nội dung tối thiểu của mỗi checkpoint

Mỗi checkpoint nên chứa:
- `checkpoint_id`
- `timestamp`
- `current_step`
- `last_completed_step`
- `artifact_paths`
- `gate_status`
- `open_issues`
- `next_action`
- `resume_hint`

Ví dụ:

```yaml
checkpoint_id: CP-001
timestamp: 2026-06-05T02:35:49Z
current_step: 13
last_completed_step: 12
artifact_paths:
  spec: specs/001-simple-login-app/spec.md
  plan: specs/001-simple-login-app/plan.md
  tasks: specs/001-simple-login-app/tasks.md
  report: docs/output/run-logs/001-simple-login-app/reports/12-testkit-report.md
gate_status: PASS
open_issues: []
next_action: STEP_13_launch
resume_hint: Reload run-context.yaml and continue from step 13
```

## Quy trình backup

### Trước khi backup
1. Đọc `state.yaml` hiện tại.
2. Đọc `run-context.yaml` hiện tại.
3. Ghi tóm tắt step vừa xong vào checkpoint.
4. Cập nhật `last_checkpoint_at`.

### Sau khi backup
1. Đồng bộ lại `state.yaml`.
2. Đồng bộ lại `run-context.yaml`.
3. Ghi log backup vào `00-myharness.log.md`.

## Quy trình resume

Khi resume, agent nên đọc theo thứ tự:
1. `state.yaml` để biết bước cuối cùng.
2. `run-context.yaml` để lấy artifact paths.
3. checkpoint gần nhất để lấy tóm tắt ngữ cảnh.
4. `00-myharness.log.md` để xem retry/gate history.

Resume rule:
- Nếu `state=COMPLETE`, không chạy lại pipeline trừ khi user yêu cầu rerun.
- Nếu `state=FAILED`, bắt đầu từ `last_completed_step + 1` hoặc step được chỉ định.
- Nếu có checkpoint mới hơn state, ưu tiên checkpoint để phục hồi ngữ cảnh ngắn.

## Đề xuất triển khai cho workflow này

- Dùng `state.yaml` làm nguồn sự thật tối thiểu.
- Dùng `run-context.yaml` làm nguồn sự thật cho artifact paths và step results.
- Dùng `checkpoint.md` như bản tóm tắt ngắn mỗi khi gần hết context.
- Gắn checkpoint vào cuối mỗi step và sau mỗi gate retry.
- Khi context sắp đầy, ghi ngay một checkpoint ngắn thay vì đợi tới cuối step.

## Kết luận

Workflow này nên có 3 lớp lưu trạng thái:
- State nhỏ để resume.
- Context đầy đủ để điều phối step.
- Checkpoint ngắn để chống mất ngữ cảnh khi hội thoại dài.

Cách này đủ nhẹ để chạy liên tục, nhưng vẫn an toàn khi cần dừng giữa chừng.
