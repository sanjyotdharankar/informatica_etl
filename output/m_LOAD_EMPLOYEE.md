# Mapping: m_LOAD_EMPLOYEE
**Folder:** SampleFolder
**Description:** 


## 📂 Source Definitions
### EMPLOYEE_SOURCE (Oracle)
- `EMP_ID`: number (10,0)
- `EMP_NAME`: varchar2 (50,0)

## 🎯 Target Definitions
### EMPLOYEE_TARGET (Oracle)
- `EMP_ID`: number (10,0)
- `EMP_NAME`: varchar2 (50,0)

## 🔄 Transformations

### SQ_EMPLOYEE (Source Qualifier)
**Fields by Group:**

#### Group: default
- `EMP_ID` (number, INPUT/OUTPUT) → No logic (Precision: 10, Scale: 0)
- `EMP_NAME` (varchar2, INPUT/OUTPUT) → No logic (Precision: 50, Scale: 0)

### EXP_EMPLOYEE (Expression)
**Fields by Group:**

#### Group: default
- `EMP_ID` (number, INPUT/OUTPUT) → No logic (Precision: 10, Scale: 0)
- `EMP_NAME` (varchar2, INPUT/OUTPUT) → No logic (Precision: 50, Scale: 0)

## 🔁 Connector Flow
- `EMPLOYEE_SOURCE`.`EMP_ID` ➝ `SQ_EMPLOYEE`.`EMP_ID`
- `EMPLOYEE_SOURCE`.`EMP_NAME` ➝ `SQ_EMPLOYEE`.`EMP_NAME`
- `SQ_EMPLOYEE`.`EMP_ID` ➝ `EXP_EMPLOYEE`.`EMP_ID`
- `SQ_EMPLOYEE`.`EMP_NAME` ➝ `EXP_EMPLOYEE`.`EMP_NAME`
- `EXP_EMPLOYEE`.`EMP_ID` ➝ `EMPLOYEE_TARGET`.`EMP_ID`
- `EXP_EMPLOYEE`.`EMP_NAME` ➝ `EMPLOYEE_TARGET`.`EMP_NAME`