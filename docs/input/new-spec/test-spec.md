# REQUIREMENT DEFINITION DOCUMENT

## Simple Login App

---

## 1. System Overview

### 1.1 Purpose

Hệ thống là một ứng dụng đơn giản dùng để test agent.  
Ứng dụng cho phép người dùng đăng nhập và truy cập vào màn hình chính.

### 1.2 Scope

The system supports:

* Đăng nhập bằng email và password
* Hiển thị màn hình chính sau khi đăng nhập thành công
* Đăng xuất khỏi hệ thống

### 1.3 Glossary

| Term | Description |
| ---- | ----------- |
| User | Người dùng sử dụng ứng dụng |
| Login | Chức năng xác thực người dùng |
| Home Screen | Màn hình chính sau khi đăng nhập |

---

## 2. Stakeholders

| Role | Description |
| ---- | ----------- |
| User | Đăng nhập và sử dụng màn hình chính |
| System | Kiểm tra thông tin đăng nhập và điều hướng màn hình |

---

## 3. Business Overview

### 3.1 Business Flow

1. User mở ứng dụng
2. System hiển thị màn hình Login
3. User nhập email và password
4. User bấm nút Login
5. System kiểm tra thông tin đăng nhập
6. Nếu hợp lệ, System chuyển sang màn hình chính
7. User có thể bấm Logout để quay lại màn hình Login

---

## 4. Use Case Definition

### UC-01: Login

| Item | Content |
| ---- | ------- |
| Actor | User |
| Description | User đăng nhập vào hệ thống bằng email và password |
| Pre-condition | User đang ở màn hình Login |
| Post-condition | User được chuyển sang màn hình chính nếu đăng nhập thành công |

**Main Flow:**

1. User nhập email
2. User nhập password
3. User bấm nút Login
4. System kiểm tra email và password
5. System chuyển user sang màn hình chính

**Exception Flow:**

* Nếu email hoặc password trống, hiển thị message: `Please enter email and password`
* Nếu thông tin đăng nhập sai, hiển thị message: `Invalid email or password`

---

### UC-02: Logout

| Item | Content |
| ---- | ------- |
| Actor | User |
| Description | User đăng xuất khỏi hệ thống |
| Pre-condition | User đang ở màn hình chính |
| Post-condition | User được chuyển về màn hình Login |

**Main Flow:**

1. User bấm nút Logout
2. System xóa trạng thái đăng nhập
3. System chuyển user về màn hình Login

**Exception Flow:**

* Không có

---

## 5. Functional Requirements

| ID | Name | Description |
| -- | ---- | ----------- |
| FR-01 | Login Form | Hệ thống hiển thị form gồm email, password và nút Login |
| FR-02 | Validate Login Input | Hệ thống kiểm tra email và password không được để trống |
| FR-03 | Login Success | Nếu thông tin hợp lệ, hệ thống chuyển sang màn hình chính |
| FR-04 | Login Error | Nếu thông tin không hợp lệ, hệ thống hiển thị lỗi |
| FR-05 | Home Screen | Hệ thống hiển thị màn hình chính đơn giản |
| FR-06 | Logout | User có thể đăng xuất và quay lại màn hình Login |

---

## 6. Screen Definition

### SCR-01: Login Screen

| Item | Content |
| ---- | ------- |
| Description | Màn hình cho phép user đăng nhập vào hệ thống |
| Input | Email, Password |
| Action | Login |

### UI Mockup

```text
+--------------------------------------+
|              Simple App              |
+--------------------------------------+
|                                      |
|  Email:    [......................]  |
|                                      |
|  Password: [......................]  |
|                                      |
|              [ Login ]               |
|                                      |
|  Error message area                  |
|                                      |
+--------------------------------------+
````

---

### SCR-02: Home Screen

| Item        | Content                                                  |
| ----------- | -------------------------------------------------------- |
| Description | Màn hình chính hiển thị thông tin đơn giản sau khi login |
| Components  | Header, welcome text, summary cards, logout button       |

### UI Mockup

```text
+--------------------------------------------------+
| Simple App                              [Logout] |
+--------------------------------------------------+
|                                                  |
|  Welcome, User!                                  |
|                                                  |
|  +----------------+  +----------------+          |
|  | Total Items    |  | Status         |          |
|  | 10             |  | Active         |          |
|  +----------------+  +----------------+          |
|                                                  |
|  Recent Activity                                 |
|  - Login success                                 |
|  - Viewed home screen                            |
|                                                  |
+--------------------------------------------------+
```

---

## 7. Data Definition

### User

| Field    | Type   | Description                        |
| -------- | ------ | ---------------------------------- |
| id       | int    | Primary key                        |
| email    | string | Email dùng để đăng nhập            |
| password | string | Password dùng để đăng nhập         |
| name     | string | Tên user                           |
| status   | string | Trạng thái user: active / inactive |

### Session

| Field      | Type     | Description                |
| ---------- | -------- | -------------------------- |
| id         | int      | Primary key                |
| user_id    | int      | ID của user đang đăng nhập |
| token      | string   | Login session token        |
| created_at | datetime | Thời gian đăng nhập        |

---

## 8. Non-Functional Requirements

### 8.1 Performance

* Login response time < 2 seconds
* Home screen loading time < 2 seconds

### 8.2 Security

* Password không hiển thị dạng plain text trên UI
* Password input phải được mask
* Chỉ user login thành công mới được truy cập màn hình chính

### 8.3 Scale

* Hệ thống dùng cho mục đích test agent
* Không yêu cầu scale lớn

---

## 9. Constraints

* Ứng dụng chỉ cần 2 màn hình: Login và Home
* Không cần chức năng đăng ký user
* Không cần chức năng quên mật khẩu
* Không cần màn hình setting hoặc profile

---

## 10. Assumptions

* Có sẵn một user test trong hệ thống
* Agent có thể dùng thông tin login giả lập để test flow
* Sau khi logout, user quay lại màn hình Login

````

User test gợi ý:

```text
Email: test@example.com
Password: password123
````
