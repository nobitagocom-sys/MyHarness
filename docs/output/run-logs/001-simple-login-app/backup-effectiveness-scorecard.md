# Backup Effectiveness Scorecard - 001-simple-login-app

## Muc tieu

So sanh hieu qua truoc/sau khi ap dung backup-state theo cung 1 kich ban gian doan.

## Cach dung nhanh

1. Chay 1 lan Baseline (khong dung resume backup).
2. Chay 1 lan With Backup (dung state + run-context + checkpoint).
3. Giu nguyen diem gian doan o ca 2 ben (de cong bang):
   - Sau step 4
   - Sau step 7
   - Sau step 10
4. Dien so vao bang duoi va tinh ket qua.

## Nguon du lieu

- State: [state.yaml](state.yaml)
- Context: [run-context.yaml](run-context.yaml)
- Timeline: [00-myharness.log.md](00-myharness.log.md)
- Token summary: [token-report.md](token-report.md)
- Design backup: [backup-state-design.md](backup-state-design.md)

## So lieu hien co (With Backup - run da hoan tat)

- Tong thoi gian run: 9771 giay (02:42:51)
- Step hoan tat: 0..13 (state = COMPLETE)
- Tong retry gate/step quan sat duoc:
  - step-5: 1
  - step-7: 1
  - step-10: 1
  - step-11: 3
  - Tong retry = 6
- Token summary hien tai: chua co so lieu chuan hoa (dang la 0 trong token-report/state)

## Bang so sanh A/B

| Metric | Baseline (no backup) | With Backup | Delta | Improvement |
|---|---:|---:|---:|---:|
| Total duration (seconds) |  | 9771 | Baseline - WithBackup | (Delta / Baseline) * 100 |
| Resume success rate (%) |  |  | WithBackup - Baseline | + la tot |
| Unexpected rework steps (count) |  |  | Baseline - WithBackup | + la tot |
| Manual interventions (count) |  |  | Baseline - WithBackup | + la tot |
| Total input tokens |  | 0* | Baseline - WithBackup | (Delta / Baseline) * 100 |
| Total output tokens |  | 0* | Baseline - WithBackup | (Delta / Baseline) * 100 |
| Estimated cost (USD) |  | 0.0* | Baseline - WithBackup | (Delta / Baseline) * 100 |

Ghi chu (*): so token/cost hien tai cua run with backup dang 0 do thieu telemetry dong nhat. Neu ban bo sung telemetry, cap nhat lai 3 dong token/cost de co ket qua chinh xac.

## Cong thuc ket luan

- Time saving % = ((BaselineTime - BackupTime) / BaselineTime) * 100
- Token saving % = ((BaselineToken - BackupToken) / BaselineToken) * 100
- Cost saving % = ((BaselineCost - BackupCost) / BaselineCost) * 100

## Nguong danh gia de pass

- Resume success rate >= 90%
- Time saving >= 20%
- Unexpected rework <= 1 step moi lan gian doan
- Khong mismatch giua state va run-context

## Ket qua

- Status: PENDING
- Ket luan tam thoi: Can 1 lan chay Baseline de dien cot no backup, sau do tinh ra % tiet kiem thoi gian/token/cost.
