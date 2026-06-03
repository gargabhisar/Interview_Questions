ANSWERS = {
"q_sql_views_vs_indexes": """<h2>Views vs Indexes in SQL Server</h2>
<p><strong>Views</strong> and <strong>indexes</strong> solve different problems — they are not alternatives. A view is a saved query (virtual table); an index is a physical access structure that speeds up data retrieval.</p>
<table>
<tr><th></th><th>View</th><th>Index</th></tr>
<tr><td>What it is</td><td>Named SELECT stored in metadata</td><td>B-tree (or specialized) structure on table columns</td></tr>
<tr><td>Stores data?</td><td>No (usually*) — reads underlying tables</td><td>Yes — index pages separate from heap/clustered data</td></tr>
<tr><td>Purpose</td><td>Simplify queries, security, abstraction</td><td>Faster seeks/scans, enforce uniqueness</td></tr>
<tr><td>Write impact</td><td>Simple views can be updatable; complex ones are read-only</td><td>Slows INSERT/UPDATE/DELETE (index maintenance)</td></tr>
<tr><td>Example</td><td><code>CREATE VIEW vw_ActiveEmployees AS ...</code></td><td><code>CREATE INDEX IX_Emp_Dept ON Employees(DeptId)</code></td></tr>
</table>
<p>*Indexed views (materialized with schema binding) are a special case — SQL Server can persist the result for performance.</p>
<pre><code>-- View: reusable query definition
CREATE VIEW vw_SalesSummary AS
SELECT Region, SUM(Amount) AS Total
FROM Sales
GROUP BY Region;

-- Index: speeds up filter/join on Employees.DeptId
CREATE NONCLUSTERED INDEX IX_Emp_DeptId ON Employees(DeptId);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Views improve readability and hide complexity; they do not replace indexes for performance.</li>
<li>Put indexes on columns used in WHERE, JOIN, ORDER BY — validate with execution plans.</li>
<li>Indexed views can help heavy aggregations but have strict creation rules.</li>
</ul>
<h3>Interview Answer</h3>
<p>A view is a stored query that presents data like a virtual table; an index is a physical structure that speeds up lookups on a table. I use views for security and simplified reporting, and indexes on real tables to fix slow queries — they complement each other, not replace each other.</p>""",

"q_sql_what_is_sp": """<h2>What is a Stored Procedure (SP)?</h2>
<p>A <strong>stored procedure</strong> is a precompiled batch of T-SQL statements saved in the database and executed by name. It can accept parameters, perform DML, contain business logic, transactions, and return result sets or status codes.</p>
<pre><code>CREATE PROCEDURE dbo.GetEmployeesByDept
    @DeptId INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT EmployeeId, Name, Salary
    FROM Employees
    WHERE DeptId = @DeptId
    ORDER BY Name;
END;

-- Execute
EXEC dbo.GetEmployeesByDept @DeptId = 3;</code></pre>
<h3>Why use stored procedures?</h3>
<ul>
<li><strong>Encapsulation</strong> — business rules live in one place close to data.</li>
<li><strong>Security</strong> — grant EXEC without exposing base tables.</li>
<li><strong>Performance</strong> — execution plan reuse; less network round trips.</li>
<li><strong>Maintenance</strong> — change logic once without redeploying every client app.</li>
</ul>
<h3>SP vs ad-hoc SQL</h3>
<table>
<tr><th>Stored Procedure</th><th>Ad-hoc SQL</th></tr>
<tr><td>Named object in DB</td><td>Sent as text each time</td></tr>
<tr><td>Can use transactions, branching, error handling</td><td>Same possible but scattered in app</td></tr>
<tr><td>Parameterised by default</td><td>Risk of SQL injection if concatenated</td></tr>
</table>
<h3>Interview Answer</h3>
<p>A stored procedure is a named, reusable T-SQL program stored in the database. I use SPs to encapsulate data access and business rules, improve security via EXEC permissions, and reduce round trips. Parameters are passed at runtime with EXEC or from ADO.NET/EF raw SQL.</p>""",

"q_sql_where_having": """<h2>WHERE vs HAVING in SQL</h2>
<p>Both filter rows, but at <strong>different stages</strong> of query execution. <code>WHERE</code> filters rows <strong>before</strong> grouping; <code>HAVING</code> filters groups <strong>after</strong> <code>GROUP BY</code>.</p>
<table>
<tr><th></th><th>WHERE</th><th>HAVING</th></tr>
<tr><td>Filters</td><td>Individual rows</td><td>Grouped aggregates</td></tr>
<tr><td>Used with</td><td>SELECT, UPDATE, DELETE</td><td>SELECT with GROUP BY</td></tr>
<tr><td>Aggregate functions?</td><td>Cannot filter on SUM/COUNT directly*</td><td>Can filter on SUM/COUNT/AVG</td></tr>
<tr><td>Order in query</td><td>Before GROUP BY</td><td>After GROUP BY</td></tr>
</table>
<p>*Use a subquery or HAVING if you need to filter on an aggregate.</p>
<pre><code>-- WHERE: filter rows before grouping
SELECT DeptId, COUNT(*) AS EmpCount
FROM Employees
WHERE Salary &gt; 50000          -- row filter
GROUP BY DeptId;

-- HAVING: filter groups after aggregation
SELECT DeptId, COUNT(*) AS EmpCount
FROM Employees
GROUP BY DeptId
HAVING COUNT(*) &gt; 5;          -- group filter

-- Both together
SELECT DeptId, AVG(Salary) AS AvgSal
FROM Employees
WHERE IsActive = 1            -- rows first
GROUP BY DeptId
HAVING AVG(Salary) &gt; 60000;   -- groups second</code></pre>
<h3>Key Points</h3>
<ul>
<li>WHERE cannot reference aggregate aliases from SELECT — HAVING can use aggregates.</li>
<li>Filter individual rows with WHERE; filter summary results with HAVING.</li>
<li>Using HAVING where WHERE suffices is slower — filter early when possible.</li>
</ul>
<h3>Interview Answer</h3>
<p>WHERE filters rows before grouping; HAVING filters after GROUP BY on aggregated results. I use WHERE for column conditions on raw rows and HAVING when the condition involves COUNT, SUM, or AVG of a group.</p>""",

"q_sql_function_return_types": """<h2>SQL Functions — Can They Have Multiple Return Types?</h2>
<p><strong>No</strong> — a single SQL Server function has <strong>one declared return type</strong> (scalar type or one table structure). You cannot return sometimes an int and sometimes a varchar from the same function.</p>
<h3>Function types in SQL Server</h3>
<table>
<tr><th>Type</th><th>Returns</th><th>Example</th></tr>
<tr><td>Scalar function</td><td>One value (INT, VARCHAR, etc.)</td><td><code>RETURNS INT</code></td></tr>
<tr><td>Inline table-valued (ITVF)</td><td>One table shape via SELECT</td><td><code>RETURNS TABLE AS RETURN ...</code></td></tr>
<tr><td>Multi-statement TVF (MSTVF)</td><td>One table variable shape</td><td><code>RETURNS @t TABLE (...)</code></td></tr>
</table>
<pre><code>-- Scalar — single INT return
CREATE FUNCTION dbo.GetBonus(@Sal DECIMAL(10,2))
RETURNS DECIMAL(10,2)
AS BEGIN
    RETURN @Sal * 0.10;
END;

-- Inline TVF — always same column set
CREATE FUNCTION dbo.ActiveEmployees(@DeptId INT)
RETURNS TABLE
AS RETURN (
    SELECT EmployeeId, Name FROM Employees
    WHERE DeptId = @DeptId AND IsActive = 1
);</code></pre>
<h3>What if you need different shapes?</h3>
<ul>
<li>Create <strong>separate functions</strong> for different return structures.</li>
<li>Use a <strong>stored procedure</strong> with multiple result sets (not ideal for queries).</li>
<li>Return a <strong>JSON</strong> or <strong>XML</strong> scalar for flexible payloads (SQL Server 2016+).</li>
<li>Use optional columns with NULLs in one consistent table shape.</li>
</ul>
<h3>Interview Answer</h3>
<p>A function has one return type — scalar or a fixed table definition. It cannot dynamically switch return types. For varying outputs I use separate functions, stored procedures, or return JSON from a scalar function when flexibility is required.</p>""",

"q_sql_commission_null": """<h2>Query: If Commission Is NULL, Return 0</h2>
<p>Use <code>ISNULL</code>, <code>COALESCE</code>, or <code>NULLIF</code> patterns to replace NULL with a default in SELECT expressions.</p>
<pre><code>-- ISNULL (SQL Server) — two arguments
SELECT
    EmployeeId,
    Name,
    ISNULL(Commission, 0) AS Commission
FROM Employees;

-- COALESCE — standard SQL, supports multiple fallbacks
SELECT
    EmployeeId,
    Name,
    COALESCE(Commission, 0) AS Commission
FROM Employees;

-- In calculations — NULL poisons math without handling
SELECT
    Name,
    Salary + ISNULL(Commission, 0) AS TotalPay
FROM Employees;

-- WHERE still needs care: NULL = 0 is UNKNOWN
SELECT * FROM Employees
WHERE ISNULL(Commission, 0) = 0;  -- includes NULL and explicit 0</code></pre>
<h3>ISNULL vs COALESCE</h3>
<table>
<tr><th>ISNULL</th><th>COALESCE</th></tr>
<tr><td>Two arguments only</td><td>Multiple arguments</td></tr>
<tr><td>SQL Server specific</td><td>ANSI standard</td></tr>
<tr><td>Always converts to first non-null type</td><td>Evaluates until first non-null</td></tr>
</table>
<h3>Interview Answer</h3>
<p>I wrap the column with ISNULL(Commission, 0) or COALESCE(Commission, 0) in the SELECT list so NULL displays as zero. For totals I apply the same before adding to Salary because NULL plus any number stays NULL in SQL.</p>""",

"q_sql_5th_highest_salary": """<h2>Get 5th Highest Salary</h2>
<p>Rank salaries descending and filter where rank equals 5. Clarify whether ties count as separate ranks (ROW_NUMBER) or shared ranks (DENSE_RANK).</p>
<h3>Method 1 — DENSE_RANK (5th distinct salary)</h3>
<pre><code>SELECT Salary
FROM (
    SELECT Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS dr
    FROM Employees
) t
WHERE dr = 5;</code></pre>
<h3>Method 2 — ROW_NUMBER (5th row regardless of ties)</h3>
<pre><code>SELECT Salary
FROM (
    SELECT Salary,
           ROW_NUMBER() OVER (ORDER BY Salary DESC) AS rn
    FROM Employees
) t
WHERE rn = 5;</code></pre>
<h3>Method 3 — OFFSET (SQL Server 2012+)</h3>
<pre><code>SELECT DISTINCT Salary
FROM Employees
ORDER BY Salary DESC
OFFSET 4 ROWS FETCH NEXT 1 ROW ONLY;
-- skips 4 rows, returns 5th distinct value</code></pre>
<h3>Key Points</h3>
<ul>
<li>OFFSET 4 = skip first four — returns the 5th highest distinct salary.</li>
<li>DENSE_RANK skips no numbers when salaries tie; ROW_NUMBER assigns unique ranks.</li>
<li>Index on <code>Salary DESC</code> helps on large tables.</li>
</ul>
<h3>Interview Answer</h3>
<p>For 5th highest salary I use DENSE_RANK or ROW_NUMBER over ORDER BY Salary DESC in a subquery and filter rank = 5, or OFFSET 4 ROWS FETCH NEXT 1 ROW ONLY on distinct salaries. I confirm whether ties should share the same rank before picking the function.</p>""",

"q_sql_dept_zero_employees": """<h2>Department with 0 Employees</h2>
<p>Find departments that exist in a master table but have no matching employees — classic <strong>LEFT JOIN</strong> with NULL check or <strong>NOT EXISTS</strong>.</p>
<pre><code>-- LEFT JOIN — departments with no employees
SELECT d.DeptId, d.DeptName
FROM Departments d
LEFT JOIN Employees e ON e.DeptId = d.DeptId
WHERE e.EmployeeId IS NULL;

-- NOT EXISTS — often efficient with index on Employees.DeptId
SELECT d.DeptId, d.DeptName
FROM Departments d
WHERE NOT EXISTS (
    SELECT 1 FROM Employees e
    WHERE e.DeptId = d.DeptId
);

-- EXCEPT (if you only have employee dept ids)
SELECT DeptId FROM Departments
EXCEPT
SELECT DISTINCT DeptId FROM Employees WHERE DeptId IS NOT NULL;</code></pre>
<h3>Opposite — departments WITH employees</h3>
<pre><code>SELECT DISTINCT d.DeptId, d.DeptName
FROM Departments d
INNER JOIN Employees e ON e.DeptId = d.DeptId;</code></pre>
<h3>Key Points</h3>
<ul>
<li>LEFT JOIN + <code>WHERE right.key IS NULL</code> is the standard anti-join pattern.</li>
<li>NOT EXISTS often performs well and reads clearly for "no matching rows."</li>
<li>Index on <code>Employees(DeptId)</code> speeds the lookup.</li>
</ul>
<h3>Interview Answer</h3>
<p>I LEFT JOIN Departments to Employees and filter where EmployeeId IS NULL, or use NOT EXISTS on Employees for that DeptId. Both return departments with zero employees; I pick based on readability and the execution plan.</p>""",

"q_sql_missing_index": """<h2>How to Identify a Missing Index in SQL Server</h2>
<p>Start with a slow query's <strong>execution plan</strong>, then confirm with <strong>DMVs</strong> and missing-index suggestions — but always test before creating indexes blindly.</p>
<h3>1. Execution plan (SSMS)</h3>
<ul>
<li>Enable <strong>Actual Execution Plan</strong> (Ctrl+M).</li>
<li>Look for <strong>Table Scan</strong> / <strong>Clustered Index Scan</strong> on large tables.</li>
<li>Green <strong>Missing Index</strong> suggestion appears with impact % and CREATE INDEX script.</li>
</ul>
<h3>2. sys.dm_db_missing_index_* DMVs</h3>
<pre><code>SELECT
    migs.avg_user_impact,
    migs.user_seeks + migs.user_scans AS total_usage,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_groups mig
JOIN sys.dm_db_missing_index_group_stats migs
    ON mig.index_group_handle = migs.group_handle
JOIN sys.dm_db_missing_index_details mid
    ON mig.index_handle = mid.index_handle
ORDER BY migs.avg_user_impact * (migs.user_seeks + migs.user_scans) DESC;</code></pre>
<h3>3. Other signals</h3>
<ul>
<li>High logical reads in STATISTICS IO.</li>
<li>Key lookup + scan combinations on wide tables.</li>
<li>Query Store regressed plans after data growth.</li>
</ul>
<h3>Caution</h3>
<ul>
<li>Missing-index DMVs suggest — they do not account for write overhead or overlapping indexes.</li>
<li>Validate with plan before/after; drop unused indexes periodically.</li>
</ul>
<h3>Interview Answer</h3>
<p>I capture the actual execution plan and look for scans and missing-index warnings. I also query dm_db_missing_index DMVs for high-impact suggestions. Before creating an index I check write load, column selectivity, and whether a covering index is needed — then measure again.</p>""",

"q_sql_last_inserted": """<h2>Keyword to Get Last Inserted Record</h2>
<p>SQL Server provides several ways depending on whether you need the <strong>identity value</strong>, the <strong>full row</strong>, or support for <strong>multiple inserts</strong>.</p>
<table>
<tr><th>Method</th><th>Scope</th><th>When to use</th></tr>
<tr><td><code>SCOPE_IDENTITY()</code></td><td>Current session + scope</td><td><strong>Preferred</strong> after INSERT in same batch/SP</td></tr>
<tr><td><code>@@IDENTITY</code></td><td>Current session, any scope</td><td>Avoid — can return ID from trigger</td></tr>
<tr><td><code>IDENT_CURRENT('Table')</code></td><td>Any session, last on table</td><td>Not safe for concurrent inserts</td></tr>
<tr><td><code>OUTPUT INSERTED.*</code></td><td>Inserted rows in same statement</td><td>Best for multiple rows / full row data</td></tr>
</table>
<pre><code>-- SCOPE_IDENTITY — most common
INSERT INTO Employees (Name, DeptId)
VALUES ('Alice', 3);

SELECT SCOPE_IDENTITY() AS NewEmployeeId;

-- OUTPUT clause — returns full inserted row(s)
INSERT INTO Employees (Name, DeptId)
OUTPUT INSERTED.EmployeeId, INSERTED.Name
VALUES ('Bob', 5);

-- Multiple rows
INSERT INTO Orders (CustomerId, Total)
OUTPUT INSERTED.OrderId, INSERTED.Total
SELECT CustomerId, Amount FROM StagingOrders;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use <strong>SCOPE_IDENTITY()</strong> not @@IDENTITY when triggers exist on the table.</li>
<li><strong>OUTPUT</strong> is ideal when you need several columns or bulk insert IDs.</li>
<li>EF Core: <code>SaveChanges</code> populates identity on entity; raw SQL uses above.</li>
</ul>
<h3>Interview Answer</h3>
<p>After INSERT I use SCOPE_IDENTITY() to get the new identity value in the same scope — it is safer than @@IDENTITY when triggers exist. For the full inserted row or bulk inserts I use the OUTPUT INSERTED clause, which returns columns directly from the insert statement.</p>""",
}
