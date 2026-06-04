# REQUIREMENT DEFINITION DOCUMENT

## AI BtoB 商流型 受発注システム

---

## 0. Max Score Evaluation Focus

Judges are likely to expect a system that is **more than a simple order-entry screen**. The demo should show a realistic BtoB business flow.

| Evaluation Point | What should be shown to score highly |
|---|---|
| 商流ID as the core concept | Before product selection, the system must identify `注文元 → 納入先 → 商流ID`. Price, available products, MOQ, and lead time all depend on the selected 商流. |
| Clear BtoB business logic | The system must not look like a B2C e-commerce flow. It should include customers, delivery destinations, contract prices, accounts-receivable orders, and ERP integration. |
| Practical AI usage | AI should support delivery-destination search, product search, validation-error explanation, CSV mapping, reorder/template suggestions, and anomaly detection. |
| End-to-end demo | Login → select 納入先/商流 → input header → search products → input quantity → validation → confirmation → generate 受注番号 → mock D365 integration. |
| Clear master data | The demo should include 担当者, 顧客, 納入先, 商流, 商品, 契約単価, MOQ/SPQ, 配送カレンダー, and 注文. |
| Strong validation | The system must block products without 販売条件, invalid MOQ/SPQ, delivery dates incompatible with 配送ルート, and expired prices. |
| Demo-ready UI | The UI should include dashboard, search, cart/order input, confirmation, history, CSV import/export, and admin master screens. |
| D365 integration | The system should show integration status, retry handling, error logs, payload preview, or a mock API. |
| Audit and security | The system should include role-based access, 操作ログ, CSV export logs, and user permissions by customer/site. |

---

## 1. System Overview

### 1.1 Purpose

This system is an order-management support system for BtoB transactions. Using `商流ID` as the core business key, it enables order users to select the correct delivery destination, contract conditions, products, and prices, create accounts-receivable orders, and immediately integrate confirmed orders with the core ERP system, D365.

The objectives of the system are as follows.

- Always determine the trade flow from `注文元 → 納入先` before order creation.
- Automatically apply available products, contract prices, MOQ/SPQ, and delivery conditions based on the selected 商流.
- Prevent input errors, price errors, and delivery-date errors in real time.
- Improve ordering efficiency through CSV bulk registration, order templates, and reorder functions.
- Immediately send confirmed orders to D365 and make the integration status traceable.
- Use AI to support product search, CSV import assistance, error explanations, and order suggestions.

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
| 商流ID | An ID that uniquely identifies the order company, delivery destination, and contract conditions in a BtoB transaction |
| 注文元 | The company or business partner that places the order |
| 納入先 | The store, warehouse, factory, or other site where products are delivered |
| 担当者 | The user who actually performs order operations |
| 契約単価 | The sales price applied based on 商流, product, and validity period |
| 取扱可能商品 | Products that can be ordered under a specific 商流 |
| MOQ | Minimum Order Quantity |
| SPQ | Standard Packing Quantity or standard ordering/packing unit |
| 荷姿 | The input unit, such as case, piece, or weight |
| 希望納期 | The delivery date requested by the order user |
| リードタイム | The number of days required from order receipt to delivery |
| 配送ルート | The delivery route available for the delivery destination |
| 売掛注文 | A BtoB order based on deferred payment/accounts receivable |
| D365 | Microsoft Dynamics 365, the core ERP system |
| CSV一括登録 | A function for registering multiple order lines together by CSV |
| 操作ログ | Audit records for user operations, order confirmations, CSV exports, and related actions |

---

## 2. Stakeholders

| Role | Description |
|---|---|
| 発注担当者 | Selects the delivery destination, enters products, quantities, and requested delivery dates, and creates orders |
| 代理入力者 | Enters orders on behalf of multiple customers or multiple locations |
| 承認者 | Reviews and approves order contents when approval is required |
| 営業担当者 | Checks customers, contract prices, available products, and order history |
| マスタ管理者 | Manages customers, delivery destinations, trade flows, products, prices, MOQ/SPQ, and delivery conditions |
| 物流担当者 | Checks delivery dates, delivery routes, shortages, and delay information |
| 経理・受注管理担当者 | Checks accounts-receivable orders, order numbers, and D365 integration status |
| システム管理者 | Manages user permissions, operation logs, integration errors, and CSV export history |
| AI Assistant | Supports product search, CSV import assistance, error-reason explanations, and reorder suggestions |

---

## 3. Business Overview

### 3.1 Business Flow

1. The order user logs in.
2. The system loads the order-company and delivery-destination permissions linked to the login ID.
3. The user searches for and selects a delivery destination.
4. The system determines the 商流ID from `注文元 → 納入先`.
5. The system loads contract prices, available products, and delivery conditions based on the 商流ID.
6. The user enters header information such as order date and requested delivery date.
7. The user searches products by product name, JAN, or product code.
8. The user enters quantities by case, piece, weight, or other supported units.
9. The system checks MOQ/SPQ, sales conditions, delivery date, and delivery route in real time.
10. The user reviews the order contents.
11. The system generates a 受注番号 and confirms the order.
12. The system immediately integrates the order with D365.
13. The system records the integration success or failure status.
14. The system sends a confirmation email and provides order history and CSV/Excel export when necessary.

### 3.2 AI Usage Flow

1. The user searches for delivery destinations and products using natural language.  
   Example: `Find milk that can be delivered to the Tokyo warehouse.`
2. AI refers to the trade flow, product master, and contract prices, then presents candidate products.
3. During CSV upload, AI guesses column meanings and maps product code, JAN, and quantity columns.
4. When a validation error occurs, AI explains the business reason in user-friendly language.  
   Example: `This product does not have configured sales conditions for the selected 商流.`
5. Based on order history, AI suggests standard order patterns and reorder candidates.

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
|              AI BtoB受発注システム                    |
+------------------------------------------------------+
| ログインID : [.................................]       |
| パスワード : [.................................]       |
|                                                      |
|                [ ログイン ]                           |
|                                                      |
| パスワードをお忘れですか？                            |
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
| AI BtoB受発注システム                     ユーザー: 山田  役割: 発注担当者          |
+----------------------------------------------------------------------------------+
| サイドバー         | メインコンテンツ                                          |
|--------------------|-----------------------------------------------------------|
| 新規注文           | [ 新規注文 ]                                              |
| 注文履歴           | 最近の注文                                                |
| CSVアップロード    | - SO-2026-000123  連携済                                  |
| テンプレート       | - SO-2026-000122  連携エラー                              |
| お気に入り         |                                                           |
| 管理               | アラート                                                  |
|                    | - D365連携エラー: 1件                                     |
|                    |                                                           |
|                    | AIアシスタント: "納入先や商品を自然文で検索できます"       |
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
| 新規注文 > 納入先・商流選択                                                     |
+----------------------------------------------------------------------------------+
| 検索: [ 納入先名 / 納入先CD .................. ] [ 検索 ]                         |
+----------------------------------------------------------------------------------+
| 検索結果                                  | 商流詳細                              |
|------------------------------------------|----------------------------------------|
| [ ] 東京店舗 001                         | 注文元: ABC商事                         |
| [ ] 大阪倉庫 002                         | 納入先: 東京店舗 001                    |
| [ ] 名古屋工場 003                       | 商流ID: FLOW-ABC-TKY-001                |
|                                          | 契約: 2026年度 基本契約                 |
|                                          | 配送ルート: ルートA                     |
|                                          | リードタイム: 2日                       |
|                                          |                                        |
|                                          | [ 商流を確定 ]                          |
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
| 注文ヘッダー                                                 |
+--------------------------------------------------------------+
| 商流ID     : FLOW-ABC-TKY-001                                 |
| 注文元     : ABC商事                                           |
| 納入先     : 東京店舗 001                                      |
| 注文日     : 2026-06-03  [変更不可]                            |
| 希望納期   : [2026-06-06 ▼]                                    |
|                                                              |
| リードタイムチェック: OK                                      |
| 配送カレンダー: 配送可能                                      |
|                                                              |
|              [ 下書き保存 ]  [ 次へ: 商品入力 ]                |
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
| 新規注文 > 商品入力                                                                          |
+------------------------------------------------------------------------------------------------+
| 商品検索: [ 商品名 / JAN / 商品コード .............. ] [ 検索 ]                                 |
| AI検索: "東京店舗に納品できる定番商品を探して" [ AIに聞く ]                                    |
+------------------------------------------------------------------------------------------------+
| 検索結果                                                                                        |
| コード    | JAN           | 商品名              | 契約単価       | 単位     | 操作               |
|-----------|---------------|---------------------|----------------|----------|--------------------|
| P-001     | 490000000001  | 牛乳 1L             | 180 JPY        | ケース   | [ 追加 ]           |
| P-002     | 490000000002  | ヨーグルト 400g     | 120 JPY        | 個       | [ 追加 ]           |
+------------------------------------------------------------------------------------------------+
| 注文明細                                                                                        |
| 商品    | 単位   | ケース | バラ | 重量 | 合計数量 | 単価 | 金額 | 検証結果                 |
|---------|--------|------|-------|--------|-----------|-------|--------|------------------------|
| 牛乳 1L | ケース | [10] | [0]   | [-]   | 120      | 180  | 21600 | OK                       |
| ヨーグルト| 個   | [0]  | [5]   | [-]   | 5        | 120  | 600   | MOQエラー: 最小10        |
+------------------------------------------------------------------------------------------------+
|                                                [ 下書き保存 ] [ 注文確認 ]                       |
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
| 検証結果                                                                        |
+----------------------------------------------------------------------------------+
| エラーコード | 行 | メッセージ                         | 推奨対応               |
|------------|------|--------------------------------------|------------------------|
| MOQ-001    | 2  | 数量がMOQを下回っています            | 数量を10に変更          |
| PRICE-404  | 3  | 契約単価が設定されていません          | 商品を削除              |
+----------------------------------------------------------------------------------+
| AI説明                                                                          |
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
| 注文確認                                                                        |
+----------------------------------------------------------------------------------+
| 注文元: ABC商事                         納入先: 東京店舗 001                    |
| 商流ID: FLOW-ABC-TKY-001              希望納期: 2026-06-06                       |
| 注文日: 2026-06-03                                                              |
+----------------------------------------------------------------------------------+
| 商品         | 数量 | 単価       | 金額   | 配送チェック | 価格チェック          |
|--------------|-----|------------|--------|----------------|----------------------|
| 牛乳 1L      | 120 | 180        | 21600  | OK             | OK                   |
| ヨーグルト400g| 10  | 120        | 1200   | OK             | OK                   |
+----------------------------------------------------------------------------------+
| 合計金額: 22800 JPY                                                             |
|                                                                                  |
|                 [ 戻る ] [ 確定してD365へ連携 ]                                  |
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
| 注文完了                                                     |
+--------------------------------------------------------------+
| 受注番号        : SO-2026-000123                              |
| D365連携状態    : 連携済                                      |
| 確認メール      : 送信済                                      |
|                                                              |
| [ 注文を見る ] [ PDFダウンロード ] [ 新規注文作成 ]          |
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
| CSV一括アップロード                                                              |
+----------------------------------------------------------------------------------+
| 商流ID: FLOW-ABC-TKY-001                                                          |
| [ CSVテンプレートダウンロード ]                                                  |
|                                                                                  |
| アップロードファイル: [ ファイル選択 ............ ] [ アップロード ]              |
+----------------------------------------------------------------------------------+
| AI列マッピング                                                                   |
| 商品コード列: [ product_code ▼ ]                                                  |
| JAN列       : [ jan ▼ ]                                                           |
| 数量列      : [ qty ▼ ]                                                           |
| 単位列      : [ unit ▼ ]                                                          |
|                                                                                  |
| [ CSV検証 ]                                                                      |
+----------------------------------------------------------------------------------+
| 行 | 商品 | 数量 | ステータス | メッセージ                                      |
|-----|---------|-----|--------|----------------------------------------------------|
| 1   | P-001   | 120 | OK     |                                                    |
| 2  | P-999 | 10 | エラー | 選択中の商流では取扱不可の商品です                 |
+----------------------------------------------------------------------------------+
| [ 有効行を追加 ] [ エラーCSVダウンロード ]                                       |
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
| 注文履歴                                                                        |
+----------------------------------------------------------------------------------+
| 開始日 [2026-06-01] 終了日 [2026-06-30] 納入先 [........] ステータス [▼] [検索] |
+----------------------------------------------------------------------------------+
| 注文番号       | 注文日     | 納入先            | 金額   | D365状態 | 操作       |
|----------------|------------|-------------------|--------|-------------|-----------|
| SO-2026-000123 | 2026-06-03 | 東京店舗 001      | 22800  | 連携済   | [再注文]   |
| SO-2026-000122 | 2026-06-02 | 大阪倉庫 002      | 15000  | 連携エラー | [詳細]    |
+----------------------------------------------------------------------------------+
| [ CSVダウンロード ] [ Excelダウンロード ]                                        |
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
| 管理 > マスタ管理                                                               |
+----------------------------------------------------------------------------------+
| サイドバー         | マスタ一覧                                                  |
|--------------------|-------------------------------------------------------------|
| 顧客               | [ マスタデータ検索 ................ ] [ 検索 ]               |
| 納入先             |                                                             |
| 商流マスタ         | コード    | 名称                  | 状態   | 操作         |
| 商品マスタ         | FLOW-001  | ABC → 東京店舗        | 有効   | [編集]       |
| 単価マスタ         | FLOW-002  | ABC → 大阪倉庫        | 有効   | [編集]       |
| MOQ/SPQマスタ      |                                                             |
| カレンダーマスタ   | [ 新規 ] [ CSV取込 ] [ CSV出力 ]                            |
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

To score highly in the hackathon, the MVP should be built in the following priority order:

| Priority | Feature | Reason |
|---|---|---|
| P0 | Login + permission mock | Demonstrates that users can only see permitted customers and 納入先. |
| P0 | 納入先 search + 商流ID identification | This is the most important concept in the assignment. |
| P0 | Product search filtered by 商流 | Demonstrates that the system is not a generic e-commerce flow. |
| P0 | Contract price auto-application | This is a key BtoB business requirement. |
| P0 | Quantity input + MOQ/SPQ check | Shows real-time validation. |
| P0 | Confirmation + 受注番号 | Completes the order flow. |
| P0 | Mock D365 integration | Required by the assignment. |
| P1 | CSV upload with validation | Creates a strong impression if it can be demonstrated. |
| P1 | AI error explanation | Shows practical and easy-to-understand AI usage. |
| P1 | Reorder/template | Increases business realism. |
| P2 | Email/Slack/Teams notification | Nice to have. |
| P2 | Approval workflow | Add this if time remains. |
| P2 | Admin master management | Good for demo quality, but sample/mock data is acceptable. |

---

## 12. Best Demo Scenario

A high-scoring demo should proceed as follows:

1. Log in as user `order_user_01`.
2. The dashboard shows that the user has permission for `ABC商事`.
3. Search for `Tokyo Store`.
4. Select `Tokyo Store 001`.
5. The system automatically identifies `FLOW-ABC-TKY-001`.
6. Search for product `Milk`.
7. The system displays only products valid for that 商流.
8. The system displays the contract price `180 JPY`.
9. Enter quantity `5`.
10. The system shows an MOQ error: minimum `10`.
11. AI explains the error in easy-to-understand Japanese.
12. Correct the quantity to `10`.
13. Select an invalid 希望納期.
14. The system suggests a valid delivery date.
15. Confirm the order.
16. The system generates `SO-2026-000123`.
17. The mock D365 API returns success.
18. The order status becomes `連携済`.
19. Open order history and reorder from a previous order.
20. Upload a CSV with one invalid row. The system displays row-level validation and allows error CSV download.

This flow clearly demonstrates: **商流 → 契約単価 → 商品制御 → validation → D365連携 → AI-supported business operations**.
