# Mapping: m_Load_Latest_Account
**Folder:** AccountProcessing
**Description:** 


## 📂 Source Definitions
### ACCOUNT (SQL Server)
- `ID`: integer (10,0)
- `NAME`: varchar (100,0)
- `PERSONAL`: varchar (255,0)
- `LASTMODIFIED_DATE`: datetime (19,0)

## 🎯 Target Definitions
### DB_ACCOUNT (SQL Server)
- `ID`: integer (10,0)
- `NAME`: varchar (100,0)
- `PERSONAL`: varchar (255,0)
- `LASTMODIFIED_DATE`: datetime (19,0)

## 🔄 Transformations

### SQ_ACCOUNT (Source Qualifier)
**Fields by Group:**

#### Group: default
- `ID` (integer, INPUT/OUTPUT) → No logic (Precision: 10, Scale: )
- `NAME` (varchar, INPUT/OUTPUT) → No logic (Precision: 100, Scale: )
- `PERSONAL` (varchar, INPUT/OUTPUT) → No logic (Precision: 255, Scale: )
- `LASTMODIFIED_DATE` (datetime, INPUT/OUTPUT) → No logic (Precision: 19, Scale: )

### LKP_MAX_DATE (Lookup Procedure)
**SQL Override:**
```sql
SELECT MAX(LASTMODIFIED_DATE) AS MAX_DATE FROM ACCOUNT
```
**Fields by Group:**

#### Group: default
- `MAX_DATE` (datetime, LOOKUP/OUTPUT) → No logic (Precision: 19, Scale: )

### EXP_COMPARE_DATE (Expression)
**Fields by Group:**

#### Group: default
- `LASTMODIFIED_DATE` (datetime, INPUT) → No logic (Precision: , Scale: )
- `MAX_DATE` (datetime, INPUT) → No logic (Precision: , Scale: )
- `o_IS_LATEST` (integer, OUTPUT) → IIF(LASTMODIFIED_DATE = MAX_DATE, 1, 0) (Precision: , Scale: )

### RTR_LATEST_RECORD (Router)
**Groups:**
- `LATEST` (None): `(no condition)`
**Fields by Group:**

#### Group: default
- `ID` (integer, INPUT) → No logic (Precision: , Scale: )
- `NAME` (varchar, INPUT) → No logic (Precision: 100, Scale: )
- `PERSONAL` (varchar, INPUT) → No logic (Precision: 255, Scale: )
- `LASTMODIFIED_DATE` (datetime, INPUT) → No logic (Precision: , Scale: )
- `o_IS_LATEST` (integer, INPUT) → No logic (Precision: , Scale: )

## 🔁 Connector Flow
- `SQ_ACCOUNT`.`ID` ➝ `RTR_LATEST_RECORD`.`ID`
- `SQ_ACCOUNT`.`NAME` ➝ `RTR_LATEST_RECORD`.`NAME`
- `SQ_ACCOUNT`.`PERSONAL` ➝ `RTR_LATEST_RECORD`.`PERSONAL`
- `SQ_ACCOUNT`.`LASTMODIFIED_DATE` ➝ `EXP_COMPARE_DATE`.`LASTMODIFIED_DATE`
- `LKP_MAX_DATE`.`MAX_DATE` ➝ `EXP_COMPARE_DATE`.`MAX_DATE`
- `SQ_ACCOUNT`.`LASTMODIFIED_DATE` ➝ `EXP_COMPARE_DATE`.`LASTMODIFIED_DATE`
- `EXP_COMPARE_DATE`.`o_IS_LATEST` ➝ `RTR_LATEST_RECORD`.`o_IS_LATEST`
- `RTR_LATEST_RECORD`.`ID` ➝ `DB_ACCOUNT`.`ID`
- `RTR_LATEST_RECORD`.`NAME` ➝ `DB_ACCOUNT`.`NAME`
- `RTR_LATEST_RECORD`.`PERSONAL` ➝ `DB_ACCOUNT`.`PERSONAL`
- `RTR_LATEST_RECORD`.`LASTMODIFIED_DATE` ➝ `DB_ACCOUNT`.`LASTMODIFIED_DATE`