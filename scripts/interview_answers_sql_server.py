ANSWERS = {
"q_sql_transaction_implement": """<h2>Transaction in SQL — What It Is &amp; How to Implement</h2>
<p>A <strong>transaction</strong> groups one or more SQL statements into one atomic unit: all succeed (<strong>COMMIT</strong>) or all undo (<strong>ROLLBACK</strong>).</p>
<h3>How to implement (T-SQL)</h3>
<pre><code>SET XACT_ABORT ON;
BEGIN TRANSACTION;

BEGIN TRY
    INSERT INTO Orders (CustomerId, Total)
    VALUES (101, 250.00);

    INSERT INTO OrderLines (OrderId, ProductId, Qty)
    VALUES (SCOPE_IDENTITY(), 5, 2);

    UPDATE Inventory SET Qty = Qty - 2 WHERE ProductId = 5;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT &gt; 0
        ROLLBACK TRANSACTION;
    THROW;
END CATCH;</code></pre>
<h3>In application code (ADO.NET)</h3>
<pre><code>await using var tx = await connection.BeginTransactionAsync();
try
{
    await cmd1.ExecuteNonQueryAsync();
    await cmd2.ExecuteNonQueryAsync();
    await tx.CommitAsync();
}
catch
{
    await tx.RollbackAsync();
    throw;
}</code></pre>
<h3>Key rules</h3>
<ul>
<li>Keep transactions <strong>short</strong> to reduce locking and deadlocks.</li>
<li>Use <code>TRY/CATCH</code> + check <code>@@TRANCOUNT</code> so failures always roll back.</li>
<li>One business operation = one transaction boundary when possible.</li>
</ul>
<h3>Interview Answer</h3>
<p>I wrap related DML in BEGIN TRANSACTION, commit on success, and roll back on any error using TRY/CATCH. In .NET I use explicit transactions on the connection or EF SaveChanges inside a transaction so related rows stay consistent.</p>""",

"q_sql_cte_used": """<h2>CTE — What Is It? Have You Used It?</h2>
<p>A <strong>Common Table Expression (CTE)</strong> is a named temporary result set defined with <code>WITH</code>, used in a single SELECT/INSERT/UPDATE/DELETE statement. It makes complex queries readable and supports <strong>recursion</strong>.</p>
<pre><code>WITH ActiveEmployees AS (
    SELECT EmployeeId, Name, DeptId, Salary
    FROM Employees
    WHERE IsActive = 1
),
DeptAvg AS (
    SELECT DeptId, AVG(Salary) AS AvgSalary
    FROM ActiveEmployees
    GROUP BY DeptId
)
SELECT e.Name, e.Salary, d.AvgSalary
FROM ActiveEmployees e
JOIN DeptAvg d ON e.DeptId = d.DeptId
WHERE e.Salary &gt; d.AvgSalary;</code></pre>
<h3>Where I have used CTEs</h3>
<ul>
<li><strong>Reporting</strong> — break a long query into readable steps (filters → aggregates → final join).</li>
<li><strong>Hierarchy</strong> — recursive CTE for org chart / parent-child trees.</li>
<li><strong>Row numbering</strong> — rank salaries, remove duplicates with <code>ROW_NUMBER()</code>.</li>
<li><strong>Stored procedures</strong> — multi-step ETL inside one batch without permanent temp tables.</li>
</ul>
<pre><code>-- Recursive CTE — employee hierarchy
WITH EmpHierarchy AS (
    SELECT EmployeeId, ManagerId, Name, 0 AS Level
    FROM Employees WHERE ManagerId IS NULL
    UNION ALL
    SELECT e.EmployeeId, e.ManagerId, e.Name, h.Level + 1
    FROM Employees e
    JOIN EmpHierarchy h ON e.ManagerId = h.EmployeeId
)
SELECT * FROM EmpHierarchy;</code></pre>
<h3>CTE vs subquery / temp table</h3>
<ul>
<li>CTE — readable, can reference itself (recursive), scoped to one statement.</li>
<li>Temp table — persists for the session/batch; better for very large intermediate sets.</li>
</ul>
<h3>Interview Answer</h3>
<p>Yes — I use CTEs to split complex SQL into named steps and for recursive hierarchies. A CTE is defined with WITH and exists only for that statement. I prefer CTEs over nested subqueries when the same intermediate set is referenced multiple times or when the logic is easier to read top to bottom.</p>""",

"q_sql_transaction_what": """<h2>What Is a Transaction in SQL? (Not “Transition”)</h2>
<p>In interviews, <strong>“Transition”</strong> usually means <strong>Transaction</strong> — a logical unit of work where one or more SQL statements succeed or fail <strong>together</strong>.</p>
<p>A <strong>transaction</strong> groups operations so the database stays consistent: either all changes are applied, or none are (after ROLLBACK).</p>
<pre><code>BEGIN TRANSACTION;

UPDATE Accounts SET Balance = Balance - 1000 WHERE AccountId = 1;
UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountId = 2;

-- If both succeed:
COMMIT TRANSACTION;

-- If any step fails:
ROLLBACK TRANSACTION;</code></pre>
<h3>Why transactions matter</h3>
<ul>
<li><strong>Money transfer</strong> — debit and credit must both happen or neither.</li>
<li><strong>Order + order lines</strong> — header and details inserted atomically.</li>
<li><strong>Batch imports</strong> — 500 rows: all valid rows commit together or roll back on failure (depending on design).</li>
</ul>
<h3>Transaction boundaries</h3>
<p>Start with <code>BEGIN TRAN</code> (or implicit transaction), end with <code>COMMIT</code> (save) or <code>ROLLBACK</code> (undo). SQL Server follows <strong>ACID</strong> properties for transactional work.</p>
<h3>Interview Answer</h3>
<p>A transaction is a group of SQL operations treated as one unit. If any part fails, I roll back so the database is not left half-updated. I use explicit transactions for financial transfers, multi-table inserts, and batch jobs where consistency is critical.</p>""",

"q_sql_acid": """<h2>ACID Properties in SQL Server</h2>
<p><strong>ACID</strong> describes guarantees of a reliable database transaction.</p>
<table>
<tr><th>Property</th><th>Meaning</th><th>Example</th></tr>
<tr><td><strong>A</strong>tomicity</td><td>All or nothing</td><td>Transfer: debit + credit both commit or both roll back</td></tr>
<tr><td><strong>C</strong>onsistency</td><td>Valid state before and after</td><td>Constraints, FKs, checks still hold after COMMIT</td></tr>
<tr><td><strong>I</strong>solation</td><td>Concurrent transactions don't corrupt each other</td><td>Isolation levels (READ COMMITTED, SERIALIZABLE)</td></tr>
<tr><td><strong>D</strong>urability</td><td>Committed data survives crash</td><td>Written to transaction log; recovered after restart</td></tr>
</table>
<h3>Atomicity</h3>
<pre><code>BEGIN TRAN;
  INSERT INTO Orders (...) VALUES (...);
  INSERT INTO OrderLines (...) VALUES (...);
  -- Error on line 2 → ROLLBACK removes order header too
COMMIT;</code></pre>
<h3>Isolation (levels)</h3>
<ul>
<li><strong>READ COMMITTED</strong> — default; no dirty reads.</li>
<li><strong>REPEATABLE READ</strong> — same row read twice returns same value.</li>
<li><strong>SERIALIZABLE</strong> — strictest; prevents phantoms.</li>
<li><strong>SNAPSHOT</strong> — row versioning without shared locks for reads.</li>
</ul>
<h3>Interview Answer</h3>
<p>ACID means transactions are Atomic (all-or-nothing), Consistent (rules enforced), Isolated (controlled concurrency), and Durable (committed data survives failure). SQL Server implements this through the transaction log, locks/row versioning, and constraints.</p>""",

"q_sql_inserted_deleted": """<h2>Difference Between INSERTED and DELETED (SQL Server)</h2>
<p>In DML triggers, SQL Server provides two <strong>virtual tables</strong> — <code>inserted</code> and <code>deleted</code> — holding row versions involved in the change.</p>
<table>
<tr><th>Virtual table</th><th>Contains</th><th>Operation</th></tr>
<tr><td><code>inserted</code></td><td><strong>New</strong> row values</td><td>INSERT, UPDATE (after image)</td></tr>
<tr><td><code>deleted</code></td><td><strong>Old</strong> row values</td><td>DELETE, UPDATE (before image)</td></tr>
</table>
<h3>By operation</h3>
<ul>
<li><strong>INSERT</strong> — only <code>inserted</code> has rows.</li>
<li><strong>DELETE</strong> — only <code>deleted</code> has rows.</li>
<li><strong>UPDATE</strong> — <code>deleted</code> = old values, <code>inserted</code> = new values.</li>
</ul>
<pre><code>CREATE TRIGGER trg_EmployeeAudit ON Employees
AFTER UPDATE
AS
BEGIN
    INSERT INTO EmployeeAudit (EmployeeId, OldSalary, NewSalary, ChangedAt)
    SELECT d.EmployeeId, d.Salary, i.Salary, GETUTCDATE()
    FROM deleted d
    INNER JOIN inserted i ON d.EmployeeId = i.EmployeeId
    WHERE d.Salary &lt;&gt; i.Salary;
END;</code></pre>
<h3>Key Points</h3>
<ul>
<li>They exist only inside triggers — not ordinary queries.</li>
<li>Same structure as the base table (for that trigger's table).</li>
<li>Use JOIN inserted/deleted for UPDATE to pair old and new rows (usually by PK).</li>
</ul>
<h3>Interview Answer</h3>
<p>inserted holds new rows after INSERT or UPDATE; deleted holds old rows after DELETE or UPDATE. For an UPDATE, both are populated so I can audit changes by joining them on the primary key.</p>""",

"q_sql_transaction_scenario": """<h2>Transaction Scenario — Partial Insert of 500 Records</h2>
<p><strong>Scenario:</strong> Insert 500 rows into a staging table and a main table. Row 300 fails (constraint violation). What happens depends on how you handle the transaction.</p>
<h3>Option 1 — Single transaction (all or nothing)</h3>
<pre><code>SET XACT_ABORT ON;
BEGIN TRANSACTION;

BEGIN TRY
    INSERT INTO Staging (Col1, Col2)
    SELECT Col1, Col2 FROM @BulkData;  -- 500 rows

    INSERT INTO MainTable (Col1, Col2)
    SELECT Col1, Col2 FROM Staging;

    COMMIT TRANSACTION;
    -- All 500 committed only if every statement succeeds
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    -- Row 300 failure → entire batch undone
    THROW;
END CATCH;</code></pre>
<p><strong>Result:</strong> Failure at row 300 → <strong>ROLLBACK</strong> → zero rows in MainTable (and Staging if in same tran).</p>
<h3>Option 2 — Row-by-row with savepoints (partial success)</h3>
<pre><code>BEGIN TRANSACTION;

DECLARE @i INT = 1;
WHILE @i &lt;= 500
BEGIN
    SAVE TRANSACTION sp_row;

    BEGIN TRY
        INSERT INTO MainTable (...) VALUES (...);  -- one row
        COMMIT TRANSACTION sp_row;  -- not valid — use nested or per-row tran
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION sp_row;
        -- log error row, continue
    END CATCH;

    SET @i += 1;
END;

COMMIT TRANSACTION;</code></pre>
<p>Often implemented as <strong>separate small transactions</strong> per row or batch of 50 with error logging — 499 succeed, 1 fails.</p>
<h3>Option 3 — Set-based with validation first (recommended)</h3>
<pre><code>BEGIN TRAN;
    INSERT INTO Staging SELECT * FROM @BulkData;

    -- Reject batch if any invalid
    IF EXISTS (SELECT 1 FROM Staging WHERE Col1 IS NULL)
        THROW 50000, 'Invalid rows in batch', 1;

    INSERT INTO MainTable SELECT * FROM Staging WHERE IsValid = 1;
COMMIT;</code></pre>
<h3>Interview Answer</h3>
<p>With one BEGIN TRAN around all 500 inserts, a failure at row 300 causes ROLLBACK and none of the rows persist. If the business needs partial success, I use per-row or batched transactions with error logging, or validate the full set in staging before a single COMMIT. I always clarify requirements: all-or-nothing vs best-effort import.</p>""",

"q_sql_commit_rollback": """<h2>COMMIT and ROLLBACK in SQL Server</h2>
<p><strong>COMMIT</strong> makes all changes in the current transaction <strong>permanent</strong>. <strong>ROLLBACK</strong> <strong>undoes</strong> all changes since the last BEGIN TRANSACTION.</p>
<table>
<tr><th>Command</th><th>Effect</th></tr>
<tr><td><code>BEGIN TRANSACTION</code></td><td>Start a transaction boundary</td></tr>
<tr><td><code>COMMIT</code> / <code>COMMIT TRANSACTION</code></td><td>Save all changes; release locks</td></tr>
<tr><td><code>ROLLBACK</code> / <code>ROLLBACK TRANSACTION</code></td><td>Undo all changes in the transaction</td></tr>
<tr><td><code>SAVE TRANSACTION name</code></td><td>Savepoint within a transaction (partial rollback)</td></tr>
</table>
<pre><code>BEGIN TRANSACTION;

UPDATE Inventory SET Qty = Qty - 10 WHERE ProductId = 5;

IF @@ERROR &lt;&gt; 0
BEGIN
    ROLLBACK TRANSACTION;
    RETURN;
END

INSERT INTO OrderHistory (ProductId, Qty) VALUES (5, 10);

COMMIT TRANSACTION;</code></pre>
<h3>Modern pattern — TRY/CATCH + XACT_ABORT</h3>
<pre><code>SET XACT_ABORT ON;
BEGIN TRANSACTION;

BEGIN TRY
    INSERT INTO Orders (...) VALUES (...);
    INSERT INTO OrderLines (...) VALUES (...);
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT &gt; 0
        ROLLBACK TRANSACTION;

    DECLARE @msg NVARCHAR(4000) = ERROR_MESSAGE();
    RAISERROR(@msg, 16, 1);
END CATCH;</code></pre>
<h3>Key Points</h3>
<ul>
<li><code>@@TRANCOUNT</code> — number of open transactions; ROLLBACK all if &gt; 0 in CATCH.</li>
<li>Uncommitted changes are visible only within the session (depending on isolation).</li>
<li><code>XACT_ABORT ON</code> auto-rolls back on runtime errors.</li>
</ul>
<h3>Interview Answer</h3>
<p>COMMIT persists everything since BEGIN TRAN; ROLLBACK reverses it. I wrap related DML in TRY/CATCH, check @@TRANCOUNT, and ROLLBACK on failure so the database never ends up half-updated. SAVE TRANSACTION allows rolling back to a savepoint without aborting the whole batch.</p>""",

"q_sql_clustered_one_per_table": """<h2>How Many Clustered Indexes per Table?</h2>
<p>In SQL Server, a table can have <strong>at most one clustered index</strong>. The clustered index defines the <strong>physical sort order</strong> of the data rows (or is the table itself).</p>
<h3>Rules</h3>
<ul>
<li><strong>0 clustered indexes</strong> — table is a <strong>heap</strong> (unordered storage).</li>
<li><strong>1 clustered index</strong> — normal case; often on PRIMARY KEY.</li>
<li><strong>2+ clustered indexes</strong> — <strong>not allowed</strong> on one table.</li>
</ul>
<pre><code>-- One clustered index (typical)
CREATE TABLE Employees (
    EmployeeId INT PRIMARY KEY CLUSTERED,  -- clustered index on PK
    Name NVARCHAR(100),
    DeptId INT
);

-- Many NON-clustered indexes allowed
CREATE NONCLUSTERED INDEX IX_Emp_Dept ON Employees(DeptId);
CREATE NONCLUSTERED INDEX IX_Emp_Name ON Employees(Name);</code></pre>
<h3>Heap vs clustered</h3>
<table>
<tr><th>Storage</th><th>Clustered index</th></tr>
<tr><td>Heap</td><td>No clustered index — rows stored in insertion order</td></tr>
<tr><td>Clustered table</td><td>One clustered index — leaf level = data pages</td></tr>
</table>
<p>You can have <strong>many non-clustered indexes</strong> (up to 999 on older versions, 999 nonclustered + 1 clustered in practice). Non-clustered leaf nodes point to the clustered key or RID (heap).</p>
<h3>Interview Answer</h3>
<p>Only one clustered index per table because it controls physical row order. You can have zero (heap) or one (usually on the primary key). Non-clustered indexes are unlimited in practice and are separate structures that reference the clustered key or row identifier.</p>""",

"q_sql_window_functions": """<h2>Window Functions in SQL Server</h2>
<p><strong>Window functions</strong> perform calculations across a set of rows <strong>related to the current row</strong> without collapsing rows into groups (unlike <code>GROUP BY</code>). They use <code>OVER (PARTITION BY ... ORDER BY ...)</code>.</p>
<h3>Common window functions</h3>
<table>
<tr><th>Function</th><th>Purpose</th></tr>
<tr><td><code>ROW_NUMBER()</code></td><td>Unique sequential number per partition (ties get different numbers)</td></tr>
<tr><td><code>RANK()</code></td><td>Rank with gaps after ties (1, 1, 3)</td></tr>
<tr><td><code>DENSE_RANK()</code></td><td>Rank without gaps (1, 1, 2)</td></tr>
<tr><td><code>NTILE(n)</code></td><td>Divide rows into n buckets</td></tr>
<tr><td><code>LAG / LEAD</code></td><td>Previous / next row value</td></tr>
<tr><td><code>SUM / AVG / COUNT</code> OVER</td><td>Running or partition totals (analytics)</td></tr>
</table>
<pre><code>SELECT
    EmployeeId,
    Name,
    DeptId,
    Salary,
    ROW_NUMBER() OVER (PARTITION BY DeptId ORDER BY Salary DESC) AS RowNum,
    RANK()       OVER (PARTITION BY DeptId ORDER BY Salary DESC) AS SalaryRank,
    DENSE_RANK() OVER (PARTITION BY DeptId ORDER BY Salary DESC) AS DenseRank,
    SUM(Salary)  OVER (PARTITION BY DeptId) AS DeptTotal
FROM Employees;</code></pre>
<h3>Window vs GROUP BY</h3>
<pre><code>-- GROUP BY — one row per dept
SELECT DeptId, AVG(Salary) FROM Employees GROUP BY DeptId;

-- Window — keeps every employee row, adds dept average
SELECT Name, Salary,
       AVG(Salary) OVER (PARTITION BY DeptId) AS DeptAvg
FROM Employees;</code></pre>
<h3>Important rules</h3>
<ul>
<li>Cannot use window functions directly in <code>WHERE</code> — wrap in CTE/subquery and filter outside.</li>
<li><code>PARTITION BY</code> is optional (whole result set is one partition).</li>
<li><code>ORDER BY</code> in OVER defines ranking and running calculations.</li>
</ul>
<h3>RANK vs DENSE_RANK (quick reference)</h3>
<table>
<tr><th>Salaries</th><th>RANK</th><th>DENSE_RANK</th></tr>
<tr><td>100, 100, 90</td><td>1, 1, 3</td><td>1, 1, 2</td></tr>
</table>
<h3>Interview Answer</h3>
<p>Window functions compute over a row set defined by OVER without grouping rows away. I use ROW_NUMBER for top-N and pagination, RANK/DENSE_RANK for leaderboards, and SUM/AVG OVER for running totals. I filter results in an outer query or CTE because OVER cannot go in WHERE.</p>""",

"q_sql_select_into_where": """<h2>SELECT * INTO — WHERE 1 = 0 vs WHERE 1 = 1</h2>
<p><code>SELECT * INTO</code> creates a <strong>new table</strong> and populates it from a query. The <code>WHERE</code> clause controls whether <strong>rows</strong> are copied; the <strong>column structure</strong> always comes from the source query.</p>
<h3>1) WHERE 1 = 0 — structure only, no data</h3>
<pre><code>SELECT * INTO NewTable FROM OldTable WHERE 1 = 0;</code></pre>
<p><strong>What happens:</strong></p>
<ul>
<li>Creates <code>NewTable</code> with the <strong>same columns and data types</strong> as <code>OldTable</code>.</li>
<li>Copies <strong>zero rows</strong> (condition is always false).</li>
<li>Table is empty but ready for INSERT/ETL.</li>
</ul>
<h3>2) WHERE 1 = 1 — structure + all data</h3>
<pre><code>SELECT * INTO NewTable FROM OldTable WHERE 1 = 1;</code></pre>
<p><strong>What happens:</strong></p>
<ul>
<li>Creates <code>NewTable</code> with the same columns and types.</li>
<li>Copies <strong>every row</strong> from <code>OldTable</code> (condition is always true).</li>
<li>Equivalent to a full table copy in one statement.</li>
</ul>
<h3>Side-by-side</h3>
<table>
<tr><th></th><th>WHERE 1 = 0</th><th>WHERE 1 = 1</th></tr>
<tr><td>Rows copied</td><td>0</td><td>All rows</td></tr>
<tr><td>Schema copied</td><td>Yes (columns, types)</td><td>Yes</td></tr>
<tr><td>Indexes / PK / FK / constraints</td><td colspan="2">Not copied — only columns</td></tr>
<tr><td>Triggers / defaults</td><td colspan="2">Not copied</td></tr>
</table>
<h3>What is NOT copied (both cases)</h3>
<p><code>SELECT INTO</code> does <strong>not</strong> copy indexes, primary keys, foreign keys, constraints, triggers, or extended properties. You get a heap-like new table with data (or empty). Add indexes/constraints afterward if needed.</p>
<h3>Temp table variant</h3>
<pre><code>-- Empty temp table with same shape as source
SELECT * INTO #Staging FROM dbo.Orders WHERE 1 = 0;

-- Full copy into temp table (session-scoped)
SELECT * INTO #OrdersBackup FROM dbo.Orders WHERE 1 = 1;</code></pre>
<h3>Real-time use cases</h3>
<table>
<tr><th>Pattern</th><th>Use case</th></tr>
<tr><td><strong>WHERE 1 = 0</strong></td><td>Quickly clone <strong>table structure</strong> for staging, migration scripts, or empty sandbox tables</td></tr>
<tr><td><strong>WHERE 1 = 0</strong></td><td>ETL: create target shell, then <code>INSERT INTO NewTable SELECT ...</code> with transforms</td></tr>
<tr><td><strong>WHERE 1 = 0</strong></td><td>Create temp table matching production columns before bulk load</td></tr>
<tr><td><strong>WHERE 1 = 1</strong></td><td>One-shot <strong>backup/snapshot</strong> of a table before risky UPDATE/DELETE</td></tr>
<tr><td><strong>WHERE 1 = 1</strong></td><td>Copy production subset to reporting DB (often with a real filter instead of 1=1)</td></tr>
<tr><td><strong>WHERE 1 = 1</strong></td><td>Archive historical data: <code>SELECT * INTO Archive2024 FROM Orders WHERE OrderDate &gt;= '2024-01-01'</code></td></tr>
</table>
<pre><code>-- Real example: backup before mass update
SELECT * INTO Orders_Backup_20250602 FROM Orders WHERE 1 = 1;
UPDATE Orders SET Status = 'Closed' WHERE OrderDate &lt; '2020-01-01';

-- Real example: staging table for import
SELECT * INTO dbo.Customer_Staging FROM dbo.Customer WHERE 1 = 0;
BULK INSERT dbo.Customer_Staging FROM 'file.csv' ...;</code></pre>
<h3>Modern alternatives</h3>
<ul>
<li><code>SELECT TOP 0 * INTO ...</code> — same effect as <code>WHERE 1 = 0</code>.</li>
<li><code>CREATE TABLE ... AS SELECT</code> — not in SQL Server; use <code>SELECT INTO</code> or <code>CREATE TABLE</code> + <code>INSERT</code>.</li>
<li>For schema only: <code>Script Table as CREATE</code> in SSMS, or <code>CREATE TABLE ... LIKE</code> (other databases).</li>
</ul>
<h3>Interview Answer</h3>
<p>WHERE 1 = 0 creates a new table with the same columns but no rows — I use it to clone structure for staging or migrations. WHERE 1 = 1 creates the table and copies all rows — I use it for quick backups or snapshots before destructive changes. Neither copies indexes or constraints; only column definitions and optionally data.</p>""",

"q_sql_scenario_pagination": """<h2>Pagination in SQL Server</h2>
<p><strong>Pagination</strong> returns one page of rows at a time (e.g. page 2, 10 rows per page) instead of loading the entire table.</p>
<h3>OFFSET / FETCH (SQL Server 2012+) — recommended</h3>
<pre><code>DECLARE @PageNumber INT = 2;   -- 2nd page
DECLARE @PageSize     INT = 10;

SELECT EmployeeId, Name, DeptId
FROM Employees
ORDER BY EmployeeId   -- stable sort required
OFFSET (@PageNumber - 1) * @PageSize ROWS
FETCH NEXT @PageSize ROWS ONLY;</code></pre>
<p>Page 1 → <code>OFFSET 0</code>, Page 2 → <code>OFFSET 10</code>, etc.</p>
<h3>Total count for UI (optional)</h3>
<pre><code>SELECT COUNT(*) AS TotalRows FROM Employees;

-- Or window function in one query (heavier on large tables)
SELECT *, COUNT(*) OVER() AS TotalRows
FROM Employees
ORDER BY EmployeeId
OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;</code></pre>
<h3>Legacy: ROW_NUMBER()</h3>
<pre><code>SELECT EmployeeId, Name
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY EmployeeId) AS rn
    FROM Employees
) t
WHERE rn BETWEEN 11 AND 20;  -- page 2, size 10</code></pre>
<h3>Key Points</h3>
<ul>
<li>Always <code>ORDER BY</code> — without it, page order is undefined.</li>
<li>Large <code>OFFSET</code> on huge tables can be slow (skips many rows); keyset pagination is better for deep pages.</li>
<li>API pattern: pass <code>page</code> and <code>pageSize</code> as parameters to a stored procedure.</li>
</ul>
<h3>Interview Answer</h3>
<p>I paginate with ORDER BY plus OFFSET/FETCH: OFFSET (page-1)*pageSize ROWS FETCH NEXT pageSize ROWS ONLY. I return total count separately for the UI and use a stable sort column like primary key.</p>""",

"q_sql_scenario_gender_codes": """<h2>Insert Gender Values — Male = 'M', Female = 'F', Other = 'O'</h2>
<p>Interviewers want a lookup table, constrained column, or seed INSERT. Common patterns:</p>
<h3>Option 1 — Lookup table + INSERT</h3>
<pre><code>CREATE TABLE Gender (
    GenderCode CHAR(1) PRIMARY KEY,
    GenderName VARCHAR(10) NOT NULL
);

INSERT INTO Gender (GenderName, GenderCode) VALUES
    ('Male',   'M'),
    ('Female', 'F'),
    ('Other',  'O');</code></pre>
<h3>Option 2 — UserDetails with CHECK constraint</h3>
<pre><code>CREATE TABLE UserDetails (
    UserId   INT PRIMARY KEY,
    FullName NVARCHAR(100),
    Gender   CHAR(1) NOT NULL
        CHECK (Gender IN ('M', 'F', 'O'))
);

INSERT INTO UserDetails (UserId, FullName, Gender) VALUES
    (1, 'Alice', 'F'),
    (2, 'Bob',   'M'),
    (3, 'Sam',   'O');</code></pre>
<h3>Option 3 — Display name in query</h3>
<pre><code>SELECT UserId, FullName, Gender,
    CASE Gender
        WHEN 'M' THEN 'Male'
        WHEN 'F' THEN 'Female'
        WHEN 'O' THEN 'Other'
    END AS GenderLabel
FROM UserDetails;</code></pre>
<h3>Interview Answer</h3>
<p>I store single-letter codes M/F/O with a CHECK constraint or foreign key to a Gender lookup table, and INSERT the three rows into the lookup. In reports I use CASE or join to Gender for full names.</p>""",

"q_sql_scenario_default_age": """<h2>Create UserDetails Table — Default Age = 18</h2>
<pre><code>CREATE TABLE UserDetails (
    UserId   INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL,
    Email    NVARCHAR(255),
    Age      INT NOT NULL DEFAULT 18
);</code></pre>
<h3>Behavior</h3>
<ul>
<li>If INSERT omits <code>Age</code>, SQL Server sets it to <strong>18</strong>.</li>
<li>Explicit value still allowed: <code>INSERT ... VALUES (..., 25)</code>.</li>
</ul>
<pre><code>-- Age becomes 18 automatically
INSERT INTO UserDetails (FullName, Email)
VALUES ('Priya', 'priya@example.com');

-- Age explicitly 25
INSERT INTO UserDetails (FullName, Email, Age)
VALUES ('Rahul', 'rahul@example.com', 25);

SELECT * FROM UserDetails;</code></pre>
<h3>Alter existing table</h3>
<pre><code>ALTER TABLE UserDetails
ADD Age INT NOT NULL CONSTRAINT DF_UserDetails_Age DEFAULT 18
    WITH VALUES;  -- fills existing rows with 18</code></pre>
<h3>Interview Answer</h3>
<p>I define the Age column as INT NOT NULL DEFAULT 18 in CREATE TABLE so new rows get 18 when Age is not supplied. For existing tables I use ALTER TABLE ADD ... DEFAULT with WITH VALUES if needed.</p>""",

"q_sql_scenario_tanker": """<h2>3rd Highest Tanker Water Level &amp; Duplicate Tanker Names</h2>
<p>Sample table:</p>
<pre><code>CREATE TABLE Tankers (
    TankerId    INT PRIMARY KEY,
    TankerName  NVARCHAR(100),
    WaterLevel  DECIMAL(10,2)  -- capacity / level reading
);

INSERT INTO Tankers VALUES
(1, 'Alpha-1', 5000),
(2, 'Beta-2',  8000),
(3, 'Alpha-1', 8000),   -- duplicate name
(4, 'Gamma',   6000),
(5, 'Delta',   8000);</code></pre>
<h3>1) 3rd highest water level (distinct levels)</h3>
<pre><code>-- DENSE_RANK — 3rd distinct level (8000, 6000, 5000 → 3rd is 5000)
SELECT WaterLevel AS ThirdHighestLevel
FROM (
    SELECT WaterLevel,
           DENSE_RANK() OVER (ORDER BY WaterLevel DESC) AS dr
    FROM Tankers
) t
WHERE dr = 3;

-- OFFSET — 3rd row when levels ordered distinct
SELECT DISTINCT WaterLevel
FROM Tankers
ORDER BY WaterLevel DESC
OFFSET 2 ROWS FETCH NEXT 1 ROW ONLY;</code></pre>
<h3>2) Duplicate tanker names</h3>
<pre><code>-- Names appearing more than once
SELECT TankerName, COUNT(*) AS DuplicateCount
FROM Tankers
GROUP BY TankerName
HAVING COUNT(*) &gt; 1;

-- All rows for duplicate names only
SELECT t.*
FROM Tankers t
INNER JOIN (
    SELECT TankerName
    FROM Tankers
    GROUP BY TankerName
    HAVING COUNT(*) &gt; 1
) d ON t.TankerName = d.TankerName
ORDER BY t.TankerName, t.TankerId;</code></pre>
<h3>Clarify in interview</h3>
<ul>
<li><strong>3rd highest level</strong> — distinct values (DENSE_RANK) vs 3rd row (ROW_NUMBER)?</li>
<li>Ties at 8000: DENSE_RANK gives 1,1,2…; ROW_NUMBER gives 1,2,3…</li>
</ul>
<h3>Interview Answer</h3>
<p>For 3rd highest water level I use DENSE_RANK over ORDER BY WaterLevel DESC and filter dr = 3, or DISTINCT with OFFSET 2. For duplicate tanker names I GROUP BY TankerName HAVING COUNT(*) &gt; 1, then join back to list all matching rows.</p>""",

"q_sql_scenario_2nd_salary": """<h2>SQL Query for 2nd Highest Salary</h2>
<p>Find the <strong>second highest</strong> salary (usually the 2nd distinct value when salaries can repeat).</p>
<h3>Method 1 — DENSE_RANK (handles ties on highest)</h3>
<pre><code>SELECT Salary AS SecondHighestSalary
FROM (
    SELECT Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS dr
    FROM Employees
) t
WHERE dr = 2;</code></pre>
<h3>Method 2 — OFFSET / FETCH (2nd distinct salary)</h3>
<pre><code>SELECT DISTINCT Salary AS SecondHighestSalary
FROM Employees
ORDER BY Salary DESC
OFFSET 1 ROWS FETCH NEXT 1 ROW ONLY;</code></pre>
<h3>Method 3 — Subquery with MAX</h3>
<pre><code>SELECT MAX(Salary) AS SecondHighestSalary
FROM Employees
WHERE Salary &lt; (SELECT MAX(Salary) FROM Employees);</code></pre>
<p>Works when you want the max salary below the top; if two people share highest salary, this still returns the correct 2nd distinct level.</p>
<h3>Employee(s) earning 2nd highest</h3>
<pre><code>SELECT EmployeeId, Name, Salary
FROM Employees
WHERE Salary = (
    SELECT MAX(Salary) FROM Employees
    WHERE Salary &lt; (SELECT MAX(Salary) FROM Employees)
);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Clarify: <strong>2nd distinct salary</strong> vs <strong>2nd row</strong> (use ROW_NUMBER for 2nd row).</li>
<li>Index on <code>Salary DESC</code> helps large tables.</li>
</ul>
<h3>Interview Answer</h3>
<p>For 2nd highest salary I use DENSE_RANK with ORDER BY Salary DESC and filter dr = 2, or DISTINCT salaries with OFFSET 1 FETCH NEXT 1. The MAX subquery pattern also works: MAX(Salary) WHERE Salary &lt; (SELECT MAX(Salary) FROM Employees).</p>""",

"q_sql_scenario_delete_duplicate": """<h2>Delete One of the Duplicate Records</h2>
<p>Keep <strong>one row</strong> per duplicate group; delete the rest. Define the duplicate key (e.g. same <code>Email</code> or same <code>Email + UserName</code>).</p>
<h3>Step 1 — Preview duplicates (CTE + ROW_NUMBER)</h3>
<pre><code>WITH DupCTE AS (
    SELECT UserID, Email, UserName,
           ROW_NUMBER() OVER (
               PARTITION BY Email        -- duplicate rule
               ORDER BY UserID           -- keep lowest UserID
           ) AS rn
    FROM dbo.[User]
)
SELECT * FROM DupCTE WHERE rn &gt; 1;   -- rows to delete</code></pre>
<h3>Step 2 — DELETE duplicates (keep rn = 1)</h3>
<pre><code>WITH DupCTE AS (
    SELECT UserID, Email, UserName,
           ROW_NUMBER() OVER (
               PARTITION BY Email
               ORDER BY UserID
           ) AS rn
    FROM dbo.[User]
)
DELETE FROM DupCTE
WHERE rn &gt; 1;</code></pre>
<p>SQL Server allows <code>DELETE</code> from a CTE on a <strong>single base table</strong> when the CTE is deterministic.</p>
<h3>With primary key (simpler)</h3>
<pre><code>DELETE e
FROM Employees e
INNER JOIN (
    SELECT Email, MIN(EmployeeId) AS KeepId
    FROM Employees
    GROUP BY Email
    HAVING COUNT(*) &gt; 1
) d ON e.Email = d.Email AND e.EmployeeId &gt; d.KeepId;</code></pre>
<h3>Safety</h3>
<ul>
<li>Run <code>SELECT</code> preview first; wrap in <code>BEGIN TRAN</code> / <code>ROLLBACK</code> to test.</li>
<li>Backup table or use <code>DELETE</code> output clause for audit.</li>
</ul>
<h3>Interview Answer</h3>
<p>I use a CTE with ROW_NUMBER partitioned by the duplicate columns, ORDER BY a tie-breaker like lowest ID to choose which row to keep, then DELETE WHERE rn &gt; 1. I always preview duplicates before deleting and use a transaction in production scripts.</p>""",

"q_sql_scenario_optimize_query": """<h2>How Can We Optimize Query Performance?</h2>
<p>Optimize using <strong>measurement first</strong> (execution plan, duration, IO), then apply targeted fixes.</p>
<h3>1. Find the bottleneck</h3>
<ul>
<li>Enable <strong>actual execution plan</strong> in SSMS.</li>
<li>Look for <strong>table/clustered index scans</strong>, high cost %, missing index hints.</li>
<li>Check <code>SET STATISTICS IO, TIME ON</code> for logical reads and elapsed time.</li>
</ul>
<h3>2. Indexing</h3>
<ul>
<li>Add nonclustered indexes on <strong>WHERE</strong>, <strong>JOIN</strong>, and <strong>ORDER BY</strong> columns.</li>
<li>Use <strong>covering indexes</strong> (INCLUDE columns) to avoid key lookups.</li>
<li>Remove unused/redundant indexes that slow writes.</li>
<li>Update <strong>statistics</strong> (<code>UPDATE STATISTICS</code> or automatic).</li>
</ul>
<h3>3. Write better SQL</h3>
<ul>
<li>Avoid <code>SELECT *</code> — return only needed columns.</li>
<li>Filter early; avoid functions on indexed columns in WHERE (<code>WHERE YEAR(d)=2024</code> → range on <code>d</code>).</li>
<li>Replace correlated subqueries with JOINs or window functions when plans are bad.</li>
<li>Use <code>EXISTS</code> instead of <code>IN</code> for large subqueries when appropriate.</li>
<li>Paginate large results — do not return millions of rows.</li>
</ul>
<h3>4. Server &amp; design</h3>
<ul>
<li>Fix <strong>implicit conversions</strong> (NVARCHAR column vs VARCHAR parameter).</li>
<li>Reduce <strong>blocking</strong> — shorter transactions, right isolation level.</li>
<li>Partition very large tables; archive old data.</li>
<li>Warm cache for critical reports; use read replicas for reporting.</li>
</ul>
<pre><code>-- Bad — non-sargable
WHERE YEAR(OrderDate) = 2024

-- Better — sargable range
WHERE OrderDate &gt;= '2024-01-01' AND OrderDate &lt; '2025-01-01';</code></pre>
<h3>Checklist</h3>
<table>
<tr><th>Symptom</th><th>Typical fix</th></tr>
<tr><td>Scan on large table</td><td>Index on filter/join columns</td></tr>
<tr><td>Key lookup high cost</td><td>Covering index with INCLUDE</td></tr>
<tr><td>Bad cardinality estimate</td><td>Update stats, recompile, fix parameter sniffing</td></tr>
<tr><td>Too many rows returned</td><td>Filter, paginate, project fewer columns</td></tr>
</table>
<h3>Interview Answer</h3>
<p>I start with the execution plan and missing-index suggestions, then add or tune indexes on filter and join columns, avoid SELECT * and non-sargable predicates, and keep statistics current. I measure before and after each change rather than adding indexes blindly.</p>""",

"q_sql_joins_self_join": """<h2>What Are Joins? What Is a Self Join?</h2>
<p>A <strong>JOIN</strong> combines rows from two or more tables based on a related column (usually primary key = foreign key).</p>
<h3>Quick reference</h3>
<table>
<tr><th>Join</th><th>Result</th></tr>
<tr><td><strong>INNER JOIN</strong></td><td>Only matching rows from both tables</td></tr>
<tr><td><strong>LEFT JOIN</strong></td><td>All rows from left table + matches from right (NULL if no match)</td></tr>
<tr><td><strong>RIGHT JOIN</strong></td><td>All rows from right + matches from left</td></tr>
<tr><td><strong>FULL OUTER JOIN</strong></td><td>All rows from both; NULL where no match</td></tr>
<tr><td><strong>CROSS JOIN</strong></td><td>Cartesian product — every row paired with every row</td></tr>
<tr><td><strong>SELF JOIN</strong></td><td>Same table joined to itself using aliases</td></tr>
</table>
<h3>Sample tables (retail banking)</h3>
<pre><code>Customer(CustomerId, Name, BranchId)
Account(AccountId, CustomerId, AccountNumber, Balance)
Branch(BranchId, BranchName, City)
Employee(EmployeeId, Name, ManagerId, BranchId)</code></pre>
<h3>1. INNER JOIN</h3>
<p><strong>Meaning:</strong> Returns rows only when a match exists in <strong>both</strong> tables.</p>
<pre><code>-- Customers who have at least one account
SELECT c.Name, a.AccountNumber, a.Balance
FROM Customer c
INNER JOIN Account a ON c.CustomerId = a.CustomerId;</code></pre>
<p><strong>Real-time scenario:</strong> Monthly statement job — fetch only customers with active accounts to generate PDF statements. Prospects with no account are excluded.</p>
<h3>2. LEFT JOIN (LEFT OUTER JOIN)</h3>
<p><strong>Meaning:</strong> Returns <strong>all rows from the left table</strong>, plus matching rows from the right (NULL if no match).</p>
<pre><code>-- All customers, including those with no account yet
SELECT c.Name, a.AccountNumber, a.Balance
FROM Customer c
LEFT JOIN Account a ON c.CustomerId = a.CustomerId;

-- Branches with zero customers (see departments with 0 employees pattern)
SELECT b.BranchName, c.Name AS CustomerName
FROM Branch b
LEFT JOIN Customer c ON c.BranchId = b.BranchId;</code></pre>
<p><strong>Real-time scenario:</strong> CRM dashboard showing every registered customer and their accounts — if a new customer has not opened an account, account columns show NULL so sales can follow up.</p>
<h3>3. RIGHT JOIN (RIGHT OUTER JOIN)</h3>
<p><strong>Meaning:</strong> Returns <strong>all rows from the right table</strong>, plus matches from the left (NULL if no match). Same as LEFT JOIN with tables swapped — LEFT JOIN is used more often.</p>
<pre><code>-- All accounts, even if customer record is missing (data quality check)
SELECT c.Name, a.AccountNumber, a.Balance
FROM Customer c
RIGHT JOIN Account a ON c.CustomerId = a.CustomerId;</code></pre>
<p><strong>Real-time scenario:</strong> Data reconciliation after ETL — find accounts in the core system whose customer master row is missing (orphan accounts for investigation).</p>
<h3>4. FULL OUTER JOIN</h3>
<p><strong>Meaning:</strong> Returns all rows from <strong>both</strong> tables — matched rows once, unmatched rows with NULL on the missing side.</p>
<pre><code>-- Compare customers in CRM vs core banking
SELECT
    crm.CustomerId AS CrmId,
    core.CustomerId AS CoreId,
    COALESCE(crm.Name, core.Name) AS Name
FROM CrmCustomer crm
FULL OUTER JOIN CoreCustomer core
    ON crm.CustomerId = core.CustomerId
WHERE crm.CustomerId IS NULL OR core.CustomerId IS NULL;</code></pre>
<p><strong>Real-time scenario:</strong> Nightly sync between marketing CRM and core banking — identify customers present in only one system so ops can merge or fix duplicates.</p>
<h3>5. CROSS JOIN</h3>
<p><strong>Meaning:</strong> Every row from table A paired with <strong>every</strong> row from table B (no ON clause). Row count = A × B.</p>
<pre><code>-- All combinations of account type and branch region (small reference tables only)
SELECT p.ProductName, b.BranchName
FROM AccountProduct p
CROSS JOIN Branch b;</code></pre>
<p><strong>Real-time scenario:</strong> Generate a product eligibility matrix for a report (every loan product × every branch region). Use only on small tables — accidental CROSS JOIN on large tables causes performance disasters.</p>
<h3>6. SELF JOIN</h3>
<p><strong>Meaning:</strong> Joins a table <strong>to itself</strong> using two aliases — common for hierarchies or comparing rows in the same table.</p>
<pre><code>-- Bank employee and their manager (same Employee table)
SELECT
    e.Name AS Employee,
    m.Name AS Manager
FROM Employee e
LEFT JOIN Employee m ON e.ManagerId = m.EmployeeId;

-- Find duplicate account numbers entered twice (intra-table comparison)
SELECT a1.AccountNumber, a1.AccountId, a2.AccountId AS DuplicateId
FROM Account a1
INNER JOIN Account a2
    ON a1.AccountNumber = a2.AccountNumber
   AND a1.AccountId &lt; a2.AccountId;</code></pre>
<p><strong>Real-time scenario:</strong> HR org chart report (employee → manager chain) or fraud check finding duplicate account numbers created on the same day in the same branch.</p>
<h3>Which join to pick?</h3>
<table>
<tr><th>Need</th><th>Use</th></tr>
<tr><td>Only matched records</td><td>INNER JOIN</td></tr>
<tr><td>All from main table + optional detail</td><td>LEFT JOIN</td></tr>
<tr><td>Find rows missing on either side</td><td>FULL OUTER JOIN</td></tr>
<tr><td>Hierarchy or same-table compare</td><td>SELF JOIN</td></tr>
<tr><td>All combinations (small sets)</td><td>CROSS JOIN</td></tr>
</table>
<h3>Interview Answer</h3>
<p>Joins combine tables on related keys. INNER returns matches only — e.g. customers with accounts. LEFT keeps all customers even without accounts. RIGHT/FULL help reconciliation when data may exist on one side only. CROSS JOIN builds combinations on small reference data. Self join uses two aliases on one table for manager hierarchy or duplicate detection. In banking I use LEFT JOIN for CRM dashboards, INNER for statements, and FULL OUTER for CRM vs core sync.</p>""",

"q_sql_index_when_to_use": """<h2>Use of Clustered and Non-Clustered Indexes</h2>
<p>Indexes speed up <strong>reads</strong> (SELECT, JOIN, WHERE, ORDER BY) at the cost of slower <strong>writes</strong> (INSERT/UPDATE/DELETE) and extra storage.</p>
<h3>Clustered index — when to use</h3>
<ul>
<li><strong>One per table</strong> — defines physical row order.</li>
<li>Put on the column used most for <strong>range scans</strong> and sorting — often <code>PRIMARY KEY</code> (identity).</li>
<li>Good for: <code>WHERE OrderDate BETWEEN ...</code>, <code>ORDER BY OrderId</code>, sequential inserts on ID.</li>
<li>Avoid wide, random clustered keys (e.g. GUID) — causes page splits and fragmentation.</li>
</ul>
<h3>Non-clustered index — when to use</h3>
<ul>
<li>Add on columns in <strong>WHERE</strong>, <strong>JOIN</strong>, and <strong>ORDER BY</strong> that are not the clustered key.</li>
<li><strong>Covering index</strong> — INCLUDE extra columns so the query is satisfied from the index alone (no key lookup).</li>
<li>Foreign keys and highly selective filters (Status, Email, CustomerId).</li>
<li>Many allowed per table; do not over-index every column — hurts insert/update throughput.</li>
</ul>
<table>
<tr><th>Scenario</th><th>Index choice</th></tr>
<tr><td>Primary key, sequential ID</td><td>Clustered on PK</td></tr>
<tr><td>Search by email</td><td>Nonclustered on Email (often UNIQUE)</td></tr>
<tr><td>Report filter + return few columns</td><td>Nonclustered with INCLUDE</td></tr>
<tr><td>Heap table (no clustered)</td><td>Nonclustered leaf points to RID</td></tr>
</table>
<pre><code>CREATE CLUSTERED INDEX IX_Order_Date ON Orders(OrderDate);

CREATE NONCLUSTERED INDEX IX_Order_Customer
ON Orders(CustomerId)
INCLUDE (OrderDate, Total);  -- covering for common query</code></pre>
<h3>Interview Answer</h3>
<p>I use the clustered index for the main access path—usually the PK—for physical ordering. I add nonclustered indexes on filter and join columns and covering indexes when plans show expensive key lookups. I balance read speed with write overhead and validate with execution plans.</p>""",

"q_sql_profiling": """<h2>SQL Profiling — How to See It &amp; Interview Experience</h2>
<p><strong>SQL profiling</strong> means capturing what SQL Server is executing — queries, duration, reads, waits — to find slow or expensive statements.</p>
<h3>Tools in SQL Server</h3>
<table>
<tr><th>Tool</th><th>Use</th></tr>
<tr><td><strong>Actual Execution Plan</strong> (SSMS)</td><td>Per-query plan, operators, cost, missing index hints (Ctrl+M)</td></tr>
<tr><td><strong>SET STATISTICS IO, TIME ON</strong></td><td>Logical reads and elapsed time in Messages tab</td></tr>
<tr><td><strong>SQL Server Profiler</strong></td><td>Legacy trace of batches, RPCs, durations (avoid heavy traces on prod)</td></tr>
<tr><td><strong>Extended Events (XEvents)</strong></td><td>Modern, lightweight replacement for Profiler</td></tr>
<tr><td><strong>Query Store</strong></td><td>Built-in history of plans and regressions per database</td></tr>
<tr><td><strong>DMVs</strong></td><td><code>sys.dm_exec_query_stats</code>, wait stats for server-wide view</td></tr>
</table>
<h3>How to enable profiling in SSMS</h3>
<pre><code>-- Per session — before running your query
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT * FROM Orders WHERE CustomerId = 42;

-- Execution plan: Query menu → Include Actual Execution Plan
-- Or shortcut Ctrl+M</code></pre>
<h3>Extended Events (brief)</h3>
<p>Create a session for <code>sql_statement_completed</code> or <code>rpc_completed</code>, filter by duration &gt; 1000 ms, export to file or live watch in SSMS.</p>
<h3>Sample interview answer (experience)</h3>
<p>“Yes. When a stored procedure or API was slow, I captured the <strong>actual execution plan</strong> in SSMS and looked for table scans, high-cost operators, and missing index suggestions. I used <strong>STATISTICS IO/TIME</strong> to compare logical reads before and after adding an index. On servers I preferred <strong>Extended Events</strong> or <strong>Query Store</strong> over long Profiler traces to avoid overhead. I fixed issues like missing indexes on join columns, implicit conversions, and parameter sniffing after comparing plans.”</p>
<h3>What to look for in a plan</h3>
<ul>
<li>Table / clustered index <strong>scan</strong> on large tables → consider index.</li>
<li><strong>Key lookup</strong> (nested loops) → covering index may help.</li>
<li>High <strong>actual vs estimated</strong> rows → stale statistics.</li>
<li>Warnings: implicit convert, no join predicate, excessive memory grant.</li>
</ul>
<h3>Interview Answer</h3>
<p>I profile with actual execution plans and STATISTICS IO/TIME in SSMS, and on servers with Extended Events or Query Store. I trace slow queries, identify scans and expensive lookups, apply index or query fixes, and re-run the plan to confirm lower cost and reads.</p>""",

"q_sql_profiler": """<h2>SQL Profiler — Interview Questions &amp; Answers</h2>
<h3>1. What is SQL Profiler?</h3>
<p>SQL Profiler is a graphical tool in Microsoft SQL Server used to monitor and capture events from a SQL Server instance in real time. It helps with:</p>
<ul>
<li>Performance tuning</li>
<li>Query analysis</li>
<li>Detecting deadlocks</li>
<li>Identifying long-running queries</li>
<li>Troubleshooting database issues</li>
</ul>
<h3>2. What are the main uses of SQL Profiler?</h3>
<ul>
<li>Finding slow queries</li>
<li>Tracking stored procedure execution</li>
<li>Detecting blocking and deadlocks</li>
<li>Monitoring login/logout activity</li>
<li>Auditing database activity</li>
<li>Capturing queries generated by applications</li>
</ul>
<h3>3. Which events are commonly monitored?</h3>
<ul>
<li><code>SQL:BatchCompleted</code> / <code>SQL:BatchStarting</code></li>
<li><code>RPC:Completed</code></li>
<li><code>SP:Completed</code></li>
<li><code>Deadlock Graph</code></li>
<li><code>ExistingConnection</code></li>
<li><code>Login</code> / <code>Logout</code></li>
<li>Exception events</li>
</ul>
<h3>4. SQL:BatchCompleted vs RPC:Completed</h3>
<table>
<tr><th>Event</th><th>Meaning</th></tr>
<tr><td><strong>SQL:BatchCompleted</strong></td><td>Captures ad-hoc SQL queries</td></tr>
<tr><td><strong>RPC:Completed</strong></td><td>Captures stored procedure executions</td></tr>
</table>
<pre><code>SELECT * FROM Employees        -- SQL:BatchCompleted
EXEC GetEmployees              -- RPC:Completed</code></pre>
<h3>5. How do you identify slow queries?</h3>
<p>Use columns: <strong>Duration</strong>, <strong>CPU</strong>, <strong>Reads</strong>, <strong>Writes</strong>. Sort by highest Duration or Reads. Filter:</p>
<pre><code>Duration &gt; 1000 ms</code></pre>
<h3>6. What is Duration?</h3>
<p>Total execution time of a query/event. Older Profiler versions: <strong>microseconds</strong>. Newer versions: often displayed as <strong>milliseconds</strong> — confirm your SSMS/SQL Server version when comparing.</p>
<h3>7. How can SQL Profiler affect performance?</h3>
<p>Tracing consumes server resources. Heavy traces with many events, large text columns, or long production runs can slow SQL Server.</p>
<p><strong>Best practice:</strong> use filters, capture only required events, avoid heavy traces on production.</p>
<h3>8. SQL Profiler vs Extended Events</h3>
<table>
<tr><th>SQL Profiler</th><th>Extended Events</th></tr>
<tr><td>Older tool</td><td>Modern lightweight monitoring</td></tr>
<tr><td>Higher overhead</td><td>Lower overhead</td></tr>
<tr><td>GUI-based</td><td>More scalable</td></tr>
<tr><td>Being phased out</td><td>Recommended by Microsoft</td></tr>
</table>
<h3>9. How do you capture deadlocks?</h3>
<p>Enable <strong>Deadlock Graph</strong> event. Captures processes involved, locked resources, and victim process — useful for concurrency troubleshooting.</p>
<h3>10. What filters can be applied?</h3>
<p>Common filters: <code>DatabaseName</code>, <code>LoginName</code>, <code>ApplicationName</code>, <code>HostName</code>, <code>Duration</code>, <code>TextData</code>.</p>
<pre><code>DatabaseName = 'HRDB'
Duration &gt; 5000</code></pre>
<h3>11. How do you trace a query from a specific application?</h3>
<p>Filter on <code>ApplicationName</code>, e.g. <code>ApplicationName = '.Net SqlClient Data Provider'</code>.</p>
<h3>12. What is Replay in SQL Profiler?</h3>
<p>Replay allows captured SQL events to be replayed against SQL Server for load testing, reproducing issues, and performance testing.</p>
<h3>13. How do you identify blocking?</h3>
<p>Monitor: <code>Blocked Process Report</code>, <code>Lock:Deadlock</code>, <code>Lock:Timeout</code>. Look for one SPID blocking another and long-running transactions.</p>
<h3>14. Best practices</h3>
<ul>
<li>Use filters; capture minimal events</li>
<li>Avoid long traces on production</li>
<li>Save traces to file instead of table when possible</li>
<li>Prefer Extended Events for modern monitoring</li>
</ul>
<h3>15. Scenario: Production database is slow — how do you investigate?</h3>
<ol>
<li>Start a new trace</li>
<li>Capture <code>RPC:Completed</code> and <code>SQL:BatchCompleted</code></li>
<li>Include Duration, CPU, Reads, Writes</li>
<li>Filter <code>Duration &gt; 1000 ms</code></li>
<li>Identify slow queries, excessive reads, blocking/deadlocks</li>
<li>Tune with indexing, execution plans, query optimization</li>
</ol>
<h3>Rapid-fire Q&amp;A</h3>
<table>
<tr><th>Question</th><th>Answer</th></tr>
<tr><td>Can Profiler capture SELECT queries?</td><td>Yes</td></tr>
<tr><td>Can Profiler capture stored procedures?</td><td>Yes — RPC events</td></tr>
<tr><td>Profiler or Extended Events?</td><td>Extended Events (modern choice)</td></tr>
<tr><td>Is Profiler lightweight?</td><td>No — can create overhead</td></tr>
<tr><td>Monitor deadlocks?</td><td>Yes — Deadlock Graph</td></tr>
<tr><td>Filter by database?</td><td>Yes — DatabaseName filter</td></tr>
<tr><td>Run remotely?</td><td>Yes</td></tr>
<tr><td>Expensive query columns?</td><td>Duration, CPU, Reads</td></tr>
<tr><td>Show execution plans?</td><td>Indirectly — Showplan events</td></tr>
<tr><td>Is Profiler deprecated?</td><td>Microsoft recommends Extended Events going forward</td></tr>
</table>
<h3>Interview Answer</h3>
<p>I use SQL Profiler (or prefer Extended Events on modern servers) to capture RPC and batch completions, filter by duration and database, and sort on Duration/Reads to find slow queries and deadlocks. I use filters and short traces to limit overhead, then fix with indexes and execution plan analysis.</p>""",

"q_sql_opt_techniques_list": """<h2>SQL Server Optimization Techniques (5–7 Ways)</h2>
<p>Top techniques I use to improve SQL Server performance — always <strong>measure first</strong> (plan, duration, IO), then apply fixes.</p>
<ol>
<li><strong>Proper indexing</strong> — nonclustered indexes on WHERE/JOIN/ORDER BY; covering indexes with INCLUDE; one sensible clustered key (often PK).</li>
<li><strong>Update statistics</strong> — keep optimizer estimates accurate (<code>UPDATE STATISTICS</code>, auto stats, Query Store for regressions).</li>
<li><strong>Rewrite inefficient SQL</strong> — avoid <code>SELECT *</code>, non-sargable functions on columns, correlated subqueries; use EXISTS/JOINs and filter early.</li>
<li><strong>Read execution plans</strong> — fix scans, key lookups, implicit conversions, bad joins; use missing-index hints as starting points only.</li>
<li><strong>Reduce locking &amp; blocking</strong> — shorter transactions, right isolation level, READ COMMITTED SNAPSHOT where appropriate.</li>
<li><strong>Partition &amp; archive data</strong> — smaller hot working set, partition large tables by date, move history to archive tables.</li>
<li><strong>Hardware &amp; configuration</strong> — enough memory for buffer pool, fast disks for log/data, MAXDOP/Cost Threshold for Parallelism tuned for workload.</li>
</ol>
<h3>Bonus techniques</h3>
<ul>
<li>Parameterized queries / avoid plan cache pollution.</li>
<li>Tempdb tuning for heavy sorts/hashes.</li>
<li>Caching at app layer (Redis) for read-heavy reference data.</li>
</ul>
<h3>Interview Answer</h3>
<p>I list indexing, current statistics, query rewrites, plan analysis, shorter transactions, data archiving, and server tuning as my main levers. I pick based on what the plan and IO stats show—not by adding indexes everywhere.</p>""",

"q_sql_5th_rank_cte": """<h2>Find 5th Highest Rank Using RANK and CTE</h2>
<p>Use a <strong>CTE</strong> with <strong>RANK()</strong> (or <strong>DENSE_RANK()</strong> if you want 5th distinct value without gaps) over salaries, then filter <code>rnk = 5</code>.</p>
<h3>Using RANK (gaps after ties — Olympic style)</h3>
<pre><code>WITH SalaryRank AS (
    SELECT
        EmployeeId,
        Name,
        Salary,
        RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employees
)
SELECT EmployeeId, Name, Salary, rnk
FROM SalaryRank
WHERE rnk = 5;</code></pre>
<p>If two employees tie for 4th, next rank is 6 — so <code>rnk = 5</code> may return no rows.</p>
<h3>Using DENSE_RANK (no gaps — 5th distinct salary)</h3>
<pre><code>WITH SalaryRank AS (
    SELECT
        EmployeeId,
        Name,
        Salary,
        DENSE_RANK() OVER (ORDER BY Salary DESC) AS drnk
    FROM Employees
)
SELECT EmployeeId, Name, Salary, drnk
FROM SalaryRank
WHERE drnk = 5;</code></pre>
<h3>Return only the 5th highest salary value</h3>
<pre><code>WITH DistinctSalaries AS (
    SELECT DISTINCT Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS drnk
    FROM Employees
)
SELECT Salary AS FifthHighestSalary
FROM DistinctSalaries
WHERE drnk = 5;</code></pre>
<h3>Interview Answer</h3>
<p>I wrap the table in a CTE, apply RANK or DENSE_RANK over ORDER BY Salary DESC, and SELECT WHERE rank = 5. I clarify whether ties should skip ranks (RANK) or not (DENSE_RANK) before choosing the function.</p>""",

"q_sql_concurrent_update_conflict": """<h2>Two Users Update Same Data — Who Was First?</h2>
<p>When two people edit the same row, the <strong>first COMMIT wins</strong>. The second update must detect that data changed and return a friendly “already updated” message — not overwrite silently.</p>
<h3>Pattern: rowversion / timestamp token</h3>
<pre><code>CREATE TABLE Orders (
    OrderId    INT PRIMARY KEY,
    Status     NVARCHAR(20),
    Amount     DECIMAL(18,2),
    RowVer     ROWVERSION   -- auto-updates on every change
);

-- User A reads at 10:00
SELECT OrderId, Status, Amount, RowVer FROM Orders WHERE OrderId = 1;
-- RowVer = 0x00000000000007D1

-- User B reads same row, updates first at 10:01 — succeeds
UPDATE Orders SET Status = 'Shipped', Amount = 500
WHERE OrderId = 1;
-- RowVer changes to 0x00000000000007D2

-- User A tries at 10:02 with OLD RowVer — must fail
UPDATE Orders
SET Status = 'Approved', Amount = 450
WHERE OrderId = 1 AND RowVer = 0x00000000000007D1;
-- @@ROWCOUNT = 0 → someone else updated first</code></pre>
<h3>Application logic (.NET / API)</h3>
<pre><code>// On save, include original RowVer from when user opened the form
var rows = await _db.Database.ExecuteSqlRawAsync(
    @"UPDATE Orders SET Status = {0}, Amount = {1}
      WHERE OrderId = {2} AND RowVer = {3}",
    status, amount, orderId, originalRowVer);

if (rows == 0)
    return Conflict("Sorry, this record was already updated by another user. Please refresh.");</code></pre>
<h3>How you know who was first</h3>
<ul>
<li><strong>First commit</strong> succeeds and bumps <code>ROWVERSION</code> / <code>LastModifiedUtc</code>.</li>
<li><strong>Second update</strong> affects 0 rows when WHERE includes old token → tell user to refresh.</li>
<li>Optional audit table: <code>UpdatedBy</code>, <code>UpdatedAt</code> shows who won.</li>
</ul>
<h3>Interview Answer</h3>
<p>I store a concurrency token (ROWVERSION or LastModified). On update, the WHERE clause includes the token the user read. If no rows updated, the second person gets a 409 Conflict message to refresh — the first commit already changed the row.</p>""",

"q_sql_optimistic_concurrency": """<h2>Optimistic Concurrency — What It Is &amp; How to Use It</h2>
<p><strong>Optimistic concurrency</strong> assumes conflicts are <strong>rare</strong>: users read data without long locks; at <strong>save time</strong> the app checks whether the row still matches what they read. If not, the update fails and the user refreshes.</p>
<h3>Optimistic vs pessimistic</h3>
<table>
<tr><th></th><th>Optimistic</th><th>Pessimistic</th></tr>
<tr><td>Locks while reading?</td><td>No — read freely</td><td>Yes — UPDLOCK, HOLDLOCK</td></tr>
<tr><td>Conflict detection</td><td>At UPDATE (token / version)</td><td>Blocked until lock released</td></tr>
<tr><td>Best for</td><td>Web apps, low collision rate</td><td>High contention, banking counters</td></tr>
</table>
<h3>How to implement in SQL Server</h3>
<ol>
<li>Add <code>ROWVERSION</code> column (or <code>LastModified</code> datetime + user id).</li>
<li>Client reads row <strong>including token</strong> when opening edit screen.</li>
<li>On UPDATE/DELETE, include token in WHERE: <code>WHERE Id = @id AND RowVer = @oldVer</code>.</li>
<li>If <code>@@ROWCOUNT = 0</code>, throw concurrency exception → “Data was modified by another user.”</li>
</ol>
<pre><code>UPDATE Products
SET Name = @name, Price = @price
WHERE ProductId = @id AND RowVer = @rowVerFromClient;

IF @@ROWCOUNT = 0
    RAISERROR('Concurrency conflict', 16, 1);</code></pre>
<h3>Entity Framework Core</h3>
<pre><code>public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    [Timestamp]
    public byte[] RowVersion { get; set; } = null!;
}

// SaveChanges throws DbUpdateConcurrencyException on conflict
try { await _db.SaveChangesAsync(); }
catch (DbUpdateConcurrencyException)
{
    return Conflict("Record already updated. Please reload.");
}</code></pre>
<h3>SQL Server isolation note</h3>
<p>Optimistic concurrency is an <strong>application pattern</strong>; it works with default READ COMMITTED. It is different from <strong>SNAPSHOT</strong> isolation but often used together in OLTP apps.</p>
<h3>Interview Answer</h3>
<p>Optimistic concurrency means no locks during read; on save I compare a rowversion or timestamp token. If the row changed, UPDATE affects zero rows and I return a conflict to the second user. In EF Core I use a [Timestamp] property and handle DbUpdateConcurrencyException.</p>""",
}
