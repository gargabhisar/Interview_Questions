ANSWERS = {
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
}
