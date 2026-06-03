# REQUIREMENT DEFINITION DOCUMENT

## AI BtoB 商流型 受発注システム

---

## 0. Max Score Evaluation Focus

Ban giám khảo nhiều khả năng muốn thấy hệ thống **không chỉ là màn hình đặt hàng**, mà là một flow BtoB đúng nghiệp vụ.

| Điểm kỳ vọng | Nội dung cần thể hiện để ăn điểm cao |
|---|---|
| 商流ID là trung tâm | Trước khi chọn sản phẩm, hệ thống phải xác định được `注文元 → 納入先 → 商流ID`. Giá, sản phẩm, MOQ, lead time đều phụ thuộc vào 商流. |
| Nghiệp vụ BtoB rõ ràng | Không làm giống EC B2C. Phải có khách hàng, 納入先, 契約単価, 売掛注文, 基幹連携. |
| AI có vai trò thực tế | AI hỗ trợ tìm 納入先, tìm sản phẩm, giải thích lỗi validation, mapping CSV, đề xuất reorder/template, phát hiện bất thường. |
| Demo end-to-end | Login → chọn 納入先/商流 → nhập header → search sản phẩm → nhập số lượng → validation → xác nhận → tạo 受注番号 → mock D365 連携. |
| Master data rõ | Có 担当者, 顧客, 納入先, 商流, 商品, 契約単価, MOQ/SPQ, 配送カレンダー, 注文. |
| Validation mạnh | Không cho đặt sản phẩm không có 販売条件, sai MOQ/SPQ, 納期 không hợp 配送ルート, giá hết hiệu lực. |
| UI có thể demo | Có dashboard, search, cart/order input, confirm, history, CSV import/export, admin master. |
| Tích hợp D365 | Có trạng thái 連携, retry, error log, payload preview hoặc mock API. |
| Audit & security | Role-based access, 操作ログ, CSV export log, user permission theo khách hàng/拠点. |

---

## 1. System Overview

### 1.1 Purpose

本システムは、BtoB取引における「商流ID」を基準に、発注担当者が正しい納入先・契約条件・商品・単価を選択し、売掛注文を作成して基幹システム D365 に即時連携するための受発注支援システムである。

システムの目的は以下である。

- 発注前に必ず `注文元 → 納入先` の商流を確定する
- 商流に基づき、取扱可能商品・契約単価・MOQ/SPQ・配送条件を自動適用する
- 入力ミス、価格ミス、納期ミスをリアルタイムで防止する
- CSV一括登録、注文テンプレート、再注文により発注業務を効率化する
- 確定済み注文を D365 へ即時連携し、連携状態を追跡可能にする
- AIにより、商品検索、CSV取込補助、エラー説明、注文提案を支援する

### 1.2 Scope

The system supports:

- User login and customer/delivery-destination permission control
- Delivery destination search and 商流ID identification
- Contract-based product filtering and price application
- Order header input, delivery date control, and line-item input
- MOQ/SPQ, package type, lead time, delivery route validation
- Order confirmation, order number generation, and D365 integration
- CSV bulk upload and CSV/Excel download
- Order history, reorder, draft order, favorite items, and order templates
- Multi-location ordering
- Role-based access control and operation logs
- AI assistant for search, validation explanation, CSV mapping, reorder suggestion, and business-rule guidance

### 1.3 Glossary

| Term | Description |
|---|---|
| 商流ID | BtoB取引における注文元・納入先・契約条件を一意に特定するID |
| 注文元 | 発注を行う会社、または取引先企業 |
| 納入先 | 商品を納品する店舗・倉庫・工場など |
| 担当者 | 実際に注文操作を行うユーザー |
| 契約単価 | 商流・商品・有効期間に基づき適用される販売価格 |
| 取扱可能商品 | 特定の商流で注文可能な商品 |
| MOQ | Minimum Order Quantity。最小発注数量 |
| SPQ | Standard Packing Quantity。標準発注単位・梱包単位 |
| 荷姿 | ケース、バラ、重量などの入力単位 |
| 希望納期 | 発注者が希望する納品日 |
| リードタイム | 受注から納品までに必要な日数 |
| 配送ルート | 納入先に対して利用可能な配送経路 |
| 売掛注文 | 後払い・掛取引を前提としたBtoB受注 |
| D365 | Microsoft Dynamics 365。基幹システム |
| CSV一括登録 | 複数の注文明細をCSVでまとめて登録する機能 |
| 操作ログ | ユーザー操作、注文確定、CSV出力などの監査記録 |

---

## 2. Stakeholders

| Role | Description |
|---|---|
| 発注担当者 | 納入先を選択し、商品・数量・希望納期を入力して注文を作成する |
| 代理入力者 | 複数顧客・複数拠点の注文を代理で入力する |
| 承認者 | 必要に応じて注文内容を確認・承認する |
| 営業担当者 | 顧客・契約単価・取扱商品の確認、注文履歴の参照を行う |
| マスタ管理者 | 顧客、納入先、商流、商品、単価、MOQ/SPQ、配送条件を管理する |
| 物流担当者 | 納期、配送ルート、欠品・遅延情報を確認する |
| 経理・受注管理担当者 | 売掛注文、受注番号、D365連携状態を確認する |
| システム管理者 | ユーザー権限、操作ログ、連携エラー、CSV出力履歴を管理する |
| AI Assistant | 商品検索、CSV取込補助、エラー理由説明、再注文提案を行う補助機能 |

---

## 3. Business Overview

### 3.1 Business Flow

1. 発注担当者がログインする
2. ログインIDに紐づく注文元・納入先権限をロードする
3. 納入先を検索・選択する
4. `注文元 → 納入先` により商流IDを確定する
5. 商流IDに基づき、契約単価・取扱商品・配送条件をロードする
6. 注文日、希望納期などのヘッダ情報を入力する
7. 商品名、JAN、商品コードから商品を検索する
8. ケース数、バラ数、重量などで数量を入力する
9. MOQ/SPQ、販売条件、納期、配送ルートをリアルタイムチェックする
10. 注文内容を確認する
11. 受注番号を発番し、注文を確定する
12. D365へ即時連携する
13. 連携成功・失敗状態を記録する
14. 必要に応じて確認メール、注文履歴、CSV/Excel出力を行う

### 3.2 AI Usage Flow

1. ユーザーが自然言語で納入先・商品を検索する  
   例: 「東京倉庫に納品できる牛乳を探して」
2. AIが商流、商品マスタ、契約単価を参照して候補を提示する
3. CSVアップロード時、AIが列名を推測し、商品コード/JAN/数量列をマッピングする
4. Validation error発生時、AIが業務的な理由を説明する  
   例: 「この商品は選択中の商流では販売条件が未設定です」
5. 注文履歴からAIが定型注文・再注文候補を提案する

---

## 4. Use Case Definition

### UC-01: Login and Load Customer Permission

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User logs in and the system loads permitted customers and delivery destinations |
| Pre-condition | User account exists and is active |
| Post-condition | Available 注文元 and 納入先 list is loaded |

**Main Flow:**

1. User enters login credentials
2. System authenticates the user
3. System loads customer and delivery-destination permissions
4. System displays dashboard with available order companies

**Exception Flow:**

- Invalid login → system displays authentication error
- No customer permission → system blocks ordering and shows contact-admin message
- Suspended user → system blocks access

---

### UC-02: Select Delivery Destination and Identify 商流

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User searches delivery destination and system identifies 商流ID |
| Pre-condition | User is logged in and has customer permission |
| Post-condition | 商流ID is fixed and related master data is loaded |

**Main Flow:**

1. User searches by 納入先名 or 納入先CD
2. System displays available delivery destinations
3. User selects delivery destination
4. System identifies 商流ID from 注文元 and 納入先
5. System loads contract price, available products, MOQ/SPQ, delivery route, and calendar

**Exception Flow:**

- No valid 商流 → system blocks order creation
- Multiple 商流 candidates → system asks user to select applicable condition
- Expired contract → system displays warning and blocks ordering

---

### UC-03: Input Order Header

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User inputs common order conditions |
| Pre-condition | 商流ID is fixed |
| Post-condition | Order header is temporarily saved |

**Main Flow:**

1. System sets 注文日 as system date
2. User selects 希望納期 from calendar
3. System checks lead time and delivery calendar
4. User proceeds to product input

**Exception Flow:**

- 希望納期 is earlier than allowed lead time → system displays selectable earliest date
- Delivery unavailable date → system suggests next available delivery date

---

### UC-04: Search and Add Product

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User searches products available for the selected 商流 |
| Pre-condition | 商流ID and header are fixed |
| Post-condition | Product line is added to order detail |

**Main Flow:**

1. User searches by 商品名, JAN, or 商品コード
2. System filters products by 商流ID
3. System displays contract price valid on 注文日
4. User selects product
5. System adds product to order detail

**Exception Flow:**

- Product not available for selected 商流 → system hides or marks unavailable product
- Contract price not found → system blocks adding product
- Price expired → system displays validity-period error

---

### UC-05: Input Quantity and Validate

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User inputs quantity by package unit |
| Pre-condition | Product line exists |
| Post-condition | Quantity and calculated amount are valid |

**Main Flow:**

1. User selects input unit: ケース数, バラ数, or 重量
2. User inputs quantity
3. System converts quantity based on package master
4. System checks MOQ/SPQ
5. System calculates line amount
6. System displays validation status

**Exception Flow:**

- Quantity below MOQ → system displays minimum quantity
- Quantity not aligned with SPQ → system suggests nearest valid quantity
- Invalid weight unit → system displays unit conversion error

---

### UC-06: Confirm Order and Send to D365

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User confirms order and system creates order number |
| Pre-condition | All validation checks are successful |
| Post-condition | Order is confirmed and integration to D365 is executed |

**Main Flow:**

1. User opens confirmation screen
2. System displays header, detail, price, delivery condition, total amount
3. User confirms order
4. System generates 受注番号
5. System sends order data to D365
6. System records integration result
7. System displays completion screen

**Exception Flow:**

- Validation error remains → system blocks confirmation
- D365 integration failed → order status becomes `連携エラー`
- Duplicate submission → system prevents duplicate order by idempotency key

---

### UC-07: CSV Bulk Order Upload

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User uploads CSV to register multiple order lines |
| Pre-condition | 商流ID is fixed |
| Post-condition | Valid CSV rows are loaded into order detail |

**Main Flow:**

1. User downloads CSV template
2. User fills product code/JAN and quantity
3. User uploads CSV
4. System validates column format
5. AI suggests column mapping if headers are unclear
6. System validates products, prices, MOQ/SPQ, and delivery rules
7. Valid rows are added to order

**Exception Flow:**

- Unknown product code → system marks row error
- Missing quantity → system marks row error
- Mixed invalid rows → system allows error CSV download

---

### UC-08: Reorder from Order History

| Item | Content |
|---|---|
| Actor | 発注担当者 |
| Description | User copies a previous order to create a new order |
| Pre-condition | User has access to past order |
| Post-condition | New draft order is created |

**Main Flow:**

1. User opens order history
2. User selects previous order
3. User clicks reorder
4. System copies lines to new draft
5. System recalculates price using current order date
6. System validates current 商流 conditions

**Exception Flow:**

- Product no longer available → system marks unavailable line
- Price changed → system shows updated price notice
- Delivery condition changed → system requests new delivery date

---

## 5. Functional Requirements

| ID | Name | Description |
|---|---|---|
| FR-01 | User Authentication | System shall authenticate users by login ID/password or SSO |
| FR-02 | Customer Permission Control | System shall restrict 注文元 and 納入先 based on logged-in user |
| FR-03 | Delivery Destination Search | System shall search 納入先 by name and code |
| FR-04 | 商流 Identification | System shall identify 商流ID from 注文元 and 納入先 |
| FR-05 | Master Data Load | System shall load contract price, product, MOQ/SPQ, delivery route, calendar based on 商流ID |
| FR-06 | Header Input | System shall set 注文日 automatically and allow 希望納期 selection |
| FR-07 | Lead Time Validation | System shall validate 希望納期 against lead time and delivery calendar |
| FR-08 | Product Search | System shall support search by 商品名, JAN, 商品コード |
| FR-09 | 商流 Product Filter | System shall display only products available for selected 商流 |
| FR-10 | Contract Price Application | System shall apply valid contract price based on 商流ID, 商品, and 注文日 |
| FR-11 | Quantity Input | System shall support ケース数, バラ数, 重量 input |
| FR-12 | Auto Quantity Calculation | System shall convert package quantity and calculate total quantity |
| FR-13 | MOQ/SPQ Check | System shall validate minimum and standard package quantity in real time |
| FR-14 | Sales Condition Check | System shall block products without valid sales condition |
| FR-15 | Delivery Route Check | System shall validate delivery route compatibility |
| FR-16 | Confirmation Screen | System shall display final order details before confirmation |
| FR-17 | Order Number Generation | System shall generate unique 受注番号 after confirmation |
| FR-18 | D365 Integration | System shall send confirmed order data to D365 immediately |
| FR-19 | Integration Status Management | System shall track 未連携, 連携中, 連携済, 連携エラー |
| FR-20 | Confirmation Email | System should send order confirmation email |
| FR-21 | Order History | System should allow users to search and view past orders |
| FR-22 | Draft Save | System should allow saving incomplete orders as draft |
| FR-23 | Reorder | System should allow copying previous orders with current price recalculation |
| FR-24 | Order Template | System should allow creating and using fixed order templates |
| FR-25 | Favorite Products | System may allow users to register favorite products |
| FR-26 | CSV Bulk Upload | System shall support bulk registration by CSV |
| FR-27 | CSV Validation | System shall validate CSV format, product, quantity, price, and business rules |
| FR-28 | Error CSV Download | System should allow downloading CSV with row-level errors |
| FR-29 | Excel/CSV Download | System should allow order history and master data export |
| FR-30 | Multi-location Support | System shall support ordering for multiple delivery destinations |
| FR-31 | Role Management | System shall control access by role |
| FR-32 | Approval Workflow | System may support approval before order confirmation |
| FR-33 | Operation Log | System shall record login, search, order confirmation, CSV upload/download, master update |
| FR-34 | AI Product Search | System should support natural-language product search |
| FR-35 | AI Validation Explanation | System should explain validation errors in business-friendly language |
| FR-36 | AI CSV Mapping | System should suggest CSV column mapping and row-level correction hints |
| FR-37 | AI Reorder Suggestion | System may suggest reorder candidates based on history |
| FR-38 | Notification | System may notify users about delay, shortage, or D365 integration error |
| FR-39 | Slack/Teams Integration | System may send order or error notifications to external channels |
| FR-40 | Admin Master Maintenance | System should provide master data management screens |

---

## 6. Screen Definition

### SCR-00: Login Screen

| Item | Content |
|---|---|
| Description | User authentication screen |
| Input | Login ID, password |
| Action | Login, password reset |

#### UI Mockup

```text
+------------------------------------------------------+
|              AI BtoB Order System                    |
+------------------------------------------------------+
| Login ID  : [.................................]       |
| Password  : [.................................]       |
|                                                      |
|                [ Login ]                             |
|                                                      |
| Forgot password?                                     |
+------------------------------------------------------+
```

---

### SCR-01: Dashboard

| Item | Content |
|---|---|
| Description | Entry point after login |
| Components | Available customers, recent orders, drafts, alerts, AI assistant |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| AI BtoB Order System                         User: Yamada  Role: 発注担当者        |
+----------------------------------------------------------------------------------+
| Sidebar            | Main Content                                               |
|--------------------|-----------------------------------------------------------|
| New Order          | [ New Order ]                                              |
| Order History      | Recent Orders                                              |
| CSV Upload         | - SO-2026-000123  連携済                                  |
| Templates          | - SO-2026-000122  連携エラー                              |
| Favorites          |                                                           |
| Admin              | Alerts                                                     |
|                    | - D365連携エラー: 1件                                     |
|                    |                                                           |
|                    | AI Assistant: "納入先や商品を自然文で検索できます"         |
+----------------------------------------------------------------------------------+
```

---

### SCR-02: Delivery Destination / 商流 Selection Screen

| Item | Content |
|---|---|
| Description | Select delivery destination and identify 商流ID |
| Components | Search box, delivery destination list, 商流 detail panel |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| New Order > 納入先・商流選択                                                     |
+----------------------------------------------------------------------------------+
| Search: [ 納入先名 / 納入先CD .................. ] [ Search ]                     |
+----------------------------------------------------------------------------------+
| Results                                  | 商流 Detail                            |
|------------------------------------------|----------------------------------------|
| [ ] Tokyo Store 001                      | 注文元: ABC商事                         |
| [ ] Osaka Warehouse 002                  | 納入先: Tokyo Store 001                 |
| [ ] Nagoya Factory 003                   | 商流ID: FLOW-ABC-TKY-001                |
|                                          | 契約: 2026年度 基本契約                 |
|                                          | 配送ルート: Route-A                     |
|                                          | Lead Time: 2 days                       |
|                                          |                                        |
|                                          | [ Confirm 商流 ]                        |
+----------------------------------------------------------------------------------+
```

---

### SCR-03: Order Header Input Screen

| Item | Content |
|---|---|
| Input | 注文日, 希望納期, 納入先, 商流ID |
| Action | Save draft, proceed to product input |

#### UI Mockup

```text
+--------------------------------------------------------------+
| Order Header                                                  |
+--------------------------------------------------------------+
| 商流ID     : FLOW-ABC-TKY-001                                 |
| 注文元     : ABC商事                                           |
| 納入先     : Tokyo Store 001                                   |
| 注文日     : 2026-06-03  [変更不可]                            |
| 希望納期   : [2026-06-06 ▼]                                    |
|                                                              |
| Lead Time Check: OK                                           |
| Delivery Calendar: Available                                 |
|                                                              |
|              [ Save Draft ]  [ Next: Product Input ]          |
+--------------------------------------------------------------+
```

---

### SCR-04: Product Search and Order Detail Input Screen

| Item | Content |
|---|---|
| Description | Search products and input quantities |
| Components | Product search, product result list, order detail grid, AI assistant |

#### UI Mockup

```text
+------------------------------------------------------------------------------------------------+
| New Order > Product Input                                                                       |
+------------------------------------------------------------------------------------------------+
| Product Search: [ 商品名 / JAN / 商品コード .............. ] [ Search ]                         |
| AI Search: "東京店舗に納品できる定番商品を探して" [ Ask AI ]                                    |
+------------------------------------------------------------------------------------------------+
| Search Results                                                                                  |
| Code      | JAN           | Product Name        | Contract Price | Unit     | Action             |
|-----------|---------------|---------------------|----------------|----------|--------------------|
| P-001     | 490000000001  | Milk 1L             | 180 JPY        | case     | [ Add ]            |
| P-002     | 490000000002  | Yogurt 400g         | 120 JPY        | piece    | [ Add ]            |
+------------------------------------------------------------------------------------------------+
| Order Detail                                                                                    |
| Product | Unit   | Case | Piece | Weight | Qty Total | Price | Amount | Validation             |
|---------|--------|------|-------|--------|-----------|-------|--------|------------------------|
| Milk 1L | case   | [10] | [0]   | [-]    | 120       | 180   | 21600  | OK                     |
| Yogurt  | piece  | [0]  | [5]   | [-]    | 5         | 120   | 600    | MOQ Error: min 10      |
+------------------------------------------------------------------------------------------------+
|                                                [ Save Draft ] [ Confirm Order ]                 |
+------------------------------------------------------------------------------------------------+
```

---

### SCR-05: Validation Error Explanation Screen

| Item | Content |
|---|---|
| Description | Show validation errors and AI explanation |
| Components | Error list, affected row, AI explanation, suggested correction |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| Validation Result                                                                |
+----------------------------------------------------------------------------------+
| Error Code | Line | Message                              | Suggested Action       |
|------------|------|--------------------------------------|------------------------|
| MOQ-001    | 2    | Quantity is below MOQ                | Change quantity to 10   |
| PRICE-404  | 3    | Contract price is not configured     | Remove product          |
+----------------------------------------------------------------------------------+
| AI Explanation                                                                    |
|----------------------------------------------------------------------------------|
| Yogurt 400g は選択中の商流では最小発注数量が10個です。                             |
| 現在の入力は5個のため、10個以上に修正してください。                                |
+----------------------------------------------------------------------------------+
```

---

### SCR-06: Confirmation Screen

| Item | Content |
|---|---|
| Description | Final confirmation before order creation |
| Components | Header summary, detail summary, validation status, total amount |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| Order Confirmation                                                               |
+----------------------------------------------------------------------------------+
| 注文元: ABC商事                         納入先: Tokyo Store 001                  |
| 商流ID: FLOW-ABC-TKY-001              希望納期: 2026-06-06                       |
| 注文日: 2026-06-03                                                              |
+----------------------------------------------------------------------------------+
| Product      | Qty | Unit Price | Amount | Delivery Check | Price Check          |
|--------------|-----|------------|--------|----------------|----------------------|
| Milk 1L      | 120 | 180        | 21600  | OK             | OK                   |
| Yogurt 400g  | 10  | 120        | 1200   | OK             | OK                   |
+----------------------------------------------------------------------------------+
| Total Amount: 22800 JPY                                                          |
|                                                                                  |
|                 [ Back ] [ Confirm and Send to D365 ]                            |
+----------------------------------------------------------------------------------+
```

---

### SCR-07: Order Complete / D365 Integration Result Screen

| Item | Content |
|---|---|
| Description | Display order number and integration result |
| Components | 受注番号, D365 status, email status, next actions |

#### UI Mockup

```text
+--------------------------------------------------------------+
| Order Completed                                               |
+--------------------------------------------------------------+
| 受注番号        : SO-2026-000123                              |
| D365連携状態    : 連携済                                      |
| 確認メール      : 送信済                                      |
|                                                              |
| [ View Order ] [ Download PDF ] [ Create New Order ]          |
+--------------------------------------------------------------+
```

---

### SCR-08: CSV Bulk Upload Screen

| Item | Content |
|---|---|
| Description | Upload CSV file and validate rows |
| Components | Template download, upload area, mapping, validation result |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| CSV Bulk Upload                                                                  |
+----------------------------------------------------------------------------------+
| 商流ID: FLOW-ABC-TKY-001                                                          |
| [ Download CSV Template ]                                                         |
|                                                                                  |
| Upload File: [ choose file ................ ] [ Upload ]                          |
+----------------------------------------------------------------------------------+
| AI Column Mapping                                                                 |
| 商品コード Column: [ product_code ▼ ]                                             |
| JAN Column       : [ jan ▼ ]                                                      |
| Quantity Column  : [ qty ▼ ]                                                      |
| Unit Column      : [ unit ▼ ]                                                     |
|                                                                                  |
| [ Validate CSV ]                                                                  |
+----------------------------------------------------------------------------------+
| Row | Product | Qty | Status | Message                                            |
|-----|---------|-----|--------|----------------------------------------------------|
| 1   | P-001   | 120 | OK     |                                                    |
| 2   | P-999   | 10  | Error  | Product not available for selected 商流             |
+----------------------------------------------------------------------------------+
| [ Add Valid Rows ] [ Download Error CSV ]                                         |
+----------------------------------------------------------------------------------+
```

---

### SCR-09: Order History Screen

| Item | Content |
|---|---|
| Description | Search, view, reorder, and export past orders |
| Components | Search filters, order list, reorder button, CSV/Excel download |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| Order History                                                                    |
+----------------------------------------------------------------------------------+
| Date From [2026-06-01] Date To [2026-06-30] 納入先 [........] Status [▼] [Search] |
+----------------------------------------------------------------------------------+
| Order No       | Date       | Delivery To       | Amount | D365 Status | Action    |
|----------------|------------|-------------------|--------|-------------|-----------|
| SO-2026-000123 | 2026-06-03 | Tokyo Store 001   | 22800  | 連携済      | [Reorder] |
| SO-2026-000122 | 2026-06-02 | Osaka WH 002      | 15000  | 連携エラー  | [Detail]  |
+----------------------------------------------------------------------------------+
| [ Download CSV ] [ Download Excel ]                                               |
+----------------------------------------------------------------------------------+
```

---

### SCR-10: Admin Master Management Screen

| Item | Content |
|---|---|
| Description | Manage master data |
| Components | Customer, delivery destination, 商流, product, price, MOQ/SPQ, delivery calendar |

#### UI Mockup

```text
+----------------------------------------------------------------------------------+
| Admin > Master Management                                                        |
+----------------------------------------------------------------------------------+
| Sidebar            | Master List                                                 |
|--------------------|-------------------------------------------------------------|
| Customers          | [ Search master data ................ ] [ Search ]           |
| Delivery Sites     |                                                             |
| 商流 Master         | Code      | Name                  | Status | Action       |
| Product Master     | FLOW-001  | ABC → Tokyo Store     | Active | [Edit]       |
| Price Master       | FLOW-002  | ABC → Osaka WH        | Active | [Edit]       |
| MOQ/SPQ Master     |                                                             |
| Calendar Master    | [ New ] [ Import CSV ] [ Export CSV ]                       |
+----------------------------------------------------------------------------------+
```

---

## 7. Data Definition

### User

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| login_id | string | Login identifier |
| name | string | User name |
| email | string | Email address |
| role | string | 発注担当者, 承認者, 管理者, 営業担当者 |
| status | string | active, suspended, deleted |
| created_at | datetime | Created timestamp |
| updated_at | datetime | Updated timestamp |

### UserCustomerPermission

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| user_id | string | FK to User |
| customer_id | string | FK to Customer |
| delivery_site_id | string | Optional FK to DeliverySite |
| can_order | boolean | Whether user can create order |
| can_approve | boolean | Whether user can approve order |
| status | string | Record status |

### Customer

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| customer_code | string | 注文元CD |
| customer_name | string | 注文元名 |
| billing_type | string | 売掛, 前払い, other |
| status | string | active, inactive |

### DeliverySite

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| delivery_site_code | string | 納入先CD |
| delivery_site_name | string | 納入先名 |
| address | string | Delivery address |
| site_type | string | store, warehouse, factory |
| status | string | active, inactive |

### TradeFlow

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| trade_flow_id | string | 商流ID |
| customer_id | string | FK to Customer |
| delivery_site_id | string | FK to DeliverySite |
| contract_id | string | FK to Contract |
| delivery_route_id | string | FK to DeliveryRoute |
| lead_time_days | int | Required lead time |
| status | string | active, expired, suspended |
| valid_from | date | Valid start date |
| valid_to | date | Valid end date |

### Product

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| product_code | string | 商品コード |
| jan | string | JAN code |
| product_name | string | 商品名 |
| product_category | string | Category |
| base_unit | string | case, piece, kg |
| case_quantity | int | Pieces per case |
| status | string | active, inactive |

### TradeFlowProduct

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| trade_flow_id | string | FK to TradeFlow |
| product_id | string | FK to Product |
| is_available | boolean | Whether product can be ordered |
| sales_condition_status | string | configured, missing, expired |
| status | string | Record status |

### ContractPrice

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| trade_flow_id | string | FK to TradeFlow |
| product_id | string | FK to Product |
| unit_price | decimal | Contract unit price |
| currency | string | JPY |
| valid_from | date | Price valid from |
| valid_to | date | Price valid to |
| status | string | active, expired |

### MOQSPQRule

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| trade_flow_id | string | FK to TradeFlow |
| product_id | string | FK to Product |
| moq | decimal | Minimum order quantity |
| spq | decimal | Standard packing quantity |
| allowed_units | string | case, piece, kg |
| status | string | active, inactive |

### DeliveryRoute

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| route_code | string | 配送ルートCD |
| route_name | string | 配送ルート名 |
| available_weekdays | string | Mon,Tue,Wed,etc. |
| cutoff_time | time | Order cutoff time |
| status | string | active, inactive |

### DeliveryCalendar

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| delivery_route_id | string | FK to DeliveryRoute |
| calendar_date | date | Date |
| is_delivery_available | boolean | Whether delivery is possible |
| reason | string | Holiday, closed day, route unavailable |

### OrderHeader

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| order_no | string | 受注番号 |
| user_id | string | FK to User |
| customer_id | string | FK to Customer |
| delivery_site_id | string | FK to DeliverySite |
| trade_flow_id | string | FK to TradeFlow |
| order_date | date | System date |
| requested_delivery_date | date | 希望納期 |
| status | string | draft, confirmed, cancelled |
| d365_status | string | not_sent, sending, sent, error |
| total_amount | decimal | Total amount |
| created_at | datetime | Created timestamp |
| confirmed_at | datetime | Confirmed timestamp |

### OrderLine

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| order_id | string | FK to OrderHeader |
| line_no | int | Line number |
| product_id | string | FK to Product |
| input_unit | string | case, piece, kg |
| case_qty | decimal | Case quantity |
| piece_qty | decimal | Piece quantity |
| weight_qty | decimal | Weight quantity |
| total_qty | decimal | Converted total quantity |
| unit_price | decimal | Applied contract price |
| amount | decimal | Quantity x price |
| validation_status | string | ok, warning, error |

### D365IntegrationLog

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| order_id | string | FK to OrderHeader |
| request_payload | json | Data sent to D365 |
| response_payload | json | Response from D365 |
| status | string | success, error |
| error_message | string | Error detail |
| retry_count | int | Number of retries |
| created_at | datetime | Timestamp |

### OperationLog

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| user_id | string | FK to User |
| action | string | login, search, confirm_order, csv_upload, csv_download, master_update |
| target_type | string | order, product, master, csv |
| target_id | string | Target record id |
| detail | json | Operation detail |
| ip_address | string | Client IP |
| created_at | datetime | Timestamp |

### OrderTemplate

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| user_id | string | Owner user |
| trade_flow_id | string | FK to TradeFlow |
| template_name | string | Template name |
| status | string | active, inactive |

### OrderTemplateLine

| Field | Type | Description |
|---|---|---|
| id | string | Primary key |
| template_id | string | FK to OrderTemplate |
| product_id | string | FK to Product |
| default_unit | string | case, piece, kg |
| default_qty | decimal | Default quantity |

---

## 8. Non-Functional Requirements

### 8.1 Performance

- Normal screen response time should be less than 2 seconds
- Product search response time should be less than 1.5 seconds for 100,000 products
- CSV validation for 1,000 rows should complete within 10 seconds
- D365 API request should timeout within 30 seconds
- AI explanation should be generated within 5 seconds for validation errors

### 8.2 Security

- Authentication should support password login or SSO
- Authorization should be role-based and customer/delivery-site-based
- Users must not access unauthorized customers or delivery destinations
- Order confirmation, CSV export, and master update must be logged
- Sensitive data should be encrypted in transit by HTTPS
- Passwords must be hashed if local authentication is used
- Admin functions must be restricted to authorized roles
- CSV upload must validate file type, size, encoding, and malicious content

### 8.3 Scale

- Expected users: 1,000 to 10,000 users
- Concurrent sessions: 300 to 1,000
- Product master: 100,000+ records
- Contract price records: 1,000,000+ records
- Order lines per order: up to 500
- CSV upload size: up to 5,000 lines per file
- Multi-location support: 1 customer may have hundreds of delivery destinations

### 8.4 Availability

- Business-hour availability target: 99.5% or higher
- D365 integration failure should not lose confirmed order data
- Failed integrations should be retryable
- System should store integration logs for investigation

### 8.5 Auditability

- All order confirmations must be traceable
- Price applied at order time must be stored in OrderLine
- User, timestamp, 商流ID, price source, validation result must be auditable
- CSV upload/download history must be recorded
- Operation logs should be exportable by admin

### 8.6 Usability

- Product search should support JAN, product code, keyword, and AI natural language
- Validation errors should be displayed per row and per field
- Users should be able to correct errors without leaving the order screen
- Reorder and template functions should reduce repetitive input
- Mobile or tablet-friendly layout is desirable for warehouse/store users

### 8.7 AI Requirements

- AI must not create orders without user confirmation
- AI suggestions must be explainable and editable
- AI must respect user permission and 商流 restrictions
- AI should cite or display the master data basis when recommending products
- AI should only suggest products valid for the selected 商流
- AI should not override business validations
- AI outputs should be logged when used for CSV mapping or correction suggestion

---

## 9. Constraints

- System must identify 商流 before product selection
- Order date must be system date and cannot be manually changed
- Product price must be based on contract price valid on order date
- Products without sales condition cannot be ordered
- MOQ/SPQ and delivery route checks are mandatory before confirmation
- D365 integration is required after order confirmation
- CSV upload must follow approved template or AI-assisted mapping rules
- Role-based access control is mandatory
- Operation log and CSV export log are mandatory
- The hackathon demo may use mock D365 API, but the data structure should be realistic
- Master data may be seeded with sample data for demo purposes

---

## 10. Assumptions

- D365 API endpoint is available or mockable during demo
- Contract price master is maintained outside or inside the system
- 商流ID can be derived from 注文元 and 納入先
- One user may have access to multiple customers and delivery destinations
- One delivery destination may have different 商流 depending on order company or contract
- Price can change by valid date, so historical orders must store the applied price
- Order confirmation email is optional but recommended
- Approval workflow is optional unless business rule requires it
- AI features are assistant functions, not final decision makers
- The MVP should prioritize: 商流 selection, product filtering, contract price, quantity validation, confirmation, D365 mock integration, and operation log

---

## 11. Recommended MVP for Hackathon Demo

Để đạt điểm cao trong hackathon, nên build MVP theo thứ tự này:

| Priority | Feature | Reason |
|---|---|---|
| P0 | Login + permission mock | Chứng minh user chỉ thấy khách hàng/納入先 được phép |
| P0 | 納入先 search + 商流ID xác định | Đây là concept quan trọng nhất của đề |
| P0 | Product search filtered by 商流 | Chứng minh không phải EC thường |
| P0 | Contract price auto apply | Điểm nghiệp vụ BtoB rất quan trọng |
| P0 | Quantity input + MOQ/SPQ check | Cho thấy validation real-time |
| P0 | Confirmation + 受注番号 | Hoàn chỉnh order flow |
| P0 | Mock D365 integration | Bắt buộc theo đề |
| P1 | CSV upload with validation | Dễ gây ấn tượng nếu demo được |
| P1 | AI error explanation | AI dùng đúng chỗ, dễ hiểu |
| P1 | Reorder/template | Tăng tính thực tế |
| P2 | Email/Slack/Teams notification | Nice-to-have |
| P2 | Approval workflow | Nếu còn thời gian |
| P2 | Admin master management | Tốt cho demo, nhưng có thể mock data |

---

## 12. Best Demo Scenario

Một demo max điểm nên đi như sau:

1. Login bằng user `order_user_01`
2. Dashboard hiển thị user có quyền với `ABC商事`
3. Search `Tokyo Store`
4. Chọn `Tokyo Store 001`
5. System tự xác định `FLOW-ABC-TKY-001`
6. Search sản phẩm `Milk`
7. Chỉ hiển thị sản phẩm hợp lệ với 商流 đó
8. Hiển thị contract price `180 JPY`
9. Nhập số lượng `5`
10. System báo lỗi MOQ: minimum `10`
11. AI giải thích lỗi bằng tiếng Nhật dễ hiểu
12. Sửa số lượng thành `10`
13. Chọn 希望納期 không hợp lệ
14. System gợi ý ngày giao hàng hợp lệ
15. Confirm order
16. System tạo `SO-2026-000123`
17. Mock D365 API trả về success
18. Order status thành `連携済`
19. Mở order history và reorder lại đơn cũ
20. Upload CSV có 1 dòng lỗi, system hiển thị row-level validation và cho download error CSV

Đây là flow thể hiện rõ: **商流 → 契約単価 → 商品制御 → validation → D365連携 → AI hỗ trợ nghiệp vụ**.
