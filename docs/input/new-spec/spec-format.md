# REQUIREMENT DEFINITION DOCUMENT

## [System Name]

---

## 1. System Overview

### 1.1 Purpose

[Describe the purpose of the system — what it does, who it is for, and in what context.]

### 1.2 Scope

The system supports:

* [Core feature 1]
* [Core feature 2]
* [Core feature 3]

### 1.3 Glossary

| Term      | Description |
| --------- | ----------- |
| [Term 1]  | [Definition] |
| [Term 2]  | [Definition] |

---

## 2. Stakeholders

| Role     | Description |
| -------- | ----------- |
| [Role 1] | [Responsibilities and permissions] |
| [Role 2] | [Responsibilities and permissions] |
| [Role 3] | [Responsibilities and permissions] |

---

## 3. Business Overview

### 3.1 Business Flow

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]

---

## 4. Use Case Definition (IPA style)

### UC-01: [Use Case Name]

| Item           | Content |
| -------------- | ------- |
| Actor          | [Actor] |
| Description    | [Brief description] |
| Pre-condition  | [Condition that must be true before execution] |
| Post-condition | [State of the system after successful execution] |

**Main Flow:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Exception Flow:**

* [Exception case → how the system handles it]

---

### UC-02: [Use Case Name]

| Item           | Content |
| -------------- | ------- |
| Actor          | [Actor] |
| Description    | [Brief description] |
| Pre-condition  | [Condition before] |
| Post-condition | [Result after] |

**Main Flow:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Exception Flow:**

* [Exception case → how the system handles it]

---

## 5. Functional Requirements

| ID    | Name | Description |
| ----- | ---- | ----------- |
| FR-01 | [Feature name] | [Description] |
| FR-02 | [Feature name] | [Description] |
| FR-03 | [Feature name] | [Description] |
| FR-04 | [Feature name] | [Description] |

---

## 6. Screen Definition

### SCR-00: [Screen Name]

| Item        | Content |
| ----------- | ------- |
| Description | [What this screen is for] |
| Input       | [Input fields] |
| Action      | [Available actions] |

### UI Mockup

```
+------------------------------------------------------+
|                                                      |
|  [Describe layout in ASCII art]                      |
|                                                      |
+------------------------------------------------------+
```

---

### SCR-01: [Screen Name]

| Item       | Content |
| ---------- | ------- |
| Description | [What this screen is for] |
| Components  | [Main UI components] |

### UI Mockup

```
+----------------------------------------------------------------------------------+
| [Header / Navbar]                                                                |
+----------------------------------------------------------------------------------+
| Sidebar            | Main Content                                               |
|--------------------|-----------------------------------------------------------|
| [Nav item 1]       | [Content area description]                                |
| [Nav item 2]       |                                                           |
|--------------------|-----------------------------------------------------------|
```

---

### SCR-02: [Screen Name]

| Item        | Content |
| ----------- | ------- |
| Description | [What this screen is for] |
| Components  | [Main UI components] |

### UI Mockup

```
+----------------------------------------------------------------------------------+
| [Header / Navbar]                                                                |
+----------------------------------------------------------------------------------+
| Sidebar            | Detail Panel                                               |
|--------------------|-----------------------------------------------------------|
| [Nav item 1]       | [Field 1]: [value]                                        |
| [Nav item 2]       | [Field 2]: [value]                                        |
|                    |-----------------------------------------------------------|
|                    | [Section title]                                           |
|                    | [Item 1]                                                  |
+----------------------------------------------------------------------------------+
```

---

### SCR-03: [Screen Name — Create / Edit]

| Item   | Content |
| ------ | ------- |
| Input  | [Form fields] |
| Action | Save, Cancel |

### UI Mockup

```
+--------------------------------------+
| [Form title]                         |
+--------------------------------------+
| [Field 1]: [........................]|
| [Field 2]:                           |
| [..............................]     |
| [Field 3]: [Dropdown]               |
|                                      |
|          [ Save ]  [ Cancel ]        |
+--------------------------------------+
```

---

## 7. Data Definition

### [Entity 1]

| Field   | Type   | Description |
| ------- | ------ | ----------- |
| id      | int    | Primary key |
| [field] | string | [Description] |
| [field] | string | [Description] |
| [field] | int    | [Description] |
| status  | string | Record status |

### [Entity 2]

| Field        | Type   | Description |
| ------------ | ------ | ----------- |
| id           | int    | Primary key |
| [entity1_id] | int    | Foreign key to [Entity 1] |
| [field]      | string | [Description] |
| [field]      | number | [Description] |
| deadline     | date   | Due date |

### User

| Field | Type   | Description |
| ----- | ------ | ----------- |
| id    | int    | Primary key |
| name  | string | Full name |
| role  | string | System role |

---

## 8. Non-Functional Requirements

### 8.1 Performance

* Response time < [X]s

### 8.2 Security

* [Authentication method, e.g. JWT]

* [Authorization model, e.g. role-based access]

### 8.3 Scale

* [Expected user count / concurrent sessions]

---

## 9. Constraints

* [Technical constraint, e.g. Web-based system]
* [Environment constraint, e.g. supported browsers]

---

## 10. Assumptions

* [Assumption 1]
* [Assumption 2]
