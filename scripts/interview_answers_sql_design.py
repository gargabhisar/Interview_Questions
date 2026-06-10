ANSWERS = {
"q_1": """<h2>MongoDB vs SQL Databases</h2>
<p>SQL databases are relational, schema-first systems that store data in tables with enforced relationships and ACID transactions. MongoDB is a document-oriented NoSQL database that stores flexible JSON-like BSON documents in collections, optimized for horizontal scaling and rapid schema evolution.</p>
<p>On SQL Server you also tune parallelism with <code>MAXDOP</code> (maximum degree of parallelism), which limits how many CPUs a single query may use—separate from the SQL vs document-store choice but important for relational performance.</p>
<table>
<tr><th>Aspect</th><th>SQL</th><th>MongoDB</th></tr>
<tr><td>Data model</td><td>Tables, rows, columns</td><td>Collections, documents</td></tr>
<tr><td>Schema</td><td>Fixed, enforced</td><td>Flexible, optional</td></tr>
<tr><td>Scaling</td><td>Mostly vertical</td><td>Horizontal sharding</td></tr>
<tr><td>Joins</td><td>Native JOINs</td><td>Embedding or $lookup</td></tr>
</table>
<pre><code>-- SQL: normalized order query
SELECT o.OrderId, c.Name
FROM Orders o
JOIN Customers c ON o.CustomerId = c.Id;

-- MongoDB: embedded or lookup
db.orders.aggregate([
  { $lookup: { from: "customers", localField: "customerId",
      foreignField: "_id", as: "customer" } }
]);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Choose SQL when you need strong consistency, complex joins, and reporting.</li>
<li>Choose MongoDB for flexible schemas, high write throughput, and document-centric apps.</li>
<li>Many teams use both: SQL for transactional core, MongoDB for logs or content.</li>
</ul>
<h3>Interview Answer</h3>
<p>SQL is relational and ACID-focused with strict schemas; MongoDB is document-based and schema-flexible, better for scale-out and evolving data shapes. I pick based on consistency needs, query patterns, and team expertise—not hype.</p>""",

"q_5": """<h2>Database Normalization &amp; Its Forms (1NF, 2NF, 3NF)</h2>
<blockquote>
<p>“Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity.</p>
<p>The main goal is:</p>
<ul>
<li>avoiding duplicate data,</li>
<li>preventing update/delete anomalies,</li>
<li>and making the database more maintainable and efficient.</li>
</ul>
<p>In real-world systems like banking applications at <strong>PNC</strong>, normalization is very important because customer and transaction data are huge and frequently updated.”</p>
</blockquote>
<h3>PNC banking example — the problem</h3>
<p>“Suppose we have a banking table like this:”</p>
<table>
<tr><th>CustomerID</th><th>CustomerName</th><th>AccountNumber</th><th>BranchName</th></tr>
<tr><td>101</td><td>John</td><td>9001</td><td>New York</td></tr>
<tr><td>101</td><td>John</td><td>9002</td><td>New York</td></tr>
</table>
<p>Customer and branch information are <strong>repeated</strong>. This causes:</p>
<ul>
<li>storage wastage</li>
<li>inconsistency</li>
<li>update anomalies — if branch name changes, we must update multiple rows</li>
</ul>
<h3>How you normalize it</h3>
<p>“Instead of keeping everything in one table, we divide it into separate entities.”</p>
<pre><code>Customers
-----------
CustomerID
CustomerName

Accounts
-----------
AccountNumber
CustomerID      -- FK → Customers
BranchID        -- FK → Branches

Branches
-----------
BranchID
BranchName</code></pre>
<p>Now customer data is stored <strong>once</strong>, branch data is stored <strong>once</strong>, and relationships are maintained using <strong>foreign keys</strong>.</p>
<h3>Normal forms — step by step (same PNC example)</h3>
<p>Walk through <strong>1NF → 2NF → 3NF</strong> on the same banking data so the story stays consistent on a Teams call.</p>
<h4>1NF — First Normal Form</h4>
<p>“First Normal Form ensures <strong>atomic values</strong> and removes repeating groups.”</p>
<p><strong>Before 1NF</strong> — multiple account numbers in one cell (repeating group):</p>
<table>
<tr><th>CustomerID</th><th>CustomerName</th><th>AccountNumbers</th><th>BranchName</th></tr>
<tr><td>101</td><td>John</td><td>9001, 9002</td><td>New York</td></tr>
</table>
<p><strong>After 1NF</strong> — one value per column; one row per account:</p>
<table>
<tr><th>CustomerID</th><th>CustomerName</th><th>AccountNumber</th><th>BranchName</th></tr>
<tr><td>101</td><td>John</td><td>9001</td><td>New York</td></tr>
<tr><td>101</td><td>John</td><td>9002</td><td>New York</td></tr>
</table>
<pre><code>-- Or split into an Accounts table (still 1NF):
Customers(CustomerID, CustomerName)
Accounts(AccountNumber, CustomerID, BranchName)</code></pre>
<h4>2NF — Second Normal Form</h4>
<p>“Second Normal Form removes <strong>partial dependency</strong>. If we have a composite key, every non-key column must depend on the <strong>whole</strong> key—not just part of it.”</p>
<p><strong>Before 2NF</strong> — composite PK <code>(CustomerID, AccountNumber)</code> but <code>CustomerName</code> depends only on <code>CustomerID</code>:</p>
<pre><code>AccountRegister(CustomerID, AccountNumber, CustomerName, BranchName)
PK = (CustomerID, AccountNumber)
-- CustomerName → CustomerID only  (partial dependency)</code></pre>
<p><strong>After 2NF</strong> — move customer name to its own table:</p>
<pre><code>Customers(CustomerID PK, CustomerName)
Accounts(AccountNumber PK, CustomerID FK, BranchName)
-- CustomerName stored once; no partial dependency on composite key</code></pre>
<h4>3NF — Third Normal Form</h4>
<p>“Third Normal Form removes <strong>transitive dependency</strong>. A non-key column must not depend on another non-key column.”</p>
<p><strong>Before 3NF</strong> — <code>BranchName</code> depends on branch, not on <code>AccountNumber</code>, but is stored on every account row:</p>
<pre><code>Accounts(AccountNumber PK, CustomerID FK, BranchName)
-- AccountNumber → BranchName is transitive (branch is its own entity)</code></pre>
<p><strong>After 3NF</strong> — branch facts live in <code>Branches</code>; accounts reference <code>BranchID</code>:</p>
<pre><code>Customers(CustomerID PK, CustomerName)
Branches(BranchID PK, BranchName, City, State)
Accounts(AccountNumber PK, CustomerID FK, BranchID FK)

-- Final result: customer once, branch once, FKs link accounts</code></pre>
<h3>Quick reference</h3>
<table>
<tr><th>Form</th><th>Rule</th><th>Fixes</th></tr>
<tr><td><strong>1NF</strong></td><td>Atomic values; no repeating groups</td><td>Multi-valued columns</td></tr>
<tr><td><strong>2NF</strong></td><td>1NF + no partial dependency on composite key</td><td>Non-key depends on part of key only</td></tr>
<tr><td><strong>3NF</strong></td><td>2NF + no transitive dependency</td><td>Non-key depends on another non-key</td></tr>
</table>
<h3>Anomalies normalization prevents</h3>
<table>
<tr><th>Anomaly</th><th>PNC example</th></tr>
<tr><td><strong>Insert</strong></td><td>Cannot add a branch until a customer opens an account there</td></tr>
<tr><td><strong>Update</strong></td><td>Branch renamed “New York Downtown”—must update every account row</td></tr>
<tr><td><strong>Delete</strong></td><td>Closing last account loses customer name stored only in that row</td></tr>
</table>
<h3>Practical tradeoff (sounds experienced)</h3>
<blockquote>
<p>“In highly transactional systems like banking, we generally <strong>normalize OLTP databases</strong> for consistency. However, sometimes <strong>partial denormalization</strong> is also used in reporting systems for faster reads.”</p>
</blockquote>
<p>Reporting/data warehouse layers often use star schemas; denormalize only after measuring—keep the core banking OLTP normalized.</p>
<h3>Short version (if interviewer wants a quick answer)</h3>
<blockquote>
<p>“Normalization is organizing database tables to reduce redundancy and maintain data integrity. We achieve this by splitting large tables into related smaller tables using primary and foreign keys. Common normal forms are 1NF, 2NF, and 3NF. For example, in a banking system, customer, account, and branch data are stored separately instead of duplicating them in one table.”</p>
</blockquote>
<h3>Tips for Teams call delivery</h3>
<ul>
<li><strong>Speak slowly</strong> — don’t rush definitions</li>
<li><strong>Draw structure verbally</strong> — “Imagine we have one table…” keeps the interviewer engaged</li>
<li><strong>Use business examples</strong> — banking (PNC) sounds stronger than generic student/course</li>
<li><strong>Problem + solution</strong> — always explain what issue exists and how normalization fixes it</li>
</ul>
<h3>Golden closing line</h3>
<blockquote>
<p>“So normalization helps in creating scalable, maintainable, and consistent database systems, especially in enterprise applications like banking.”</p>
</blockquote>
<h3>Interview Answer</h3>
<p>Normalization organizes data to cut redundancy and protect integrity—critical at PNC-scale banking where customers and transactions change constantly. I walk through a bad single-table design, split into Customers, Accounts, and Branches with FKs, then explain 1NF/2NF/3NF. I close by noting OLTP stays normalized while reporting may denormalize for read performance.</p>""",

"q_6": """<h2>Boyce-Codd Normal Form (BCNF)</h2>
<p>BCNF is a stricter form of 3NF: every determinant must be a candidate key. A table is in BCNF when for every functional dependency X → Y, X is a superkey. It eliminates anomalies 3NF might still allow when multiple overlapping candidate keys exist.</p>
<p>When a non-key attribute determines another non-key attribute, decompose into separate tables while keeping joins lossless and preserving dependencies where possible.</p>
<pre><code>-- Violates BCNF (Teacher → Room, but Teacher is not a key):
Enrollment(Student, Course, Teacher, Room)

-- Fix: separate Teacher → Room dependency
TeacherRoom(Teacher, Room)
Enrollment(Student, Course, Teacher)</code></pre>
<h3>Key Points</h3>
<ul>
<li>BCNF ⊂ 3NF; all BCNF tables are 3NF, not vice versa.</li>
<li>Violations occur when non-key attributes determine other non-key attributes.</li>
<li>Decomposition must be lossless and preserve dependencies where possible.</li>
</ul>
<h3>Interview Answer</h3>
<p>BCNF requires every determinant to be a candidate key. If Teacher determines Room but Teacher isn't a key, I decompose into separate tables to remove the anomaly while keeping joins lossless.</p>""",

"q_7": """<h2>SQL Server Indexes</h2>
<p>Indexes are auxiliary data structures (typically B-trees) that speed up data retrieval by avoiding full table scans. They trade faster reads for extra storage and slower writes due to index maintenance.</p>
<p>Design indexes around real query patterns — filters, joins, ORDER BY, and GROUP BY — and validate with execution plans rather than indexing every column.</p>
<table>
<tr><th>Pros</th><th>Cons</th></tr>
<tr><td>Faster SELECT / WHERE / JOIN</td><td>Slower INSERT / UPDATE / DELETE</td></tr>
<tr><td>Enforces uniqueness (unique index)</td><td>Extra disk and memory</td></tr>
</table>
<h3>Clustered vs non-clustered</h3>
<p>A <strong>clustered index</strong> defines the physical sort order of table rows — there can be <strong>only one</strong> per table. A <strong>non-clustered index</strong> is a separate structure with pointers (row locators) back to the data.</p>
<table>
<tr><th>Clustered</th><th>Non-clustered</th></tr>
<tr><td>One per table (or heap if none)</td><td>Many allowed</td></tr>
<tr><td>Leaf level = data pages</td><td>Separate structure + key lookup</td></tr>
<tr><td>Default on PRIMARY KEY</td><td>Leaf points to clustered key or RID (heap)</td></tr>
<tr><td>Efficient range scans on key</td><td>May need key lookup if not covering</td></tr>
</table>
<pre><code>CREATE TABLE Employees (
    EmployeeId INT PRIMARY KEY CLUSTERED,  -- one clustered index
    DeptId INT,
    Name NVARCHAR(100)
);

CREATE NONCLUSTERED INDEX IX_Emp_Dept ON Employees(DeptId);
CREATE NONCLUSTERED INDEX IX_Emp_Name ON Employees(Name);</code></pre>
<h3>How many clustered indexes per table?</h3>
<ul>
<li><strong>0 clustered</strong> — table is a <strong>heap</strong> (unordered storage).</li>
<li><strong>1 clustered</strong> — normal case; often on PRIMARY KEY.</li>
<li><strong>2+ clustered</strong> — <strong>not allowed</strong> on one table.</li>
</ul>
<p>You can have many non-clustered indexes in practice. Non-clustered leaf nodes point to the clustered key or RID on a heap.</p>
<h3>Types of indexes in SQL Server</h3>
<p>Most OLTP work uses <strong>clustered</strong> and <strong>non-clustered</strong> B-tree indexes. SQL Server also supports specialized types:</p>
<table>
<tr><th>Type</th><th>Use case</th></tr>
<tr><td><strong>Clustered / Nonclustered</strong> (B-tree)</td><td>Everyday relational tables — OLTP lookups and joins</td></tr>
<tr><td><strong>Columnstore</strong> (clustered or nonclustered)</td><td>Data warehousing, analytics, large scans</td></tr>
<tr><td><strong>Hash</strong></td><td>Memory-optimized (In-Memory OLTP) tables — point lookups</td></tr>
<tr><td><strong>XML index</strong></td><td>XML columns (primary + PATH / VALUE / PROPERTY)</td></tr>
<tr><td><strong>Spatial index</strong></td><td>Geometry / geography columns</td></tr>
<tr><td><strong>Full-text index</strong></td><td>Word / phrase search (separate engine)</td></tr>
</table>
<p><strong>Variations:</strong> unique index, <strong>filtered (partial)</strong> index with a <code>WHERE</code> predicate, <strong>indexed view</strong> (clustered index on a view).</p>
<pre><code>-- Nonclustered + filtered + include (covering subset)
CREATE NONCLUSTERED INDEX IX_User_Active
ON dbo.[User](UserName) INCLUDE (Email)
WHERE IsActive = 1;

-- Columnstore (reporting / analytics)
CREATE CLUSTERED COLUMNSTORE INDEX CCI_Orders ON dbo.Orders;</code></pre>
<h3>When to use clustered vs non-clustered</h3>
<p><strong>Clustered index — use when:</strong></p>
<ul>
<li>Column drives most <strong>range scans</strong> and sorting — often <code>PRIMARY KEY</code> (identity).</li>
<li>Good for: <code>WHERE OrderDate BETWEEN ...</code>, <code>ORDER BY OrderId</code>, sequential inserts on ID.</li>
<li>Avoid wide, random clustered keys (e.g. GUID) — causes page splits and fragmentation.</li>
</ul>
<p><strong>Non-clustered index — use when:</strong></p>
<ul>
<li>Columns appear in <strong>WHERE</strong>, <strong>JOIN</strong>, or <strong>ORDER BY</strong> but are not the clustered key.</li>
<li>Foreign keys and selective filters (Status, Email, CustomerId).</li>
<li><strong>Covering index</strong> — INCLUDE extra columns so the query avoids key lookup (see Section 10 item 13).</li>
<li>Many allowed per table — do not over-index; hurts write-heavy OLTP.</li>
</ul>
<table>
<tr><th>Scenario</th><th>Index choice</th></tr>
<tr><td>Primary key, sequential ID</td><td>Clustered on PK</td></tr>
<tr><td>Search by email</td><td>Nonclustered on Email (often UNIQUE)</td></tr>
<tr><td>Report filter + few returned columns</td><td>Nonclustered with INCLUDE</td></tr>
<tr><td>Heap table (no clustered)</td><td>Nonclustered leaf points to RID</td></tr>
</table>
<pre><code>CREATE CLUSTERED INDEX IX_Order_Date ON Orders(OrderDate);

CREATE NONCLUSTERED INDEX IX_Order_Customer
ON Orders(CustomerId)
INCLUDE (OrderDate, Total);</code></pre>
<p><strong>Related in this section:</strong> Views vs Indexes (item 11), Missing Index (item 12), Covering Index (item 13), Index Design Strategy (item 14).</p>
<h3>Interview Answer</h3>
<p>Indexes speed up reads but slow writes. In SQL Server the clustered index defines physical row order — only one per table, usually on the PK. Non-clustered indexes are separate structures for filter and join columns; I add covering indexes with INCLUDE when plans show expensive key lookups. I also know columnstore for analytics and filtered indexes for subsets. I validate with execution plans, avoid over-indexing OLTP tables, and keep the clustered key narrow and sequential.</p>""",

"q_9": """<h2>SQL Execution Plans</h2>
<p>An execution plan shows how the optimizer retrieves data: scan vs seek, join algorithms, sort/hash operations, and estimated vs actual row counts. Reading plans is essential for performance tuning.</p>
<p>Compare estimated vs actual rows; large gaps often mean stale statistics or parameter sniffing issues.</p>
<pre><code>SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT e.Name, d.DeptName
FROM Employees e
INNER JOIN Departments d ON e.DeptId = d.DeptId
WHERE e.Salary &gt; 80000;

-- View plan in SSMS: Ctrl+M or SET SHOWPLAN_ALL ON;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Look for table/index scans on large tables—often fixable with indexes.</li>
<li>Compare estimated vs actual rows; big gaps suggest stale statistics.</li>
<li>Watch for implicit conversions, key lookups, and expensive sorts.</li>
</ul>
<h3>Interview Answer</h3>
<p>I use execution plans to see whether SQL Server scans or seeks, which joins it picks, and where cost concentrates. Red flags are scans on big tables, bad cardinality estimates, and missing indexes.</p>""",

"q_sql_constraints": """<h2>Constraints in SQL</h2>
<p><strong>Constraints</strong> are rules on tables or columns that the database enforces on INSERT/UPDATE/DELETE. They keep data valid and support ACID <strong>Consistency</strong>—invalid rows are rejected before they are stored.</p>
<table>
<tr><th>Constraint</th><th>Purpose</th></tr>
<tr><td><strong>PRIMARY KEY</strong></td><td>Uniquely identifies each row; NOT NULL; one per table (typically)</td></tr>
<tr><td><strong>FOREIGN KEY</strong></td><td>Links to parent table; prevents orphan rows (referential integrity)</td></tr>
<tr><td><strong>UNIQUE</strong></td><td>No duplicates in column(s); allows one NULL per column in SQL Server</td></tr>
<tr><td><strong>CHECK</strong></td><td>Boolean condition must be true (e.g. Age &gt;= 18)</td></tr>
<tr><td><strong>NOT NULL</strong></td><td>Column cannot store NULL</td></tr>
<tr><td><strong>DEFAULT</strong></td><td>Value used when INSERT omits the column</td></tr>
</table>
<pre><code>CREATE TABLE Orders (
    OrderId     INT NOT NULL PRIMARY KEY,
    CustomerId  INT NOT NULL,
    OrderDate   DATE NOT NULL DEFAULT GETDATE(),
    Status      VARCHAR(20) NOT NULL
        CONSTRAINT CK_Orders_Status
        CHECK (Status IN ('Pending','Shipped','Cancelled')),
    CONSTRAINT FK_Orders_Customers
        FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId)
);

CREATE TABLE Customers (
    CustomerId INT PRIMARY KEY,
    Email      NVARCHAR(256) NOT NULL UNIQUE
);</code></pre>
<h3>Foreign key actions</h3>
<ul>
<li><code>ON DELETE CASCADE</code> — delete child rows when parent is deleted.</li>
<li><code>ON DELETE SET NULL</code> — null out FK when parent is deleted.</li>
<li><code>NO ACTION</code> (default) — block delete/update if children exist.</li>
</ul>
<h3>Key Points</h3>
<ul>
<li>Prefer constraints over triggers when the rule is simple (CHECK, FK, UNIQUE).</li>
<li><code>SELECT INTO</code> does <strong>not</strong> copy constraints—add them afterward.</li>
<li>Constraints can be <code>NOCHECK</code> disabled for bulk loads (use carefully).</li>
</ul>
<h3>Interview Answer</h3>
<p>Constraints enforce data integrity at the database layer—PK and UNIQUE for uniqueness, FK for relationships, CHECK and NOT NULL for business rules, DEFAULT for missing values. I define them in the schema so every application gets the same rules, and I use constraints before triggers when they are enough.</p>""",

"q_sql_relationships": """<h2>Database Relationships (1:1, 1:N, M:N)</h2>
<p>Relationships describe how rows in one table link to rows in another. In relational databases they are implemented with <strong>primary keys</strong>, <strong>foreign keys</strong>, and sometimes a <strong>junction (bridge) table</strong>.</p>
<p>Examples below use a <strong>PNC Bank</strong>–style retail/commercial banking model (customers, accounts, branches, engagements).</p>
<table>
<tr><th>Relationship</th><th>Description</th><th>PNC Bank example</th></tr>
<tr><td><strong>One-to-One (1:1)</strong></td><td>One record in Table A links to exactly one record in Table B</td><td>Customer ↔ KYCProfile (one customer, one compliance profile)</td></tr>
<tr><td><strong>One-to-Many (1:N)</strong></td><td>One parent record has many child records</td><td>Customer → many Accounts (checking, savings, loan)</td></tr>
<tr><td><strong>Many-to-Many (M:N)</strong></td><td>Many records linked on both sides via junction table</td><td>Customers ↔ Relationship Managers (via CustomerRMAssignment)</td></tr>
</table>
<h3>One-to-One (1:1)</h3>
<p>Each row on side A matches <strong>at most one</strong> row on side B, and vice versa.</p>
<p><strong>PNC example:</strong> Core customer data lives in <code>Customer</code>; sensitive KYC/AML details live in <code>CustomerKYCProfile</code> — split for security and optional fields.</p>
<pre><code>Customer(CustomerId PK, FirstName, LastName, Email, Phone)
CustomerKYCProfile(CustomerId PK/FK UNIQUE,
    SSNLast4, RiskRating, LastReviewDate, PEPFlag)
-- One CustomerId → exactly one KYC profile</code></pre>
<p><strong>Implementation:</strong> shared primary key, or <code>UNIQUE</code> on the FK column so one parent maps to one child only.</p>
<h3>One-to-Many (1:N)</h3>
<p>The <strong>most common</strong> relationship. The “one” side holds the primary key; the “many” side stores a foreign key.</p>
<p><strong>PNC examples:</strong></p>
<ul>
<li>One <strong>Customer</strong> → many <strong>Accounts</strong> (Virtual Wallet, checking, savings, credit card)</li>
<li>One <strong>Branch</strong> → many <strong>Employees</strong> (tellers, bankers, managers)</li>
<li>One <strong>Account</strong> → many <strong>Transactions</strong> (deposits, withdrawals, transfers)</li>
</ul>
<pre><code>Customer(CustomerId PK, FirstName, LastName)
Account(AccountId PK, CustomerId FK → Customer,
        AccountType, Balance, OpenDate)

Branch(BranchId PK, BranchName, City, State)
Employee(EmployeeId PK, BranchId FK → Branch, Role, HireDate)

-- List all accounts for a customer:
SELECT c.FirstName, c.LastName, a.AccountType, a.Balance
FROM Customer c
JOIN Account a ON c.CustomerId = a.CustomerId
WHERE c.CustomerId = 10042;</code></pre>
<p><strong>Rule:</strong> FK goes on the <strong>many</strong> side. Use <code>ON DELETE CASCADE</code> or <code>RESTRICT</code> based on banking rules (accounts usually cannot orphan a customer without closure workflow).</p>
<h3>Many-to-Many (M:N)</h3>
<p>Neither table holds a direct FK to the other. Use a <strong>junction table</strong> with a composite PK or unique pair of FKs.</p>
<p><strong>PNC examples:</strong></p>
<ul>
<li><strong>Customers ↔ Relationship Managers</strong> — a customer may have multiple RMs over time; one RM serves many customers</li>
<li><strong>Commercial clients ↔ Banking products</strong> — treasury, lending, merchant services assigned via <code>ClientProduct</code></li>
<li><strong>Employees ↔ Certifications</strong> — CFA, AML, Series 7 tracked via <code>EmployeeCertification</code></li>
</ul>
<pre><code>Customer(CustomerId PK, CompanyName)          -- commercial client
RelationshipManager(RMId PK, Name, LineOfBusiness)
CustomerRMAssignment(CustomerId FK, RMId FK, StartDate, EndDate,
                     PRIMARY KEY (CustomerId, RMId, StartDate))

-- Which RMs are assigned to a client today?
SELECT c.CompanyName, rm.Name, cra.StartDate
FROM Customer c
JOIN CustomerRMAssignment cra ON c.CustomerId = cra.CustomerId
JOIN RelationshipManager rm ON cra.RMId = rm.RMId
WHERE c.CustomerId = 5001 AND cra.EndDate IS NULL;</code></pre>
<h3>How relationships map to SQL</h3>
<table>
<tr><th>Concept</th><th>SQL object</th><th>PNC example</th></tr>
<tr><td>Identify row</td><td>PRIMARY KEY</td><td><code>CustomerId</code>, <code>AccountId</code></td></tr>
<tr><td>Link tables</td><td>FOREIGN KEY</td><td><code>Account.CustomerId → Customer</code></td></tr>
<tr><td>Enforce 1:1</td><td>UNIQUE on FK</td><td><code>CustomerKYCProfile.CustomerId UNIQUE</code></td></tr>
<tr><td>Resolve M:N</td><td>Junction table</td><td><code>CustomerRMAssignment</code></td></tr>
</table>
<h3>Interview Answer</h3>
<p>At a bank like PNC, one-to-one splits core customer from KYC profile. One-to-many is Customer to Accounts or Branch to Employees with the FK on the many side. Many-to-many uses a junction table—Customer to Relationship Manager via CustomerRMAssignment. I enforce all of these with foreign keys and appropriate delete rules so data stays consistent across channels (branch, mobile, online).</p>""",

"q_10": """<h2>Primary Key vs Unique Constraint</h2>
<p>Both enforce uniqueness, but a primary key identifies each row and cannot be NULL. A table has one primary key but can have multiple unique constraints. Unique allows one NULL in SQL Server.</p>
<p>Use a surrogate PK for identity and UNIQUE constraints for alternate business keys like email or product codes.</p>
<table>
<tr><th>Primary Key</th><th>Unique</th></tr>
<tr><td>One per table</td><td>Multiple allowed</td></tr>
<tr><td>NOT NULL required</td><td>NULL usually allowed once</td></tr>
<tr><td>Creates clustered index (SQL Server default)</td><td>Non-clustered by default</td></tr>
</table>
<pre><code>CREATE TABLE Users (
  UserId INT PRIMARY KEY,
  Email NVARCHAR(255) UNIQUE,
  Phone NVARCHAR(20) UNIQUE NULL
);</code></pre>
<h3>Key Points</h3>
<ul>
<li>PK is the row identifier; unique constraints protect alternate business keys.</li>
<li>Don't make every unique column a PK—use surrogate keys when needed.</li>
<li>Both create indexes automatically in most engines.</li>
</ul>
<h3>Interview Answer</h3>
<p>Primary key is the main row identifier—one per table, no NULLs. Unique constraints also block duplicates but allow NULLs and you can have several. I use PK for identity and UNIQUE for emails, codes, etc.</p>""",

"q_sql_types_of_keys": """<h2>Types of Keys in SQL</h2>
<p>Keys identify rows uniquely and link tables. Below are the key types interviewers expect, with <strong>PNC Bank</strong>–style examples.</p>
<table>
<tr><th>Key type</th><th>What it is</th><th>PNC example</th></tr>
<tr><td><strong>Super key</strong></td><td>Any column/set that uniquely identifies a row (may include extra columns)</td><td><code>{CustomerId}</code>, <code>{CustomerId, Email}</code></td></tr>
<tr><td><strong>Candidate key</strong></td><td>Minimal super key — no subset is also unique</td><td><code>CustomerId</code> or <code>Email</code> (if unique)</td></tr>
<tr><td><strong>Primary key (PK)</strong></td><td>Chosen candidate key; one per table; NOT NULL</td><td><code>Customer.CustomerId</code></td></tr>
<tr><td><strong>Alternate key</strong></td><td>Other candidate keys not chosen as PK; enforced with UNIQUE</td><td><code>UNIQUE(Email)</code>, <code>UNIQUE(AccountNumber)</code></td></tr>
<tr><td><strong>Foreign key (FK)</strong></td><td>Column(s) referencing parent PK/unique key</td><td><code>Account.CustomerId → Customer</code></td></tr>
<tr><td><strong>Composite key</strong></td><td>Primary or foreign key made of two+ columns</td><td><code>PK (CustomerId, RMId, StartDate)</code> on assignment table</td></tr>
<tr><td><strong>Surrogate key</strong></td><td>System-generated ID (IDENTITY/GUID), no business meaning</td><td><code>AccountId INT IDENTITY</code></td></tr>
<tr><td><strong>Natural key</strong></td><td>Business-meaningful unique identifier</td><td>SSN (where allowed), account number, routing+account</td></tr>
</table>
<h3>Super key vs candidate key vs primary key</h3>
<pre><code>Customer(CustomerId, Email, Phone, FirstName, LastName)

Super keys:     {CustomerId}, {CustomerId, Email}, {Email} (if unique)
Candidate keys: {CustomerId}, {Email}           -- minimal
Primary key:    CustomerId                      -- one chosen
Alternate keys: Email UNIQUE                    -- other candidates</code></pre>
<h3>Primary key</h3>
<ul>
<li>One per table; identifies each row; NOT NULL</li>
<li>In SQL Server, often creates a <strong>clustered index</strong> by default</li>
<li>Prefer stable surrogate keys (<code>IDENTITY</code>) for OLTP when natural keys can change</li>
</ul>
<pre><code>CREATE TABLE Customer (
    CustomerId INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName  NVARCHAR(50) NOT NULL
);</code></pre>
<h3>Alternate key (unique key)</h3>
<p>Candidate keys not selected as PK — enforced with <code>UNIQUE</code> constraint.</p>
<pre><code>CREATE TABLE Customer (
    CustomerId INT PRIMARY KEY,
    Email NVARCHAR(256) NOT NULL UNIQUE,
    TaxId      CHAR(9) NULL UNIQUE
);</code></pre>
<h3>Foreign key</h3>
<p>Links child to parent; enforces referential integrity.</p>
<pre><code>CREATE TABLE Account (
    AccountId   INT PRIMARY KEY,
    CustomerId  INT NOT NULL
        REFERENCES Customer(CustomerId),
    BranchId    INT NOT NULL
        REFERENCES Branch(BranchId)
);</code></pre>
<h3>Composite key</h3>
<p>Key spanning multiple columns — common on junction/transaction tables.</p>
<pre><code>CREATE TABLE CustomerRMAssignment (
    CustomerId INT NOT NULL REFERENCES Customer,
    RMId       INT NOT NULL REFERENCES RelationshipManager,
    StartDate  DATE NOT NULL,
    PRIMARY KEY (CustomerId, RMId, StartDate)
);</code></pre>
<h3>Surrogate vs natural key</h3>
<table>
<tr><th></th><th>Surrogate</th><th>Natural</th></tr>
<tr><td>Example</td><td><code>AccountId INT IDENTITY</code></td><td><code>AccountNumber</code> (10 digits)</td></tr>
<tr><td>Pros</td><td>Stable, narrow, simple joins</td><td>Meaningful to business users</td></tr>
<tr><td>Cons</td><td>Extra column; no business meaning</td><td>Can change format; may be sensitive</td></tr>
</table>
<p><strong>Banking practice:</strong> use surrogate PK internally; keep account number as UNIQUE alternate key for customer-facing lookups.</p>
<h3>Quick comparison</h3>
<table>
<tr><th>Key</th><th>Count per table</th><th>NULL?</th><th>Purpose</th></tr>
<tr><td>Primary</td><td>One</td><td>No</td><td>Row identity</td></tr>
<tr><td>Alternate (UNIQUE)</td><td>Many</td><td>Usually one NULL allowed</td><td>Other unique business identifiers</td></tr>
<tr><td>Foreign</td><td>Many</td><td>Depends on design</td><td>Relationship to parent</td></tr>
<tr><td>Composite</td><td>—</td><td>—</td><td>Multi-column PK or FK</td></tr>
</table>
<h3>Interview Answer</h3>
<p>Super keys uniquely identify rows; candidate keys are minimal super keys. I pick one candidate as the primary key—often a surrogate like CustomerId—and enforce other candidates as alternate unique keys like Email or AccountNumber. Foreign keys link Accounts to Customers and Branches. Composite keys appear on junction tables like CustomerRMAssignment. At a bank I use surrogate PKs for stability and natural or alternate keys for business lookups.</p>""",

"q_11": """<h2>UNION vs UNION ALL</h2>
<p>UNION combines result sets from two or more SELECT statements and removes duplicate rows (distinct sort/hash). UNION ALL concatenates all rows including duplicates—faster when duplicates are acceptable or impossible.</p>
<p>Column order, count, and compatible types must match across all SELECT branches.</p>
<pre><code>SELECT City FROM Customers
UNION
SELECT City FROM Suppliers;

SELECT City FROM Customers
UNION ALL
SELECT City FROM Suppliers;</code></pre>
<table>
<tr><th>UNION</th><th>UNION ALL</th></tr>
<tr><td>Removes duplicates</td><td>Keeps all rows</td></tr>
<tr><td>Slower (sort/distinct)</td><td>Faster</td></tr>
<tr><td>Same column count/types</td><td>Same column count/types</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Prefer UNION ALL when you know sets are disjoint or duplicates are fine.</li>
<li>Column order, count, and compatible types must match.</li>
<li>ORDER BY applies to the final combined result.</li>
</ul>
<h3>Interview Answer</h3>
<p>UNION merges queries and removes duplicates; UNION ALL just stacks them. I use UNION ALL for performance unless I explicitly need distinct combined results.</p>""",

"q_12": """<h2>ISNULL vs COALESCE</h2>
<p>Both replace NULL with a value. ISNULL is SQL Server–specific, takes exactly two arguments, and uses the first argument's data type. COALESCE is ANSI-standard, accepts multiple arguments, and returns the first non-NULL value.</p>
<p>ISNULL can silently truncate if types differ; COALESCE follows data-type precedence rules—prefer COALESCE for portability.</p>
<pre><code>SELECT
  ISNULL(MiddleName, 'N/A') AS Middle,
  COALESCE(MiddleName, NickName, 'N/A') AS Display
FROM Employees;

SELECT COALESCE(NullableInt, 0) FROM T;</code></pre>
<h3>Key Points</h3>
<ul>
<li>COALESCE evaluates arguments until first non-NULL; ISNULL evaluates once.</li>
<li>ISNULL can truncate if types differ; COALESCE follows precedence rules.</li>
<li>Prefer COALESCE for portability and multiple fallbacks.</li>
</ul>
<h3>Interview Answer</h3>
<p>ISNULL replaces NULL with one fallback and is SQL Server–specific. COALESCE is standard, supports multiple fallbacks, and is my default unless I need ISNULL's two-arg simplicity in T-SQL.</p>""",

"q_125": """<h2>TRUNCATE vs DELETE</h2>
<p>DELETE removes rows one at a time (or in batches), can use WHERE, fires triggers, and is fully logged per row. TRUNCATE deallocates data pages for the whole table, is faster, resets identity seeds, and cannot use WHERE.</p>
<p>TRUNCATE fails when foreign keys reference the table unless constraints are handled; use DELETE for selective removal and auditing.</p>
<table>
<tr><th>DELETE</th><th>TRUNCATE</th></tr>
<tr><td>Row-level DML</td><td>Page deallocation</td></tr>
<tr><td>WHERE supported</td><td>Removes all rows</td></tr>
<tr><td>Triggers fire</td><td>Minimal logging (varies by edition)</td></tr>
<tr><td>Can rollback in transaction</td><td>Needs ALTER permission; FK restrictions</td></tr>
</table>
<pre><code>DELETE FROM AuditLog WHERE LogDate &lt; '2024-01-01';
TRUNCATE TABLE StagingOrders;  -- fast empty staging table</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use TRUNCATE to quickly clear staging tables without filters.</li>
<li>Use DELETE for selective removal and when triggers/auditing matter.</li>
<li>TRUNCATE fails if FK references exist unless handled.</li>
</ul>
<h3>Interview Answer</h3>
<p>DELETE removes specific rows and fires triggers; TRUNCATE wipes the whole table by deallocating pages—much faster but no WHERE. I TRUNCATE staging tables and DELETE when I need filters or referential safety.</p>""",

"q_14": """<h2>Tables vs Views</h2>
<p>Tables store physical data on disk. Views are saved SELECT queries—virtual tables that present data without storing it (except indexed views in SQL Server, which materialize).</p>
<p>Views simplify complex joins and enforce row/column security but don't automatically improve performance unless indexed.</p>
<table>
<tr><th>Table</th><th>View</th></tr>
<tr><td>Physical storage</td><td>Logical definition</td></tr>
<tr><td>Full CRUD (with rules)</td><td>Read-mostly; updatable views limited</td></tr>
<tr><td>Indexes on table</td><td>Indexed view = persisted data</td></tr>
</table>
<pre><code>CREATE VIEW vw_ActiveEmployees AS
SELECT EmployeeId, Name, DeptId
FROM Employees
WHERE IsActive = 1;

SELECT * FROM vw_ActiveEmployees WHERE DeptId = 5;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Views simplify complex joins and enforce row/column security.</li>
<li>They don't automatically improve performance unless indexed.</li>
<li>Use views for abstraction; don't hide performance problems behind them.</li>
</ul>
<h3>Interview Answer</h3>
<p>Tables hold data; views are stored queries that expose a simplified or secured interface. I use views to encapsulate joins and permissions, but the underlying tables do the real storage.</p>""",

"q_15": """<h2>Stored Procedures vs Functions</h2>
<p>Stored procedures are precompiled batches for business logic, DML, and orchestration. Functions return a single scalar or table value and are designed for reuse inside queries—with restrictions on side effects.</p>
<p>Scalar UDFs can hurt performance on large sets; inline table-valued functions are preferred for set-based operations.</p>
<table>
<tr><th>Stored Procedure</th><th>Function</th></tr>
<tr><td>Can INSERT/UPDATE/DELETE</td><td>Deterministic reads (generally)</td></tr>
<tr><td>OUTPUT parameters, multiple result sets</td><td>Must RETURN value or table</td></tr>
<tr><td>EXEC in app/batch</td><td>Used in SELECT/WHERE</td></tr>
</table>
<pre><code>CREATE PROC usp_AddOrder @CustomerId INT AS
BEGIN INSERT INTO Orders(CustomerId) VALUES(@CustomerId); END;

CREATE FUNCTION fn_Tax(@Amount DECIMAL) RETURNS DECIMAL AS
BEGIN RETURN @Amount * 0.08; END;</code></pre>
<h3>Key Points</h3>
<ul>
<li>SPs for transactions and workflows; functions for reusable calculations.</li>
<li>Scalar UDFs can hurt performance on large sets—inline TVFs preferred.</li>
<li>Functions cannot modify persistent data in SQL Server.</li>
</ul>
<h3>Interview Answer</h3>
<p>Stored procedures execute business logic and can modify data; functions return computed values for use in queries. I use SPs for operations and functions for pure calculations embedded in SELECTs.</p>""",

"q_123": """<h2>Benefits of Stored Procedures</h2>
<p>Stored procedures encapsulate SQL logic on the server, offering performance, security, and maintainability advantages over ad hoc queries sent from application code.</p>
<p>Parameterized SPs prevent SQL injection when called correctly; avoid hiding all business logic in SPs when ORM migrations matter.</p>
<pre><code>CREATE PROC usp_TransferFunds
  @From INT, @To INT, @Amount DECIMAL(18,2)
AS
BEGIN TRANSACTION;
  UPDATE Accounts SET Balance = Balance - @Amount WHERE Id = @From;
  UPDATE Accounts SET Balance = Balance + @Amount WHERE Id = @To;
COMMIT;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Performance: execution plans cached; reduced network traffic.</li>
<li>Security: grant EXEC without exposing base tables.</li>
<li>Maintainability: single place to change business rules.</li>
</ul>
<h3>Interview Answer</h3>
<p>Stored procedures improve performance via plan reuse, boost security through EXEC grants, centralize business rules, and cut network round trips. I use them for complex transactional logic close to the data.</p>""",

"q_16": """<h2>Common Table Expressions (CTE)</h2>
<p>A CTE is a temporary named result set defined with WITH, scoped to a single statement. It improves readability for recursive queries and multi-step transformations without creating permanent objects.</p>
<p>Recursive CTEs traverse hierarchies (org charts, BOMs). The optimizer may inline CTEs rather than materialize them.</p>
<pre><code>WITH DeptTotals AS (
  SELECT DeptId, SUM(Salary) AS TotalSalary
  FROM Employees
  GROUP BY DeptId
)
SELECT d.DeptName, t.TotalSalary
FROM DeptTotals t
JOIN Departments d ON t.DeptId = d.DeptId;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Recursive CTEs traverse hierarchies (org charts, BOMs).</li>
<li>CTEs are not guaranteed to be materialized—optimizer may inline.</li>
<li>Can reference multiple CTEs in one WITH clause.</li>
</ul>
<h3>Interview Answer</h3>
<p>A CTE is a named subquery using WITH that makes complex SQL readable and supports recursion. It's scoped to one statement and doesn't persist like a temp table unless the optimizer materializes it.</p>""",

"q_124": """<h2>CTE vs Temp Table vs Table Variable</h2>
<p>All three hold intermediate results, but they differ in <strong>scope, indexing, statistics, and ideal data size</strong>.</p>
<table>
<tr><th></th><th>CTE</th><th>#Temp Table</th><th>@Table Variable</th></tr>
<tr><td><strong>Syntax</strong></td><td><code>WITH cte AS (...)</code></td><td><code>CREATE TABLE #t / SELECT INTO #t</code></td><td><code>DECLARE @t TABLE (...)</code></td></tr>
<tr><td><strong>Scope</strong></td><td><strong>One statement only</strong></td><td>Session (or nested procs)</td><td>Batch / procedure that declared it</td></tr>
<tr><td><strong>Stored in</strong></td><td>Not materialized — inlined into the query plan</td><td>tempdb</td><td>tempdb too (not "memory only" — common myth)</td></tr>
<tr><td><strong>Indexes</strong></td><td>No (uses base table indexes)</td><td>Yes — clustered/nonclustered, added anytime</td><td>Only PK/UNIQUE inline (+ inline indexes 2014+)</td></tr>
<tr><td><strong>Statistics</strong></td><td>n/a</td><td><strong>Yes</strong> — optimizer estimates well</td><td><strong>No</strong> — poor estimates (improved a bit in 2019)</td></tr>
<tr><td><strong>Recursion</strong></td><td><strong>Yes</strong> — recursive CTEs</td><td>No</td><td>No</td></tr>
<tr><td><strong>Transactions</strong></td><td>n/a</td><td>Fully logged, rolls back</td><td>Mostly unaffected by rollback</td></tr>
<tr><td><strong>Best size</strong></td><td>Any (it's just syntax)</td><td>Large intermediate sets</td><td>Small sets (&lt; ~1000 rows)</td></tr>
</table>
<h3>When to choose each</h3>
<ul>
<li><strong>CTE</strong> — readability: breaking a complex query into named steps, window-function filtering (<code>WHERE rnk = 1</code>), and <strong>recursion</strong> (org charts, BOM trees). Remember: referenced twice = potentially executed twice — it's not cached.</li>
<li><strong>#Temp table</strong> — large intermediate results <strong>reused across multiple statements</strong>, need indexes or accurate statistics, multi-step transformations in SPs and ETL.</li>
<li><strong>@Table variable</strong> — small lookup/staging sets, table-valued parameters (TVPs) into procs, cases where you don't want the data affected by transaction rollback.</li>
</ul>
<pre><code>-- CTE: one-statement readability + recursion
WITH TopSales AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Region ORDER BY Amount DESC) rn
    FROM Sales
)
SELECT * FROM TopSales WHERE rn = 1;

-- Temp table: big set, reused, indexed
SELECT * INTO #Sales2024 FROM Sales WHERE Year = 2024;
CREATE INDEX IX_Region ON #Sales2024(Region);
-- ...several statements reuse #Sales2024...

-- Table variable: small set / TVP
DECLARE @Ids TABLE (Id INT PRIMARY KEY);
INSERT INTO @Ids VALUES (1), (2), (3);</code></pre>
<h3>Key Points</h3>
<ul>
<li>CTE = inline syntax for one statement; not materialized, supports recursion.</li>
<li>#Temp = tempdb + indexes + statistics → best for large reused sets.</li>
<li>@Table variable = small sets; no statistics → optimizer guesses (1 row pre-2019).</li>
<li>Both #temp and @table live in tempdb — the "memory only" claim is a myth.</li>
</ul>
<h3>Interview Answer</h3>
<p>A CTE is just named query syntax scoped to one statement — great for readability, window-function filtering, and recursion, but it isn't materialized. A temp table is materialized in tempdb with indexes and real statistics, so I use it for large intermediate results reused across multiple steps in a procedure. A table variable also lives in tempdb but has no statistics, so the optimizer estimates poorly — I keep it for small sets and table-valued parameters. Rule of thumb: CTE for clarity, temp table for big reused data, table variable for tiny sets.</p>""",

"q_18": """<h2>Temp Table vs Table Variable</h2>
<p>Temp tables (#name) store data in tempdb with full statistics (after enough rows). Table variables (@name) historically had poor cardinality estimates; SQL Server 2019+ improved this with table variable deferred compilation.</p>
<p>Use table variables for small staging; temp tables for joins on large intermediate sets.</p>
<table>
<tr><th>#Temp Table</th><th>@Table Variable</th></tr>
<tr><td>tempdb, can index</td><td>Memory/tempdb, scoped to batch/proc</td></tr>
<tr><td>Good statistics</td><td>Historically poor estimates</td></tr>
<tr><td>Visible in nested proc</td><td>Not visible outside declaring scope</td></tr>
</table>
<pre><code>DECLARE @Small TABLE (Id INT PRIMARY KEY, Name NVARCHAR(50));
CREATE TABLE #Large (Id INT, Data NVARCHAR(MAX));
CREATE INDEX IX_Id ON #Large(Id);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use table variables for small staging (&lt; few thousand rows).</li>
<li>Temp tables for joins on large intermediate sets.</li>
<li>SQL Server 2019+ improved table variable estimates.</li>
</ul>
<h3>Interview Answer</h3>
<p>Temp tables support indexes and accurate stats for larger data; table variables are lightweight for small in-memory staging. Wrong choice causes bad plans—I've moved hot paths from @vars to #temp when row counts grew.</p>""",

"q_19": """<h2>Subquery vs CTE</h2>
<p>Both nest queries, but CTEs name intermediate results at the top for clarity and recursion. Correlated subqueries run per outer row and can be slower; CTEs read cleaner for multi-step logic.</p>
<p>Performance is often identical—the optimizer may produce the same plan. Prefer EXISTS over IN for correlated checks on large tables.</p>
<pre><code>-- Subquery
SELECT Name FROM Employees
WHERE DeptId IN (SELECT DeptId FROM Departments WHERE Region = 'West');

-- CTE (clearer for multiple references)
WITH WestDepts AS (
  SELECT DeptId FROM Departments WHERE Region = 'West'
)
SELECT e.Name FROM Employees e
JOIN WestDepts w ON e.DeptId = w.DeptId;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Prefer EXISTS over IN for correlated checks on large tables.</li>
<li>CTEs avoid repeating the same subquery multiple times.</li>
<li>Performance is often identical—optimizer may produce same plan.</li>
</ul>
<h3>Interview Answer</h3>
<p>Subqueries embed logic inline; CTEs name it for readability and recursion. I pick CTEs for multi-step queries and EXISTS subqueries for existence checks—then verify with the execution plan.</p>""",

"q_20": """<h2>SQL Injection</h2>
<p>SQL injection occurs when untrusted input is concatenated into SQL, letting attackers alter queries—reading data, bypassing auth, or executing destructive commands.</p>
<p>Stored procedures help only when parameters are used—not dynamic SQL built with string concatenation inside the SP.</p>
<pre><code>-- VULNERABLE:
"SELECT * FROM Users WHERE UserName = '" + input + "'"
-- input: ' OR '1'='1

-- SAFE: parameterized query
SqlCommand cmd = new("SELECT * FROM Users WHERE UserName = @u", conn);
cmd.Parameters.AddWithValue("@u", input);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Always use parameterized queries or ORM parameter binding.</li>
<li>Never concatenate user input; validate and least-privilege DB accounts.</li>
<li>SPs help only if parameters are used—not dynamic SQL inside.</li>
</ul>
<h3>Interview Answer</h3>
<p>SQL injection happens when user input becomes executable SQL. I prevent it with parameterized queries, avoid dynamic concatenation, apply least privilege, and use input validation as defense in depth.</p>""",

"q_21": """<h2>SQL Triggers — Purpose</h2>
<p>Triggers are special stored procedures that fire automatically on INSERT, UPDATE, or DELETE (and sometimes DDL). They enforce rules, audit changes, or maintain derived data—but add hidden complexity.</p>
<h3>Purpose (why use them)</h3>
<ul>
<li><strong>Audit trail</strong> — log who changed what and when (inserted/deleted tables).</li>
<li><strong>Business rules</strong> — enforce cross-row constraints that CHECK constraints cannot express.</li>
<li><strong>Derived data</strong> — maintain summary or cache tables when source rows change.</li>
<li><strong>Replication / integration</strong> — queue outbound events on DML (use carefully).</li>
</ul>
<p>inserted and deleted pseudo-tables hold new and old row versions for DML triggers.</p>
<pre><code>CREATE TRIGGER trg_AuditEmployeeUpdate
ON Employees AFTER UPDATE
AS
BEGIN
  INSERT INTO EmployeeAudit(EmployeeId, OldSalary, NewSalary, ChangedAt)
  SELECT d.EmployeeId, d.Salary, i.Salary, GETDATE()
  FROM deleted d JOIN inserted i ON d.EmployeeId = i.EmployeeId;
END;</code></pre>
<h3>Key Points</h3>
<ul>
<li>AFTER vs INSTEAD OF triggers serve different use cases.</li>
<li>Triggers can cascade and hurt debugging—prefer constraints when possible.</li>
<li>inserted/deleted pseudo-tables hold old and new row versions.</li>
</ul>
<h3>Interview Answer</h3>
<p>Triggers auto-run on data changes for auditing or enforcement. I use them sparingly because they're implicit side effects—prefer constraints and application logic unless cross-cutting audit is required.</p>""",

"q_22": """<h2>ROW_NUMBER()</h2>
<p>ROW_NUMBER() assigns a unique sequential integer to each row within a partition, ordered by specified columns. It's the go-to function for top-N per group and pagination.</p>
<p>Filter via subquery/CTE because window functions can't go in WHERE directly. Ties get different row numbers arbitrarily—use RANK for ties with gaps.</p>
<pre><code>SELECT EmployeeId, Name, Salary,
  ROW_NUMBER() OVER (PARTITION BY DeptId ORDER BY Salary DESC) AS rn
FROM Employees;

-- 2nd highest salary per dept:
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY DeptId ORDER BY Salary DESC) rn
  FROM Employees
) x WHERE rn = 2;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Ties get different row numbers—use RANK for ties with gaps.</li>
<li>PARTITION BY defines groups; ORDER BY defines sequence within group.</li>
<li>Filter via subquery/CTE—window functions can't go in WHERE directly.</li>
</ul>
<h3>Interview Answer</h3>
<p>ROW_NUMBER() numbers rows within partitions—perfect for top-N per group and pagination. Unlike RANK, it never repeats numbers even when values tie.</p>""",

"q_23": """<h2>RANK vs DENSE_RANK</h2>
<p>Both assign ranks with ties receiving the same rank. RANK leaves gaps after ties (1,1,3); DENSE_RANK does not (1,1,2). ROW_NUMBER never ties.</p>
<p>Use DENSE_RANK for leaderboard positions without gaps; RANK when Olympic-style ranking (skip after tie) is intended.</p>
<table>
<tr><th>Score</th><th>ROW_NUMBER</th><th>RANK</th><th>DENSE_RANK</th></tr>
<tr><td>100</td><td>1</td><td>1</td><td>1</td></tr>
<tr><td>100</td><td>2</td><td>1</td><td>1</td></tr>
<tr><td>90</td><td>3</td><td>3</td><td>2</td></tr>
</table>
<pre><code>SELECT Name, Score,
  RANK() OVER (ORDER BY Score DESC) AS rnk,
  DENSE_RANK() OVER (ORDER BY Score DESC) AS drnk
FROM Results;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use DENSE_RANK for leaderboard positions without gaps.</li>
<li>Use RANK when Olympic-style ranking (skip after tie) is intended.</li>
<li>NTILE splits rows into buckets.</li>
</ul>
<h3>Interview Answer</h3>
<p>RANK gives ties the same number then skips; DENSE_RANK gives ties the same number with no gaps. I pick DENSE_RANK for consecutive ranking and RANK when skipped positions after ties are acceptable.</p>""",

"q_24": """<h2>Magic Tables in Triggers</h2>
<p>In SQL Server DML triggers, <strong>inserted</strong> and <strong>deleted</strong> are virtual tables holding the new and old row versions. Together they enable audit trails and complex validation.</p>
<p>INSERT: only inserted populated. DELETE: only deleted. UPDATE: both tables populated.</p>
<pre><code>CREATE TRIGGER trg_OrderInsert ON Orders AFTER INSERT AS
BEGIN
  INSERT INTO OrderLog(OrderId, Action, LogTime)
  SELECT OrderId, 'INSERT', GETDATE() FROM inserted;
END;

-- UPDATE uses both: deleted = before, inserted = after</code></pre>
<h3>Key Points</h3>
<ul>
<li>INSERT: only inserted populated. DELETE: only deleted. UPDATE: both.</li>
<li>They exist only inside the trigger scope.</li>
<li>MERGE triggers expose inserted/deleted for matched operations.</li>
</ul>
<h3>Interview Answer</h3>
<p>Magic tables inserted and deleted are virtual tables in SQL Server triggers showing new and old rows. I use them for auditing—comparing deleted vs inserted on updates to log what changed.</p>""",

"q_25": """<h2>Deadlocks</h2>
<p>A deadlock occurs when two or more sessions hold locks each other needs, forming a cycle. SQL Server detects deadlocks, picks a victim, rolls back its transaction, and returns error 1205.</p>
<p>Access resources in consistent order across transactions and keep transactions short.</p>
<pre><code>-- Session A                    -- Session B
BEGIN TRAN                      BEGIN TRAN
UPDATE Accounts SET ... Id=1    UPDATE Accounts SET ... Id=2
UPDATE Accounts SET ... Id=2    UPDATE Accounts SET ... Id=1
-- deadlock: one victim rolled back</code></pre>
<h3>Key Points</h3>
<ul>
<li>Access resources in consistent order across transactions.</li>
<li>Keep transactions short; avoid user interaction inside transactions.</li>
<li>Use appropriate isolation; retry victim transactions in app code.</li>
</ul>
<h3>Interview Answer</h3>
<p>Deadlocks are circular lock waits—SQL Server kills one session. I prevent them by consistent lock ordering, short transactions, proper indexes to reduce lock time, and retry logic for 1205 errors.</p>""",

"q_26": """<h2>NOLOCK Hint (READ UNCOMMITTED)</h2>
<p>WITH (NOLOCK) or READ UNCOMMITTED allows reading uncommitted data—dirty reads, non-repeatable reads, and phantom rows are possible. It reduces blocking but sacrifices consistency.</p>
<p>Prefer READ COMMITTED SNAPSHOT for read concurrency without dirty reads on critical data.</p>
<pre><code>SELECT * FROM Orders WITH (NOLOCK)
WHERE OrderDate &gt;= '2024-01-01';

-- Equivalent session setting:
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Never use NOLOCK on financial or authoritative reporting data.</li>
<li>Can read rows that roll back or see inconsistent page states.</li>
<li>Prefer READ COMMITTED SNAPSHOT for read concurrency without dirty reads.</li>
</ul>
<h3>Interview Answer</h3>
<p>NOLOCK reads without shared locks, allowing dirty reads and inconsistencies. I avoid it for critical data; if I need read concurrency, I use RCSI or snapshot isolation instead.</p>""",

"q_27": """<h2>Transaction Isolation Levels</h2>
<p>Isolation levels control how transactions interact regarding dirty reads, non-repeatable reads, and phantoms—from least to most strict: READ UNCOMMITTED, READ COMMITTED (default), REPEATABLE READ, SERIALIZABLE, plus SNAPSHOT.</p>
<p>Higher isolation means more locking or version-store overhead—match level to business consistency requirements.</p>
<table>
<tr><th>Level</th><th>Dirty</th><th>Non-Repeat</th><th>Phantom</th></tr>
<tr><td>READ UNCOMMITTED</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
<tr><td>READ COMMITTED</td><td>No</td><td>Yes</td><td>Yes</td></tr>
<tr><td>REPEATABLE READ</td><td>No</td><td>No</td><td>Yes</td></tr>
<tr><td>SERIALIZABLE</td><td>No</td><td>No</td><td>No</td></tr>
</table>
<pre><code>SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION;
  SELECT * FROM Accounts WHERE Id = 1;
COMMIT;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Higher isolation = more locking/version store overhead.</li>
<li>SNAPSHOT uses row versioning without shared read locks.</li>
<li>Match level to business consistency requirements.</li>
</ul>
<h3>Interview Answer</h3>
<p>Isolation levels trade consistency for concurrency. Default READ COMMITTED prevents dirty reads; REPEATABLE READ and SERIALIZABLE tighten further. I choose based on whether the app can tolerate phantoms or needs strict serializability.</p>""",

"q_28": """<h2>SQL Transactions</h2>
<p>A transaction groups one or more operations into an atomic unit following ACID: Atomicity, Consistency, Isolation, Durability. Either all changes commit or all roll back.</p>
<p>Use TRY/CATCH with XACT_ABORT ON in modern T-SQL; keep transactions short to reduce lock duration and deadlocks.</p>
<pre><code>BEGIN TRANSACTION;
  UPDATE Accounts SET Balance = Balance - 100 WHERE Id = 1;
  UPDATE Accounts SET Balance = Balance + 100 WHERE Id = 2;
  IF @@ERROR &lt;&gt; 0 ROLLBACK TRANSACTION;
  ELSE COMMIT TRANSACTION;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Keep transactions short to reduce lock duration and deadlocks.</li>
<li>Use TRY/CATCH with XACT_ABORT ON in modern T-SQL.</li>
<li>Nested transactions use @@TRANCOUNT; savepoints allow partial rollback.</li>
</ul>
<h3>Interview Answer</h3>
<p>Transactions ensure ACID—either all SQL in the batch succeeds or none does. I wrap related DML in explicit transactions, handle errors with rollback, and keep them as short as possible.</p>""",

"q_29": """<h2>MERGE Statement</h2>
<p>MERGE performs INSERT, UPDATE, or DELETE in one statement based on a join between target and source. Useful for upserts and synchronizing staging to production tables.</p>
<p>Requires proper indexes on join keys; known concurrency issues exist under heavy contention—consider separate INSERT/UPDATE paths.</p>
<pre><code>MERGE Products AS t
USING StagingProducts AS s ON t.ProductId = s.ProductId
WHEN MATCHED THEN UPDATE SET t.Price = s.Price
WHEN NOT MATCHED THEN INSERT (ProductId, Price)
  VALUES (s.ProductId, s.Price)
WHEN NOT MATCHED BY SOURCE THEN DELETE;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Requires proper indexes on join keys for performance.</li>
<li>Known concurrency issues—consider separate INSERT/UPDATE in high contention.</li>
<li>OUTPUT clause can capture merged rows for auditing.</li>
</ul>
<h3>Interview Answer</h3>
<p>MERGE upserts and syncs target tables from a source in one statement. I use it for ETL staging loads but watch for locking and known race conditions under heavy concurrency.</p>""",

"q_30": """<h2>Stored Procedure Parameter Limits</h2>
<p>SQL Server limits stored procedure parameters to 2,100 per procedure. Hitting this usually means the design should change—table-valued parameters, JSON, or bulk insert patterns scale better.</p>
<p>Table-valued parameters avoid dynamic SQL and plan cache pollution for large ID lists.</p>
<pre><code>-- Instead of 5000 scalar params, pass a table:
CREATE TYPE IdList AS TABLE (Id INT PRIMARY KEY);
CREATE PROC usp_ProcessIds @Ids IdList READONLY AS
  SELECT * FROM Orders o JOIN @Ids i ON o.OrderId = i.Id;

-- Or JSON (SQL Server 2016+):
CREATE PROC usp_ProcessJson @Payload NVARCHAR(MAX) AS
  SELECT value FROM OPENJSON(@Payload);</code></pre>
<h3>Key Points</h3>
<ul>
<li>2,100 param limit is hard—redesign with TVPs or temp staging tables.</li>
<li>Table-valued parameters avoid dynamic SQL and plan cache pollution.</li>
<li>Bulk insert/BCP for massive datasets, not thousands of parameters.</li>
</ul>
<h3>Interview Answer</h3>
<p>SQL Server caps SP parameters at 2,100. If you're near that, the design is wrong—I'd use table-valued parameters, JSON OPENJSON, or staging tables instead of scalar param explosion.</p>""",

"q_31": """<h2>SQL vs NoSQL</h2>
<p>SQL databases use structured schemas, ACID transactions, and powerful query languages (SQL). NoSQL covers document, key-value, column, and graph stores optimized for scale, flexibility, or specific access patterns.</p>
<p>Polyglot persistence is common—SQL for transactional core, NoSQL for logs, cache, or content at scale.</p>
<table>
<tr><th>SQL</th><th>NoSQL</th></tr>
<tr><td>Schema-on-write</td><td>Often schema-on-read</td></tr>
<tr><td>Vertical + limited horizontal</td><td>Built for horizontal scale</td></tr>
<tr><td>Complex joins</td><td>Denormalized, app-side joins</td></tr>
</table>
<pre><code>-- SQL: JOIN across normalized tables
-- MongoDB: db.users.find({ "address.city": "NYC" })
-- Redis: GET session:abc123</code></pre>
<h3>Key Points</h3>
<ul>
<li>No single winner—polyglot persistence is common.</li>
<li>SQL for transactions/reporting; NoSQL for scale/flexibility.</li>
<li>Consider operational complexity of running multiple stores.</li>
</ul>
<h3>Interview Answer</h3>
<p>SQL gives strong consistency and relational modeling; NoSQL trades that for scale and schema flexibility. I choose based on access patterns, consistency needs, and team skills—not religion.</p>""",

"q_32": """<h2>NoSQL Partitioning (Sharding)</h2>
<p>Partitioning splits data across nodes by a shard key so each node holds a subset. MongoDB uses sharded clusters; Cassandra/Dynamo partition by hash of key. Good shard keys avoid hotspots and enable even distribution.</p>
<p>Cross-shard queries are expensive—design for single-shard access when possible.</p>
<pre><code>// MongoDB sharded collection (example shard key)
sh.shardCollection("shop.orders", { customerId: 1, orderDate: 1 });

// Bad: monotonic _id only → all writes to last chunk
// Better: compound key spreading writes</code></pre>
<h3>Key Points</h3>
<ul>
<li>Shard key is immutable in many systems—choose carefully upfront.</li>
<li>Hot partitions occur when key distribution is skewed.</li>
<li>Cross-shard queries are expensive; design for single-shard access.</li>
</ul>
<h3>Interview Answer</h3>
<p>NoSQL partitioning shards data by a key across nodes for horizontal scale. Success depends on shard key design—avoid hotspots, prefer queries that hit one shard, and plan for rebalancing.</p>""",

"q_33": """<h2>Primary vs Secondary Index (NoSQL)</h2>
<p>In MongoDB, the <strong>_id</strong> field has a unique primary index by default. Secondary indexes index other fields for alternate query paths—they store indexed field values plus pointers to documents.</p>
<p>Compound index field order matters—equality fields first, then sort/range columns.</p>
<pre><code>db.users.createIndex({ email: 1 }, { unique: true });  // secondary
db.orders.createIndex({ customerId: 1, orderDate: -1 }); // compound

db.orders.find({ customerId: 123 }).sort({ orderDate: -1 });</code></pre>
<h3>Key Points</h3>
<ul>
<li>Secondary indexes speed reads but slow writes (each index updated).</li>
<li>Compound index field order matters—equality first, then sort/range.</li>
<li>Covered queries return results entirely from the index.</li>
</ul>
<h3>Interview Answer</h3>
<p>Primary index is on _id by default; secondary indexes support other query patterns. I design compound indexes matching filter and sort order, and limit index count on write-heavy collections.</p>""",

"q_34": """<h2>SQL Server Internal Communication</h2>
<p>Client apps connect via Tabular Data Stream (TDS) protocol over TCP/IP or named pipes. Inside the engine, SQLOS manages threads/scheduling, the buffer pool caches pages, and components communicate through the relational engine pipeline.</p>
<p>DMVs (sys.dm_*) expose sessions, waits, IO, and plan cache internals for troubleshooting.</p>
<pre><code>-- Client → SQL Server (TDS)
-- Connection string: Server=...;Database=...;

-- Internal flow (simplified):
-- Parser → Optimizer → Execution Engine → Storage Engine → Buffer Pool → Disk</code></pre>
<h3>Key Points</h3>
<ul>
<li>Batch requests parsed, optimized (cached plans), executed by relational engine.</li>
<li>Buffer pool keeps frequently used data pages in memory.</li>
<li>DMVs (sys.dm_*) expose sessions, waits, IO, and plan cache internals.</li>
</ul>
<h3>Interview Answer</h3>
<p>Clients talk to SQL Server via TDS. Internally, queries go through parse, optimize, and execute against the buffer pool and storage engine, with SQLOS handling scheduling and memory. I troubleshoot with DMVs and wait stats.</p>""",

"q_35": """<h2>Nth Highest Salary</h2>
<p>Classic window-function problem: rank salaries descending and filter where rank equals N. Alternatives include TOP with OFFSET or correlated subqueries (less efficient).</p>
<p>DENSE_RANK handles duplicate salaries correctly for "Nth distinct value"; ROW_NUMBER gives Nth row regardless of ties.</p>
<pre><code>-- 3rd highest salary:
SELECT DISTINCT Salary FROM (
  SELECT Salary, DENSE_RANK() OVER (ORDER BY Salary DESC) AS dr
  FROM Employees
) t WHERE dr = 3;

-- OFFSET approach (SQL Server 2012+):
SELECT DISTINCT Salary FROM Employees
ORDER BY Salary DESC
OFFSET 2 ROWS FETCH NEXT 1 ROW ONLY;</code></pre>
<h3>Key Points</h3>
<ul>
<li>DENSE_RANK handles duplicate salaries for "Nth distinct value."</li>
<li>ROW_NUMBER gives Nth row even if salaries duplicate—clarify requirement.</li>
<li>Index on Salary DESC helps large tables.</li>
</ul>
<h3>Interview Answer</h3>
<p>I use DENSE_RANK or ROW_NUMBER over ORDER BY Salary DESC in a subquery, then filter rn or dr = N. For distinct Nth value, DENSE_RANK; for Nth row regardless of ties, ROW_NUMBER.</p>""",

"q_36": """<h2>Students with the Same Score — Find Names</h2>
<p><strong>Table:</strong> <code>Students(StudentID, FirstName, LastName, Score)</code></p>
<p>Return names of students whose <code>Score</code> appears more than once (at least one other student shares that score).</p>
<pre><code>-- Recommended: scores that appear 2+ times, then all students on those scores
SELECT s.FirstName, s.LastName, s.Score
FROM Students s
INNER JOIN (
    SELECT Score
    FROM Students
    GROUP BY Score
    HAVING COUNT(*) &gt; 1
) tied ON s.Score = tied.Score
ORDER BY s.Score, s.LastName, s.FirstName;</code></pre>
<pre><code>-- Alternative: self-join (pairs; DISTINCT if you only want unique rows)
SELECT DISTINCT s1.FirstName, s1.LastName, s1.Score
FROM Students s1
INNER JOIN Students s2
    ON s1.Score = s2.Score AND s1.StudentID &lt;&gt; s2.StudentID
ORDER BY s1.Score, s1.LastName, s1.FirstName;</code></pre>
<pre><code>-- General pattern (any table):
SELECT Score FROM Results
GROUP BY Score HAVING COUNT(*) &gt; 1;</code></pre>
<h3>Key Points</h3>
<ul>
<li><code>GROUP BY Score HAVING COUNT(*) &gt; 1</code> finds tied score values; join back for names.</li>
<li>Self-join returns pairs—may duplicate rows; use DISTINCT if needed.</li>
<li>Index on <code>Score</code> helps GROUP BY and join performance.</li>
</ul>
<h3>Interview Answer</h3>
<p>I find scores with COUNT &gt; 1 in a subquery, then join to Students for FirstName and LastName. That returns every student on a duplicated score, which matches “names of students who have the same scores.”</p>""",

"q_112": """<h2>SQL Performance Bottlenecks</h2>
<p>Common bottlenecks include missing indexes, stale statistics, implicit conversions, table scans, blocking locks, tempdb pressure, parameter sniffing, and inefficient queries returning too much data.</p>
<p>Measure first with execution plans, wait stats, and IO stats—not guess.</p>
<table>
<tr><th>Symptom</th><th>Likely Cause</th></tr>
<tr><td>Slow SELECT</td><td>Missing index, scan, bad estimate</td></tr>
<tr><td>Blocking</td><td>Long transactions, lock escalation</td></tr>
<tr><td>High CPU</td><td>Scans, sorts, scalar UDFs</td></tr>
<tr><td>tempdb spike</td><td>Sorts, spills, temp table abuse</td></tr>
</table>
<pre><code>SELECT wait_type, wait_time_ms FROM sys.dm_os_wait_stats
ORDER BY wait_time_ms DESC;</code></pre>
<h3>Key Points</h3>
<ul>
<li>Measure first: execution plans, wait stats, IO stats—not guess.</li>
<li>Fix highest wait type; index and rewrite queries iteratively.</li>
<li>Avoid SELECT * and functions on indexed columns in WHERE.</li>
</ul>
<h3>Interview Answer</h3>
<p>I diagnose SQL bottlenecks with execution plans and wait stats—looking for scans, bad cardinality, blocking, and tempdb spills. Fixes are usually better indexes, query rewrites, updated stats, and shorter transactions.</p>""",

"q_113": """<h2>JOIN vs CTE vs Subquery</h2>
<p>JOINs combine tables horizontally. Subqueries nest queries for filtering or scalar values. CTEs name subqueries for readability and recursion. The optimizer often produces similar plans—choose for clarity and maintainability.</p>
<p>JOIN when combining related tables; EXISTS for semi-join existence checks; CTE when the same subquery is referenced multiple times.</p>
<pre><code>-- JOIN: combine entities
SELECT o.Id, c.Name FROM Orders o JOIN Customers c ON o.CustId = c.Id;

-- Subquery filter:
SELECT * FROM Orders WHERE CustId IN (SELECT Id FROM VIPCustomers);

-- CTE: readable multi-step
WITH VIP AS (SELECT Id FROM Customers WHERE Tier = 'Gold')
SELECT o.* FROM Orders o JOIN VIP v ON o.CustId = v.Id;</code></pre>
<h3>Key Points</h3>
<ul>
<li>JOIN when combining related tables; EXISTS for semi-join existence checks.</li>
<li>CTE when same subquery referenced multiple times or recursive.</li>
<li>Always validate performance with actual execution plans.</li>
</ul>
<h3>Interview Answer</h3>
<p>JOINs merge tables; subqueries embed logic for filters or scalars; CTEs organize complex SQL. I prioritize readable intent, then tune with plans—often they're equivalent under the hood.</p>""",

"q_solid_detailed": """<h2>SOLID Principles</h2>
<p>The <strong>SOLID principles</strong> are five important design principles in Object-Oriented Programming (OOP) that help developers write:</p>
<ul>
<li>Clean code</li>
<li>Maintainable code</li>
<li>Scalable applications</li>
<li>Easily testable systems</li>
</ul>
<p>These principles are heavily used in C#, Java, .NET backend development, system design, and interviews.</p>
<h3>SOLID at a glance</h3>
<table>
<tr><th>Letter</th><th>Principle</th><th>Meaning</th></tr>
<tr><td><strong>S</strong></td><td>Single Responsibility Principle</td><td>One class should have only one reason to change</td></tr>
<tr><td><strong>O</strong></td><td>Open/Closed Principle</td><td>Open for extension, closed for modification</td></tr>
<tr><td><strong>L</strong></td><td>Liskov Substitution Principle</td><td>Child class should replace parent class without breaking behavior</td></tr>
<tr><td><strong>I</strong></td><td>Interface Segregation Principle</td><td>Don't force classes to implement unused methods</td></tr>
<tr><td><strong>D</strong></td><td>Dependency Inversion Principle</td><td>Depend on abstractions, not concrete classes</td></tr>
</table>
<h3>1. Single Responsibility Principle (SRP)</h3>
<p><strong>Definition:</strong> A class should have <strong>only one responsibility</strong> or one reason to change.</p>
<h3>Bad example</h3>
<pre><code>public class Employee
{
    public void CalculateSalary()
    {
        Console.WriteLine("Calculating salary");
    }

    public void SaveToDatabase()
    {
        Console.WriteLine("Saving employee to DB");
    }

    public void GenerateReport()
    {
        Console.WriteLine("Generating report");
    }
}</code></pre>
<p><strong>Problem:</strong> This class has multiple responsibilities — salary calculation, database operations, and report generation. If any one changes, the class changes.</p>
<h3>Good example</h3>
<pre><code>public class Employee
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public class SalaryCalculator
{
    public void CalculateSalary(Employee emp)
    {
        Console.WriteLine("Calculating salary");
    }
}

public class EmployeeRepository
{
    public void Save(Employee emp)
    {
        Console.WriteLine("Saving to DB");
    }
}

public class ReportGenerator
{
    public void Generate(Employee emp)
    {
        Console.WriteLine("Generating report");
    }
}</code></pre>
<p><strong>Benefit:</strong> Easier maintenance, better testing, low coupling.</p>
<h3>2. Open/Closed Principle (OCP)</h3>
<p><strong>Definition:</strong> Software entities should be <strong>open for extension</strong> and <strong>closed for modification</strong>. You should add new functionality without changing existing code.</p>
<h3>Bad example</h3>
<pre><code>public class PaymentProcessor
{
    public void ProcessPayment(string paymentType)
    {
        if (paymentType == "CreditCard")
        {
            Console.WriteLine("Processing credit card");
        }
        else if (paymentType == "PayPal")
        {
            Console.WriteLine("Processing PayPal");
        }
    }
}</code></pre>
<p><strong>Problem:</strong> Every new payment type requires modifying existing code.</p>
<h3>Good example</h3>
<pre><code>public interface IPayment
{
    void Pay();
}

public class CreditCardPayment : IPayment
{
    public void Pay()
    {
        Console.WriteLine("Credit Card Payment");
    }
}

public class PaypalPayment : IPayment
{
    public void Pay()
    {
        Console.WriteLine("Paypal Payment");
    }
}

public class PaymentProcessor
{
    public void ProcessPayment(IPayment payment)
    {
        payment.Pay();
    }
}</code></pre>
<p><strong>Benefit:</strong> New payment methods can be added without changing old code.</p>
<h3>3. Liskov Substitution Principle (LSP)</h3>
<p><strong>Definition:</strong> A derived class should be replaceable for its base class without affecting correctness.</p>
<h3>Bad example — classic Bird example</h3>
<pre><code>public class Bird
{
    public virtual void Fly()
    {
        Console.WriteLine("Flying");
    }
}

public class Ostrich : Bird
{
    public override void Fly()
    {
        throw new Exception("Ostrich can't fly");
    }
}</code></pre>
<p><strong>Problem:</strong> <code>Ostrich</code> breaks expected behavior.</p>
<h3>Good example</h3>
<pre><code>public interface IBird
{
    void Eat();
}

public interface IFlyingBird
{
    void Fly();
}

public class Sparrow : IBird, IFlyingBird
{
    public void Eat()
    {
        Console.WriteLine("Eating");
    }

    public void Fly()
    {
        Console.WriteLine("Flying");
    }
}

public class Ostrich : IBird
{
    public void Eat()
    {
        Console.WriteLine("Eating");
    }
}</code></pre>
<p><strong>Benefit:</strong> No unexpected behavior.</p>
<h3>4. Interface Segregation Principle (ISP)</h3>
<p><strong>Definition:</strong> Clients should not be forced to implement methods they don't use.</p>
<h3>Bad example</h3>
<pre><code>public interface IWorker
{
    void Work();
    void Eat();
}

public class Robot : IWorker
{
    public void Work()
    {
        Console.WriteLine("Working");
    }

    public void Eat()
    {
        throw new Exception("Robot doesn't eat");
    }
}</code></pre>
<p><strong>Problem:</strong> Robot is forced to implement an unnecessary method.</p>
<h3>Good example</h3>
<pre><code>public interface IWorkable
{
    void Work();
}

public interface IEatable
{
    void Eat();
}

public class Human : IWorkable, IEatable
{
    public void Work()
    {
        Console.WriteLine("Working");
    }

    public void Eat()
    {
        Console.WriteLine("Eating");
    }
}

public class Robot : IWorkable
{
    public void Work()
    {
        Console.WriteLine("Robot working");
    }
}</code></pre>
<p><strong>Benefit:</strong> Smaller, focused interfaces.</p>
<h3>5. Dependency Inversion Principle (DIP)</h3>
<p><strong>Definition:</strong> High-level modules should not depend on low-level modules. Both should depend on abstractions.</p>
<h3>Bad example</h3>
<pre><code>public class SqlServerDatabase
{
    public void Save()
    {
        Console.WriteLine("Saved to SQL Server");
    }
}

public class EmployeeService
{
    private SqlServerDatabase db = new SqlServerDatabase();

    public void SaveEmployee()
    {
        db.Save();
    }
}</code></pre>
<p><strong>Problem:</strong> <code>EmployeeService</code> is tightly coupled with SQL Server.</p>
<h3>Good example</h3>
<pre><code>public interface IDatabase
{
    void Save();
}

public class SqlServerDatabase : IDatabase
{
    public void Save()
    {
        Console.WriteLine("Saved to SQL Server");
    }
}

public class MongoDatabase : IDatabase
{
    public void Save()
    {
        Console.WriteLine("Saved to MongoDB");
    }
}

public class EmployeeService
{
    private readonly IDatabase _database;

    public EmployeeService(IDatabase database)
    {
        _database = database;
    }

    public void SaveEmployee()
    {
        _database.Save();
    }
}</code></pre>
<p><strong>Benefit:</strong> Loose coupling, easier testing, supports Dependency Injection (DI).</p>
<h3>Real-world example in .NET</h3>
<p>SOLID principles are widely used in:</p>
<ul>
<li>ASP.NET Core</li>
<li>Dependency Injection</li>
<li>Repository Pattern</li>
<li>Clean Architecture</li>
<li>Microservices</li>
<li>Unit Testing</li>
</ul>
<p><strong>Example:</strong> Controllers depend on interfaces; services are separated; repositories handle DB logic; the DI container injects dependencies.</p>
<h3>Interview quick summary</h3>
<table>
<tr><th>Principle</th><th>Interview one-liner</th></tr>
<tr><td><strong>SRP</strong></td><td>One class → one responsibility</td></tr>
<tr><td><strong>OCP</strong></td><td>Extend behavior without modifying existing code</td></tr>
<tr><td><strong>LSP</strong></td><td>Child class should behave like parent</td></tr>
<tr><td><strong>ISP</strong></td><td>Small specific interfaces are better</td></tr>
<tr><td><strong>DIP</strong></td><td>Depend on abstraction, not implementation</td></tr>
</table>
<h3>Easy mnemonic</h3>
<div class="interview-tip"><p>Think: <strong>“SOLD” architecture becomes “SOLID”</strong></p><p>Or: <strong>“Single Objects Love Interface Driven design”</strong></p></div>
<h3>Interview Answer</h3>
<p>SOLID is five OOP principles for clean, maintainable, testable code. SRP gives each class one job. OCP adds features via new classes, not edits to old ones. LSP ensures subclasses don't break parent contracts. ISP splits fat interfaces into focused ones. DIP depends on abstractions with DI, not concrete classes. In .NET I apply these through separated services, repository interfaces, and constructor injection in ASP.NET Core.</p>""",

"q_design_pattern_types": """<h2>Types of Design Patterns</h2>
<p><strong>Design patterns</strong> are proven, reusable solutions to common software design problems. The classic <strong>Gang of Four (GoF)</strong> catalog defines <strong>23 patterns</strong> in three categories: <strong>Creational</strong>, <strong>Structural</strong>, and <strong>Behavioral</strong>. Modern catalogs add concurrency and architectural patterns on top.</p>
<h3>The three categories at a glance</h3>
<table>
<tr><th>Category</th><th>Solves</th><th>Common patterns</th></tr>
<tr><td><strong>Creational</strong></td><td>How objects are <strong>created</strong></td><td>Singleton, Factory Method, Abstract Factory, Builder, Prototype</td></tr>
<tr><td><strong>Structural</strong></td><td>How objects are <strong>composed</strong></td><td>Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight</td></tr>
<tr><td><strong>Behavioral</strong></td><td>How objects <strong>communicate</strong></td><td>Strategy, Observer, Command, Mediator, Template Method, Iterator, State, Chain of Responsibility</td></tr>
</table>
<h3>1. Creational patterns — object creation</h3>
<p>Encapsulate <strong>how objects are created</strong> so calling code doesn't depend on concrete classes or complex construction logic.</p>
<table>
<tr><th>Pattern</th><th>Purpose</th><th>Real .NET example</th></tr>
<tr><td><strong>Singleton</strong></td><td>One instance, global access</td><td>Logger, AppSettings, cache manager (DI <code>AddSingleton</code>)</td></tr>
<tr><td><strong>Factory Method</strong></td><td>Subclass/method decides which class to create</td><td><code>PaymentFactory.Create("UPI")</code> → UpiPayment</td></tr>
<tr><td><strong>Abstract Factory</strong></td><td>Create families of related objects</td><td>SQL vs MongoDB provider factory (connection + command + repo)</td></tr>
<tr><td><strong>Builder</strong></td><td>Step-by-step construction of complex objects</td><td><code>WebApplication.CreateBuilder(args)</code>, <code>StringBuilder</code>, HttpRequestMessage builders</td></tr>
<tr><td><strong>Prototype</strong></td><td>Clone an existing object</td><td><code>ICloneable</code> / record <code>with</code> expressions</td></tr>
</table>
<pre><code>// Factory Method — caller never news up concrete types
public static IPayment Create(string type) =&gt; type switch
{
    "CARD" =&gt; new CardPayment(),
    "UPI"  =&gt; new UpiPayment(),
    _      =&gt; throw new NotSupportedException(type)
};</code></pre>
<h3>2. Structural patterns — object composition</h3>
<p>Combine classes and objects into <strong>larger structures</strong> while keeping them flexible and decoupled.</p>
<table>
<tr><th>Pattern</th><th>Purpose</th><th>Real .NET example</th></tr>
<tr><td><strong>Adapter</strong></td><td>Convert one interface into another</td><td>Wrapping a legacy SOAP client behind your <code>IPaymentGateway</code></td></tr>
<tr><td><strong>Decorator</strong></td><td>Add behavior without modifying the class</td><td>Caching/logging decorator around a repository; ASP.NET Core middleware is decorator-like</td></tr>
<tr><td><strong>Facade</strong></td><td>Simple interface over a complex subsystem</td><td><code>OrderService.PlaceOrder()</code> hiding inventory + payment + email steps</td></tr>
<tr><td><strong>Proxy</strong></td><td>Stand-in controlling access to the real object</td><td>EF Core lazy-loading proxies, gRPC client stubs</td></tr>
<tr><td><strong>Composite</strong></td><td>Tree of objects treated uniformly</td><td>Menu/category trees, control hierarchies</td></tr>
</table>
<pre><code>// Decorator — add caching without touching the repository
public class CachedCustomerRepo : ICustomerRepo
{
    private readonly ICustomerRepo _inner;
    private readonly IMemoryCache _cache;

    public CachedCustomerRepo(ICustomerRepo inner, IMemoryCache cache)
    { _inner = inner; _cache = cache; }

    public Task&lt;Customer?&gt; GetAsync(int id) =&gt;
        _cache.GetOrCreateAsync($"cust:{id}", _ =&gt; _inner.GetAsync(id))!;
}</code></pre>
<h3>3. Behavioral patterns — communication &amp; responsibility</h3>
<p>Define <strong>how objects interact</strong> and how responsibilities/algorithms are assigned and swapped.</p>
<table>
<tr><th>Pattern</th><th>Purpose</th><th>Real .NET example</th></tr>
<tr><td><strong>Strategy</strong></td><td>Swap algorithms at runtime</td><td>Discount/tax calculation per customer type; payment strategies</td></tr>
<tr><td><strong>Observer</strong></td><td>Notify subscribers on state change</td><td>C# <code>event</code>, RxJS in Angular, message-based notifications</td></tr>
<tr><td><strong>Command</strong></td><td>Encapsulate a request as an object</td><td>CQRS commands with MediatR; undo queues</td></tr>
<tr><td><strong>Mediator</strong></td><td>Central hub for communication</td><td><strong>MediatR</strong> in ASP.NET Core — controllers send, handlers handle</td></tr>
<tr><td><strong>Template Method</strong></td><td>Skeleton algorithm, steps overridden</td><td>Abstract base ETL job with overridable Extract/Transform/Load</td></tr>
<tr><td><strong>Chain of Responsibility</strong></td><td>Pass request along handlers</td><td>ASP.NET Core <strong>middleware pipeline</strong></td></tr>
<tr><td><strong>State</strong></td><td>Behavior changes with internal state</td><td>Order lifecycle: Placed → Paid → Shipped</td></tr>
</table>
<pre><code>// Strategy — swap behavior without if/else chains
public interface IDiscountStrategy { decimal Apply(decimal amount); }
public class RegularDiscount : IDiscountStrategy { public decimal Apply(decimal a) =&gt; a * 0.95m; }
public class PremiumDiscount : IDiscountStrategy { public decimal Apply(decimal a) =&gt; a * 0.85m; }

public class BillingService
{
    private readonly IDiscountStrategy _discount;
    public BillingService(IDiscountStrategy discount) =&gt; _discount = discount;
    public decimal Total(decimal amount) =&gt; _discount.Apply(amount);
}</code></pre>
<h3>Beyond GoF — patterns you'll be asked about</h3>
<table>
<tr><th>Pattern</th><th>Type</th><th>Where</th></tr>
<tr><td><strong>Repository</strong> / <strong>Unit of Work</strong></td><td>Data access (enterprise)</td><td>EF Core data layer — Section 5 item 7</td></tr>
<tr><td><strong>Dependency Injection</strong></td><td>Architectural / IoC</td><td>Built into ASP.NET Core — Section 2 item 28</td></tr>
<tr><td><strong>CQRS</strong></td><td>Architectural</td><td>Separate read/write models — Section 5 item 8</td></tr>
<tr><td><strong>Circuit Breaker / Retry</strong></td><td>Resilience (cloud)</td><td>Polly — Section 2 item 42</td></tr>
<tr><td><strong>Options Pattern</strong></td><td>.NET configuration</td><td><code>IOptions&lt;T&gt;</code> — Section 2 item 7</td></tr>
</table>
<h3>Patterns you already use in ASP.NET Core (without noticing)</h3>
<ul>
<li><strong>Builder</strong> — <code>WebApplication.CreateBuilder()</code></li>
<li><strong>Chain of Responsibility</strong> — middleware pipeline (<code>app.Use...</code>)</li>
<li><strong>Singleton/Scoped/Transient</strong> — DI lifetimes</li>
<li><strong>Observer</strong> — C# events, <code>IHostApplicationLifetime</code> callbacks</li>
<li><strong>Proxy</strong> — EF Core lazy loading, HttpClient handlers</li>
</ul>
<h3>Key Points</h3>
<ul>
<li>Patterns are <strong>vocabulary, not goals</strong> — don't force them everywhere.</li>
<li>Prefer <strong>composition over inheritance</strong> in most structural cases.</li>
<li>Know <strong>one concrete example per category</strong> from your own projects.</li>
<li>Recognize when a pattern adds clarity vs unnecessary indirection.</li>
</ul>
<p><strong>Related:</strong> Section 5 — Singleton (items 2–4), Factory (item 5), Strategy (item 6), Repository (item 7), CQRS (item 8).</p>
<h3>Interview Answer</h3>
<p>Design patterns fall into three GoF categories. Creational patterns like Singleton, Factory, and Builder control object creation. Structural patterns like Adapter, Decorator, and Facade handle composition — for example I've wrapped legacy APIs with Adapters and added caching with Decorators. Behavioral patterns like Strategy, Observer, and Mediator manage communication — I use Strategy for swappable business rules and MediatR for CQRS. In ASP.NET Core, the middleware pipeline is Chain of Responsibility and CreateBuilder is the Builder pattern. I apply patterns when they match a real problem, not as boilerplate.</p>""",

"q_108": """<h2>Singleton Pattern</h2>
<p>Singleton ensures a class has exactly one instance and provides global access. Common for shared resources like configuration, logging, or connection pools—though DI containers often manage lifetime instead.</p>
<p>Thread-safe lazy initialization (Lazy&lt;T&gt; in C#) is essential; avoid Singleton abuse for every shared object.</p>
<pre><code>public sealed class Logger {
  private static readonly Lazy&lt;Logger&gt; _instance =
    new(() =&gt; new Logger());
  public static Logger Instance =&gt; _instance.Value;
  private Logger() { }
  public void Log(string msg) =&gt; Console.WriteLine(msg);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Thread-safe lazy initialization (Lazy&lt;T&gt; in C#).</li>
<li>Hard to unit test due to global state—prefer DI singleton scope.</li>
<li>Avoid Singleton abuse; not every shared object needs the pattern.</li>
</ul>
<h3>Interview Answer</h3>
<p>Singleton guarantees one instance with global access—useful for shared config or logging. In modern apps I often register a single instance in DI rather than hand-rolling static Instance properties.</p>""",

"q_58": """<h2>Have You Used Singleton?</h2>
<p>Interviewers want a concrete example, tradeoffs you considered, and whether DI replaced manual Singleton. Describe real usage: logging, cache manager, or app settings—with thread safety awareness.</p>
<p>Show evolution from static Singleton to DI-managed singleton for testability.</p>
<pre><code>// Real project: centralized AppSettings via DI singleton
services.AddSingleton&lt;IAppSettings, AppSettings&gt;();

// Legacy code used static Instance; we migrated to DI
// for testability and explicit lifetime management</code></pre>
<h3>Key Points</h3>
<ul>
<li>Give a specific project example, not textbook definition only.</li>
<li>Mention thread safety and testability challenges you faced.</li>
<li>Show evolution: static Singleton → DI-managed singleton.</li>
</ul>
<h3>Interview Answer</h3>
<p>Yes—in a .NET API I used DI singleton scope for AppSettings and a cache wrapper so one instance served the app. We avoided static Singletons to keep unit tests mockable and lifetimes explicit in Startup.</p>""",

"q_114": """<h2>Singleton vs Static Class</h2>
<p>Both offer single-instance-like access, but Singleton is an instance class you can implement interfaces, inherit from, and pass as dependency. Static classes cannot be instantiated, inherited, or interface-implemented—harder to mock.</p>
<p>Prefer instance + DI over static helpers for testability; static classes suit pure stateless utilities.</p>
<table>
<tr><th>Singleton</th><th>Static Class</th></tr>
<tr><td>Instance methods, implements interfaces</td><td>All members static</td></tr>
<tr><td>Lazy init possible</td><td>Initialized on first access</td></tr>
<tr><td>DI-friendly (as singleton)</td><td>Tight coupling, poor testability</td></tr>
</table>
<pre><code>public interface IDateProvider { DateTime Now { get; } }
public class SystemDateProvider : IDateProvider {
  public DateTime Now =&gt; DateTime.UtcNow;
}
// vs static DateHelper.Now — can't mock in tests</code></pre>
<h3>Key Points</h3>
<ul>
<li>Prefer instance + DI over static helpers for testability.</li>
<li>Static classes suit pure utility functions with no state.</li>
<li>Singleton can enforce one instance; static is inherently one.</li>
</ul>
<h3>Interview Answer</h3>
<p>Singleton is an instantiable class with one instance—I can inject and mock it. Static classes can't implement interfaces or be substituted. I use static only for pure stateless utilities; otherwise DI singleton.</p>""",

"q_factory_pattern": """<h2>Factory Pattern</h2>
<p>Factory encapsulates object creation behind an interface or method so callers depend on abstractions, not concrete types. Simple Factory uses one method; Factory Method subclasses decide type; Abstract Factory creates families of related objects.</p>
<p>DI containers often replace hand-rolled factories via registration in ASP.NET Core.</p>
<pre><code>// Step 1: Common interface — every notification type implements this
public interface INotification
{
    void Send(string message);
}

// Step 2: Concrete implementations
public class EmailNotification : INotification
{
    public void Send(string message)
    {
        Console.WriteLine($"Sending EMAIL: {message}");
    }
}

public class SmsNotification : INotification
{
    public void Send(string message)
    {
        Console.WriteLine($"Sending SMS: {message}");
    }
}

// Step 3: Factory — the ONLY place that knows about concrete classes
public class NotificationFactory
{
    public static INotification Create(string channel)
    {
        switch (channel.ToLower())
        {
            case "email":
                return new EmailNotification();
            case "sms":
                return new SmsNotification();
            default:
                throw new ArgumentException($"Unknown channel: {channel}");
        }
    }
}

// Step 4: Usage — caller works only with the interface
INotification notification = NotificationFactory.Create("email");
notification.Send("Your order has shipped!");

// Adding WhatsApp later? Add one class + one case in the factory.
// No other code in the app changes.</code></pre>
<h3>Key Points</h3>
<ul>
<li>Centralizes creation logic and supports Open/Closed extension.</li>
<li>DI containers often replace hand-rolled factories via registration.</li>
<li>Abstract Factory when creating coordinated product families.</li>
</ul>
<h3>Interview Answer</h3>
<p>Factory hides concrete instantiation behind an abstraction—callers ask for INotification, not new EmailNotification. I use it when creation logic is complex or varies by config, often delegating to DI in ASP.NET.</p>""",

"q_strategy_pattern": """<h2>Strategy Pattern</h2>
<p>Strategy defines a family of interchangeable algorithms behind a common interface, letting runtime behavior change without modifying the client. It replaces large if/else or switch blocks.</p>
<p>Works well with DI—register strategy per tenant or feature flag.</p>
<pre><code>public interface IPricingStrategy {
  decimal Calculate(Order order);
}
public class CheckoutService(IPricingStrategy pricing) {
  public decimal Total(Order o) =&gt; pricing.Calculate(o);
}
// Register RegularPricing, PremiumPricing, PromoPricing via DI</code></pre>
<h3>Key Points</h3>
<ul>
<li>Encapsulates varying behavior; client depends on interface only.</li>
<li>Works well with DI—register strategy per tenant or feature flag.</li>
<li>Combine with Factory when strategy selection is dynamic.</li>
</ul>
<h3>Interview Answer</h3>
<p>Strategy swaps algorithms at runtime through a shared interface—pricing rules, payment methods, compression. I inject the strategy so new behaviors are new classes, not growing switch statements.</p>""",

"q_88": """<h2>Repository Pattern</h2>
<p>Repository mediates between domain and data mapping layers, exposing collection-like access to aggregates while hiding persistence details (EF, Dapper, SQL). It improves testability and centralizes query logic.</p>
<p>One repository per aggregate root, not necessarily per table—avoid anemic pass-through wrappers.</p>
<pre><code>public interface IOrderRepository {
  Task&lt;Order?&gt; GetByIdAsync(int id);
  Task AddAsync(Order order);
  Task SaveChangesAsync();
}
public class OrderRepository(DbContext db) : IOrderRepository {
  public Task&lt;Order?&gt; GetByIdAsync(int id) =&gt;
    db.Orders.FindAsync(id).AsTask();
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>One repository per aggregate root, not necessarily per table.</li>
<li>Don't wrap EF DbSet with zero-value pass-through—add value or skip.</li>
<li>Unit of Work often pairs with Repository for transaction boundaries.</li>
</ul>
<h3>Interview Answer</h3>
<p>Repository abstracts data access behind domain-focused interfaces so services don't depend on EF or SQL directly. I use it for test doubles and consistent query methods, avoiding anemic CRUD wrappers.</p>""",

"q_89": """<h2>CQRS (Command Query Responsibility Segregation)</h2>
<p><strong>CQRS</strong> separates the <strong>write side</strong> (Commands — change state) from the <strong>read side</strong> (Queries — return data). Instead of one model doing both, each side gets its own model optimized for its job.</p>
<pre><code>            ┌────────── Commands (writes) ──────────┐
Client →    │  CreateOrderCommand → Handler → DB     │
            └────────────────────────────────────────┘
            ┌────────── Queries (reads) ─────────────┐
Client →    │  GetOrderQuery → Handler → read model  │
            └────────────────────────────────────────┘</code></pre>
<h3>Core rule</h3>
<ul>
<li><strong>Command</strong> — changes state, returns nothing (or just an ID). Example: <code>CreateOrderCommand</code>, <code>CancelOrderCommand</code>.</li>
<li><strong>Query</strong> — returns data, changes nothing. Example: <code>GetOrderByIdQuery</code>, <code>GetOrdersForCustomerQuery</code>.</li>
<li>A request is never both — that's the "segregation".</li>
</ul>
<h3>Typical .NET implementation (MediatR)</h3>
<pre><code>// COMMAND — write side
public record CreateOrderCommand(int CustomerId, decimal Total)
    : IRequest&lt;int&gt;;                      // returns new order id

public class CreateOrderHandler : IRequestHandler&lt;CreateOrderCommand, int&gt;
{
    private readonly AppDbContext _db;
    public CreateOrderHandler(AppDbContext db) =&gt; _db = db;

    public async Task&lt;int&gt; Handle(CreateOrderCommand cmd, CancellationToken ct)
    {
        var order = new Order(cmd.CustomerId, cmd.Total);  // domain rules here
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(ct);
        return order.Id;
    }
}

// QUERY — read side (optimized DTO, no tracking, no domain logic)
public record GetOrderQuery(int Id) : IRequest&lt;OrderDto&gt;;

public class GetOrderHandler : IRequestHandler&lt;GetOrderQuery, OrderDto&gt;
{
    private readonly AppDbContext _db;
    public GetOrderHandler(AppDbContext db) =&gt; _db = db;

    public Task&lt;OrderDto&gt; Handle(GetOrderQuery q, CancellationToken ct) =&gt;
        _db.Orders.AsNoTracking()
            .Where(o =&gt; o.Id == q.Id)
            .Select(o =&gt; new OrderDto(o.Id, o.Total, o.Status))
            .FirstAsync(ct);
}

// CONTROLLER — thin, just dispatches
[HttpPost]
public async Task&lt;IActionResult&gt; Create(CreateOrderCommand cmd)
    =&gt; Ok(await _mediator.Send(cmd));

[HttpGet("{id}")]
public async Task&lt;IActionResult&gt; Get(int id)
    =&gt; Ok(await _mediator.Send(new GetOrderQuery(id)));</code></pre>
<h3>Two levels of CQRS</h3>
<table>
<tr><th>Level</th><th>Setup</th><th>When</th></tr>
<tr><td><strong>Simple (one database)</strong></td><td>Same DB; separate command/query handlers and models. Most common in real projects.</td><td>Most APIs — clean structure with low cost</td></tr>
<tr><td><strong>Full (separate stores)</strong></td><td>Write DB (normalized SQL) + read DB (denormalized SQL views, Redis, Elastic). Synced via events — <strong>eventual consistency</strong>.</td><td>Very high read load, heavy reporting, microservices</td></tr>
</table>
<h3>Benefits</h3>
<ul>
<li><strong>Independent scaling</strong> — reads usually outnumber writes 10:1; scale read replicas separately.</li>
<li><strong>Optimized models</strong> — write side enforces business rules; read side returns flat, fast DTOs (no heavy joins per request).</li>
<li><strong>Clear code organization</strong> — one handler per use case; easy to test and onboard.</li>
<li><strong>Fits validation/logging pipelines</strong> — MediatR behaviors apply cross-cutting concerns to all commands.</li>
</ul>
<h3>Costs / when NOT to use</h3>
<ul>
<li>Simple CRUD apps — CQRS is overkill; a plain service layer is fine.</li>
<li>Separate read store adds <strong>eventual consistency</strong> — the read side may lag the write side briefly; UI must tolerate it.</li>
<li>More classes/files — discipline needed to keep handlers thin.</li>
</ul>
<h3>CQRS and Event Sourcing</h3>
<p>Often mentioned together but <strong>independent</strong>: Event Sourcing stores state as a sequence of events instead of current rows. CQRS works fine with a normal relational DB — you do <em>not</em> need Event Sourcing to use CQRS.</p>
<h3>Common follow-ups</h3>
<ul>
<li><strong>Why MediatR?</strong> Decouples controller from handler (Mediator pattern); pipeline behaviors give free validation/logging per command.</li>
<li><strong>Can a command return data?</strong> Purists say no; pragmatically returning the created ID is accepted.</li>
<li><strong>How do read/write stores stay in sync?</strong> Domain/integration events published on write, consumed by a projector that updates the read model.</li>
</ul>
<h3>Key Points</h3>
<ul>
<li>Commands mutate, queries read — never both.</li>
<li>Start with single-DB CQRS (handlers + DTOs); split stores only under real read pressure.</li>
<li>Separate stores ⇒ eventual consistency — a business decision, not just technical.</li>
<li>Pairs naturally with MediatR and DDD; Event Sourcing optional.</li>
</ul>
<h3>Interview Answer</h3>
<p>CQRS separates commands that change state from queries that read it, each with its own model. In .NET I implement it with MediatR — controllers dispatch a command or query to a dedicated handler. The write side goes through domain validation; the read side uses AsNoTracking projections straight to DTOs. In most projects I keep one database with separated handlers, which already gives clean structure and testability. I'd only split into separate read/write stores when read load or reporting demands it, accepting eventual consistency. And CQRS doesn't require Event Sourcing — they're complementary but independent.</p>""",

"q_arch_ddd": """<h2>Domain-Driven Design (DDD)</h2>
<h3>What is Domain-Driven Design?</h3>
<p><strong>DDD</strong> is an approach to building software where the <strong>business domain drives the design</strong> — code is organized around business concepts (Order, Policy, Settlement), not technical layers. Complex business rules live inside a rich <strong>domain model</strong>, written in the same language the business uses.</p>
<p>Coined by Eric Evans ("the Blue Book", 2003). The core idea: for complex domains, the hardest part of software is <strong>understanding and modeling the business</strong> — not the technology. So the model and the code should be the same thing.</p>
<h3>What problem does DDD solve?</h3>
<table>
<tr><th>Problem without DDD</th><th>How DDD solves it</th></tr>
<tr><td><strong>Business logic scattered everywhere</strong> — rules duplicated across controllers, services, stored procedures, UI</td><td>Rules live in <strong>one place</strong>: the domain model (aggregates). Impossible to bypass them</td></tr>
<tr><td><strong>Translation loss</strong> — business says "settle the trade", code says <code>UpdateFlagStatus3()</code>; bugs from misunderstanding</td><td><strong>Ubiquitous Language</strong> — same words in meetings, code, and tests</td></tr>
<tr><td><strong>Anemic models</strong> — classes are just get/set bags; objects can exist in invalid states</td><td><strong>Rich models</strong> — aggregates enforce invariants in constructors/methods; invalid state is unrepresentable</td></tr>
<tr><td><strong>One giant model for everything</strong> — "Customer" means 5 different things; every change breaks something</td><td><strong>Bounded Contexts</strong> — small consistent models with explicit boundaries</td></tr>
<tr><td><strong>Unclear team/service boundaries</strong></td><td>Bounded contexts define ownership — and map naturally to <strong>microservice boundaries</strong></td></tr>
</table>
<h3>Two halves of DDD</h3>
<table>
<tr><th>Half</th><th>Focus</th><th>Concepts</th></tr>
<tr><td><strong>Strategic design</strong></td><td>How to split a big system</td><td>Ubiquitous Language, Bounded Contexts, Context Mapping</td></tr>
<tr><td><strong>Tactical design</strong></td><td>How to model inside one context</td><td>Entities, Value Objects, Aggregates, Domain Events, Repositories, Domain Services</td></tr>
</table>
<h3>Strategic concepts</h3>
<ul>
<li><strong>Ubiquitous Language</strong> — one shared vocabulary between developers and business, used in code, tests, and meetings. If business says "Settlement", the class is <code>Settlement</code>, not <code>TransactionFinalizer</code>.</li>
<li><strong>Bounded Context</strong> — a boundary inside which a model is consistent. "Customer" in <em>Sales</em> (leads, discounts) is a different model than "Customer" in <em>Billing</em> (invoices, tax IDs). Each context gets its own model — often its own service/database in microservices.</li>
<li><strong>Context Mapping</strong> — defining how contexts talk: shared kernel, customer–supplier, anti-corruption layer (ACL) to protect your model from a legacy/external model.</li>
</ul>
<h3>Entity — identity over time</h3>
<p>An <strong>Entity</strong> is an object defined by its <strong>identity</strong>, not its attributes. Two entities with identical data are still different objects; one entity remains "the same" even as its data changes.</p>
<ul>
<li>Has an ID that persists for its whole lifetime (<code>OrderId</code>, <code>CustomerId</code>).</li>
<li><strong>Equality by ID</strong> — Order #123 today and Order #123 tomorrow are the same order, even if status changed.</li>
<li>Mutable — its state changes through behavior methods (<code>order.Submit()</code>), never raw setters.</li>
<li>Test: "If two objects have the same data, are they interchangeable?" <strong>No → Entity.</strong> Two customers both named "Ravi Kumar" are still different customers.</li>
</ul>
<pre><code>public class Customer
{
    public Guid Id { get; }              // identity — never changes
    public string Name { get; private set; }   // attributes — can change

    public void Rename(string newName)        // change via behavior
    {
        if (string.IsNullOrWhiteSpace(newName))
            throw new DomainException("Name required.");
        Name = newName;
    }

    public override bool Equals(object? o) =&gt;
        o is Customer c &amp;&amp; c.Id == Id;          // equality by ID only
}</code></pre>
<h3>Value Object — defined by its values</h3>
<p>A <strong>Value Object</strong> has <strong>no identity</strong> — it is completely defined by its attribute values, and it is <strong>immutable</strong>.</p>
<ul>
<li><strong>Equality by value</strong> — two <code>Money(100, "USD")</code> objects are the same thing, fully interchangeable.</li>
<li><strong>Immutable</strong> — you never change it; you create a new one (<code>money.Add(...)</code> returns a new Money).</li>
<li>Self-validating — a <code>Money</code> with negative amount or an <code>Email</code> without "@" can never exist.</li>
<li>Examples: <code>Money</code>, <code>Address</code>, <code>DateRange</code>, <code>Email</code>, <code>Coordinates</code>.</li>
<li>Test: "Do I care <em>which one</em> it is, or just <em>what</em> it is?" Just the value → <strong>Value Object</strong>. ₹500 is ₹500 — you don't care which ₹500.</li>
</ul>
<pre><code>// C# record = perfect fit: immutable + value equality built in
public record Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        if (amount &lt; 0)
            throw new DomainException("Amount cannot be negative.");
        Amount = amount;
        Currency = currency;
    }

    public Money Add(Money other) =&gt;
        Currency == other.Currency
            ? new Money(Amount + other.Amount, Currency)   // new instance
            : throw new DomainException("Currency mismatch.");
}</code></pre>
<table>
<tr><th></th><th>Entity</th><th>Value Object</th></tr>
<tr><td>Identity</td><td>Yes — ID</td><td>No</td></tr>
<tr><td>Equality</td><td>By ID</td><td>By all values</td></tr>
<tr><td>Mutability</td><td>Mutable (via behavior)</td><td>Immutable</td></tr>
<tr><td>Example</td><td>Order, Customer, Account</td><td>Money, Address, DateRange</td></tr>
<tr><td>In C#</td><td>class with Id</td><td><code>record</code></td></tr>
</table>
<h3>Aggregate &amp; Aggregate Root — the consistency boundary</h3>
<p>An <strong>Aggregate</strong> is a cluster of entities and value objects that must stay <strong>consistent together</strong>. The <strong>Aggregate Root</strong> is the single entity that acts as the entry point — all changes go through it.</p>
<ul>
<li><strong>Example:</strong> <code>Order</code> (root) + its <code>OrderLines</code> + <code>ShippingAddress</code>. Rule "an order's total must equal the sum of its lines" can only be guaranteed if no one edits a line directly.</li>
<li><strong>Outside code can only reference the root</strong> — you can hold <code>Order</code>, never an <code>OrderLine</code> on its own.</li>
<li><strong>One transaction = one aggregate</strong> — save the whole aggregate atomically; changes to other aggregates happen via domain events (eventual consistency).</li>
<li><strong>One repository per aggregate root</strong> — <code>IOrderRepository</code> exists; <code>IOrderLineRepository</code> should not.</li>
<li>Keep aggregates <strong>small</strong> — a giant aggregate causes locking/concurrency pain. Reference other aggregates by ID (<code>CustomerId</code>), not object references.</li>
</ul>
<pre><code>public class Order                          // Aggregate Root
{
    private readonly List&lt;OrderLine&gt; _lines = new();
    public int Id { get; private set; }
    public OrderStatus Status { get; private set; }
    public int CustomerId { get; private set; }      // other aggregate → by ID
    public IReadOnlyList&lt;OrderLine&gt; Lines =&gt; _lines; // no external mutation

    public void AddLine(Product product, int qty)
    {
        if (Status != OrderStatus.Draft)
            throw new DomainException("Cannot modify a submitted order.");
        _lines.Add(new OrderLine(product.Id, product.Price, qty));
    }

    public void Submit()
    {
        if (!_lines.Any())
            throw new DomainException("Order must have at least one line.");
        Status = OrderStatus.Submitted;
        AddDomainEvent(new OrderSubmitted(Id));   // notify the rest of the system
    }
}</code></pre>
<p>The invariant is bulletproof: there is <em>no way</em> to add a line to a submitted order — the list is private and the only path is <code>AddLine</code>, which checks the rule.</p>
<h3>Other tactical building blocks</h3>
<table>
<tr><th>Block</th><th>What it is</th><th>Example</th></tr>
<tr><td><strong>Domain Event</strong></td><td>Something that happened, in past tense</td><td><code>OrderPlaced</code>, <code>PaymentReceived</code></td></tr>
<tr><td><strong>Repository</strong></td><td>Collection-like persistence abstraction, <em>per aggregate root</em></td><td><code>IOrderRepository.GetById / Add</code></td></tr>
<tr><td><strong>Domain Service</strong></td><td>Business logic that doesn't belong to one entity</td><td><code>TransferService</code> moving money between two accounts</td></tr>
</table>
<h3>Rich vs anemic domain model</h3>
<p><strong>Anemic model</strong> (what DDD fights against): entities are just get/set property bags and all logic sits in services — any code can put an object into an invalid state. <strong>Rich model</strong>: invariants live <em>inside</em> the aggregate (as in the <code>Order</code> example above), so an invalid state is simply impossible to construct.</p>
<h3>Typical solution structure (Clean/Onion + DDD)</h3>
<pre><code>MyApp.Domain         ← entities, value objects, domain events, interfaces (NO EF, no HTTP)
MyApp.Application    ← use cases: commands/queries (CQRS + MediatR), validation
MyApp.Infrastructure ← EF Core, repositories implementations, external APIs
MyApp.API            ← controllers / minimal endpoints, DI wiring</code></pre>
<p>Dependencies point <strong>inward</strong> — Domain references nothing; Infrastructure references Domain (Dependency Inversion).</p>
<h3>How DDD and CQRS fit together</h3>
<ul>
<li><strong>Commands</strong> load an aggregate from a repository, call its methods (<code>order.Submit()</code>), save — business rules enforced by the aggregate.</li>
<li><strong>Queries</strong> bypass the domain model entirely — straight projection to DTOs for speed.</li>
<li><strong>Domain events</strong> from aggregates trigger side effects (email, read-model update, integration events to other bounded contexts).</li>
</ul>
<h3>When should DDD NOT be used?</h3>
<p>DDD has a real cost — more classes, more discipline, a steeper learning curve. The investment only pays off when domain <strong>complexity</strong> is the main risk. Skip or lighten DDD when:</p>
<ul>
<li><strong>Simple CRUD apps</strong> — forms over data, admin panels, basic catalogs. The "domain" is just create/read/update/delete; aggregates and value objects add ceremony with no payoff. A plain service layer + EF Core is faster and clearer.</li>
<li><strong>Prototypes / short-lived tools</strong> — the modeling effort outlives the app.</li>
<li><strong>Technical-complexity problems</strong> — if the hard part is throughput, data volume, or integrations (not business rules), DDD doesn't address the actual problem.</li>
<li><strong>Team unfamiliar with DDD and no domain expert available</strong> — half-applied DDD (anemic entities wrapped in DDD vocabulary) gives the cost without the benefit.</li>
<li><strong>Reporting / analytics systems</strong> — read-heavy projections don't need a behavioral model at all.</li>
</ul>
<table>
<tr><th>Use DDD</th><th>Skip / lighten it</th></tr>
<tr><td>Complex business rules (finance, insurance, trading, logistics)</td><td>Simple CRUD or admin apps</td></tr>
<tr><td>Long-lived product with evolving rules</td><td>Short-lived tools, prototypes</td></tr>
<tr><td>Multiple teams — bounded contexts define ownership</td><td>Small team, single simple domain</td></tr>
<tr><td>Domain experts available to build the language with</td><td>Pure technical problems (ETL, gateways, reporting)</td></tr>
</table>
<p><strong>Good middle ground:</strong> use <em>strategic</em> DDD (bounded contexts, ubiquitous language) for the system map, and apply <em>tactical</em> DDD only in the genuinely complex contexts — CRUD contexts can stay simple.</p>
<h3>Key Points</h3>
<ul>
<li>Strategic: Ubiquitous Language + Bounded Contexts (the most valuable part — also drives microservice boundaries).</li>
<li>Tactical: Entities (identity), Value Objects (immutable values), Aggregates (consistency boundary), Domain Events.</li>
<li>One repository per aggregate root; transactions shouldn't span aggregates.</li>
<li>Rich model — rules inside entities, not anemic get/set classes.</li>
<li>Pairs naturally with Clean Architecture and CQRS.</li>
</ul>
<h3>Interview Answer</h3>
<p>DDD means designing the system around the business domain. Strategically, I start with the ubiquitous language and bounded contexts — for example, "Customer" in Sales and Billing are different models, and those boundaries often become microservice boundaries. Tactically, I model entities with identity, immutable value objects like Money, and aggregates that enforce invariants — an Order aggregate won't allow adding lines after submission, so it can never be in an invalid state. I keep one repository per aggregate root and raise domain events for side effects. In .NET I combine this with Clean Architecture — the Domain project has no dependencies — and CQRS, where commands go through the aggregate and queries project straight to DTOs. I'd use full DDD for complex rule-heavy domains, and deliberately skip it for simple CRUD.</p>""",

"q_pattern_payment_design": """<h2>Design: Payment System Where New Methods Can Be Added Without Modifying Existing Code</h2>
<p>This is a classic <strong>Open/Closed Principle</strong> design question. The answer combines three things: <strong>Strategy pattern</strong> (interchangeable payment behaviors), <strong>Factory / DI resolution</strong> (choosing the right one), and <strong>keyed DI services in .NET 8</strong> as the modern shortcut.</p>
<h3>Step 1 — Abstraction (the contract)</h3>
<pre><code>public interface IPaymentMethod
{
    string Name { get; }                       // "Card", "UPI", "PayPal"
    Task&lt;PaymentResult&gt; ProcessAsync(PaymentRequest request);
}</code></pre>
<h3>Step 2 — One class per payment method (Strategy)</h3>
<pre><code>public class CardPayment : IPaymentMethod
{
    public string Name =&gt; "Card";
    public async Task&lt;PaymentResult&gt; ProcessAsync(PaymentRequest r)
    {
        // call card gateway
        return PaymentResult.Success(r.Amount);
    }
}

public class UpiPayment : IPaymentMethod
{
    public string Name =&gt; "UPI";
    public async Task&lt;PaymentResult&gt; ProcessAsync(PaymentRequest r)
    {
        // call UPI provider
        return PaymentResult.Success(r.Amount);
    }
}</code></pre>
<h3>Step 3 — Resolver instead of switch/if-else</h3>
<pre><code>// Register ALL implementations
builder.Services.AddScoped&lt;IPaymentMethod, CardPayment&gt;();
builder.Services.AddScoped&lt;IPaymentMethod, UpiPayment&gt;();

// Resolver picks by name — no switch statement anywhere
public class PaymentProcessor
{
    private readonly IEnumerable&lt;IPaymentMethod&gt; _methods;
    public PaymentProcessor(IEnumerable&lt;IPaymentMethod&gt; methods)
        =&gt; _methods = methods;   // DI injects every registered implementation

    public Task&lt;PaymentResult&gt; PayAsync(string method, PaymentRequest r)
    {
        var handler = _methods.FirstOrDefault(
            m =&gt; m.Name.Equals(method, StringComparison.OrdinalIgnoreCase))
            ?? throw new NotSupportedException($"Payment method: {method}");
        return handler.ProcessAsync(r);
    }
}</code></pre>
<h3>.NET 8 alternative — keyed services</h3>
<pre><code>builder.Services.AddKeyedScoped&lt;IPaymentMethod, CardPayment&gt;("card");
builder.Services.AddKeyedScoped&lt;IPaymentMethod, UpiPayment&gt;("upi");

// Resolve by key
public PaymentProcessor(IServiceProvider sp)
{
    var handler = sp.GetRequiredKeyedService&lt;IPaymentMethod&gt;("upi");
}</code></pre>
<h3>Adding PayPal tomorrow</h3>
<pre><code>1. Create PayPalPayment : IPaymentMethod      // NEW file
2. Register it in DI                          // ONE line
// PaymentProcessor, controllers, all existing methods: UNTOUCHED</code></pre>
<p>That's the Open/Closed Principle: <strong>open for extension, closed for modification</strong>.</p>
<h3>Production extras worth mentioning</h3>
<ul>
<li><strong>Validation per method</strong> — each strategy validates its own request shape.</li>
<li><strong>Idempotency keys</strong> — retries must not double-charge.</li>
<li><strong>Webhooks/callbacks</strong> — async confirmation from gateways updates payment status.</li>
<li><strong>Outbox + events</strong> — <code>PaymentCompleted</code> event drives order fulfillment without coupling.</li>
<li>Config-driven enable/disable per method (feature flags).</li>
</ul>
<h3>Key Points</h3>
<ul>
<li>Interface + one class per payment method = Strategy pattern.</li>
<li>DI injects all implementations (<code>IEnumerable&lt;IPaymentMethod&gt;</code>) or .NET 8 keyed services — no switch statements.</li>
<li>New method = new class + one registration; zero changes to existing code (OCP).</li>
<li>Mention idempotency and webhook confirmation for real payment systems.</li>
</ul>
<h3>Interview Answer</h3>
<p>I'd define an IPaymentMethod interface and implement one class per method — Card, UPI, PayPal — which is the Strategy pattern. Instead of a switch statement, I register all implementations in DI and inject IEnumerable&lt;IPaymentMethod&gt; into a resolver that picks by name, or in .NET 8 use keyed services. Adding a new payment method then means writing one new class and one DI registration — no existing code changes, which is exactly the Open/Closed Principle. In a real payment system I'd also add idempotency keys so retries can't double-charge, and webhook handling for asynchronous gateway confirmations.</p>""",
}
