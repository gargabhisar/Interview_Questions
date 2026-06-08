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

"q_7": """<h2>Database Indexes</h2>
<p>Indexes are auxiliary data structures (typically B-trees) that speed up data retrieval by avoiding full table scans. They trade faster reads for extra storage and slower writes due to index maintenance.</p>
<p>Design indexes around real query patterns—filters, joins, ORDER BY, and GROUP BY—and validate with execution plans rather than indexing every column.</p>
<pre><code>-- Clustered index on primary key (default in SQL Server)
CREATE CLUSTERED INDEX IX_Emp_Id ON Employees(EmployeeId);

-- Nonclustered index for frequent filter
CREATE NONCLUSTERED INDEX IX_Emp_Dept
ON Employees(DepartmentId) INCLUDE (LastName, Salary);</code></pre>
<table>
<tr><th>Pros</th><th>Cons</th></tr>
<tr><td>Faster SELECT/WHERE/JOIN</td><td>Slower INSERT/UPDATE/DELETE</td></tr>
<tr><td>Enforces uniqueness (unique index)</td><td>Extra disk and memory</td></tr>
</table>
<h3>Key Points</h3>
<ul>
<li>Index columns used in WHERE, JOIN, ORDER BY, and GROUP BY.</li>
<li>Too many indexes hurt write-heavy workloads.</li>
<li>Use covering indexes (INCLUDE) to avoid key lookups.</li>
</ul>
<h3>Interview Answer</h3>
<p>Indexes accelerate lookups like a book index but slow writes. I index selective, frequently queried columns, verify with execution plans, and avoid over-indexing OLTP tables.</p>""",

"q_8": """<h2>Clustered vs Non-Clustered Indexes</h2>
<p>A clustered index defines the physical sort order of table rows—there can be only one per table. A non-clustered index is a separate structure with pointers (or row locators) back to the data.</p>
<p>Range scans on the clustered key are very efficient; non-clustered indexes may require key lookups when columns aren't covered.</p>
<table>
<tr><th>Clustered</th><th>Non-Clustered</th></tr>
<tr><td>One per table</td><td>Many allowed</td></tr>
<tr><td>Data stored in index order</td><td>Separate structure + lookup</td></tr>
<tr><td>Default on PRIMARY KEY</td><td>Leaf points to clustered key or RID</td></tr>
</table>
<pre><code>CREATE TABLE Employees (
  EmployeeId INT PRIMARY KEY,  -- clustered by default
  DeptId INT,
  Name NVARCHAR(100)
);
CREATE NONCLUSTERED INDEX IX_Dept ON Employees(DeptId);</code></pre>
<h3>Key Points</h3>
<ul>
<li>Range scans on clustered key are very efficient.</li>
<li>Non-clustered indexes may require key lookups (bookmark/RID).</li>
<li>Choose clustered key on narrow, ever-increasing column (e.g., identity).</li>
</ul>
<h3>Interview Answer</h3>
<p>Clustered index sorts the table physically—one per table. Non-clustered indexes are separate lookup structures. I put the clustered index on the most common range-scan column, usually the PK.</p>""",

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

"q_124": """<h2>CTE vs Temp Table</h2>
<p>CTEs exist only for the duration of one statement and are ideal for readability and recursion. Temp tables (#table) persist for the session, support indexes/statistics, and suit multi-step ETL or large intermediate results.</p>
<p>Table variables (@t) are a third option for small in-memory staging sets.</p>
<table>
<tr><th>CTE</th><th>Temp Table</th></tr>
<tr><td>Single statement scope</td><td>Session scope</td></tr>
<tr><td>No indexes (generally)</td><td>Indexes and stats possible</td></tr>
<tr><td>Recursive support</td><td>Better for large datasets</td></tr>
</table>
<pre><code>SELECT * INTO #TopSales FROM Sales WHERE Year = 2024;
CREATE INDEX IX_Region ON #TopSales(Region);
-- reuse across batches</code></pre>
<h3>Key Points</h3>
<ul>
<li>Use CTE for clarity; temp table when data is reused or needs indexing.</li>
<li>Temp tables live in tempdb; watch contention at scale.</li>
<li>Table variables (@t) are a third option for small sets.</li>
</ul>
<h3>Interview Answer</h3>
<p>CTEs are inline, single-statement helpers; temp tables persist in tempdb with indexes for heavier multi-step work. I choose based on reuse, size, and whether I need statistics for the optimizer.</p>""",

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
<p>GoF patterns divide into Creational (object creation), Structural (composition), and Behavioral (communication/responsibility). Modern catalogs add concurrency and architectural patterns.</p>
<p>Patterns are vocabulary—not goals. Don't force them everywhere; use when they match a real problem.</p>
<table>
<tr><th>Category</th><th>Examples</th><th>Purpose</th></tr>
<tr><td>Creational</td><td>Singleton, Factory, Builder</td><td>Encapsulate creation</td></tr>
<tr><td>Structural</td><td>Adapter, Decorator, Facade</td><td>Compose objects</td></tr>
<tr><td>Behavioral</td><td>Strategy, Observer, Command</td><td>Algorithms &amp; interaction</td></tr>
</table>
<pre><code>// Creational: Factory creates without exposing new()
// Structural: Adapter wraps legacy API
// Behavioral: Strategy swaps algorithms at runtime</code></pre>
<h3>Key Points</h3>
<ul>
<li>Patterns are vocabulary—not goals. Don't force them everywhere.</li>
<li>Prefer composition over inheritance in most structural cases.</li>
<li>Know when a pattern adds clarity vs unnecessary indirection.</li>
</ul>
<h3>Interview Answer</h3>
<p>Design patterns fall into creational, structural, and behavioral groups. I name them when they match a real problem—Factory for creation complexity, Strategy for swappable behavior—not as boilerplate.</p>""",

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
<pre><code>public interface INotification { void Send(string msg); }
public class NotificationFactory {
  public static INotification Create(string channel) =&gt; channel switch {
    "email" =&gt; new EmailNotification(),
    "sms"   =&gt; new SmsNotification(),
    _       =&gt; throw new ArgumentException()
  };
}</code></pre>
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
<p>CQRS separates read models from write models. Commands change state through validated handlers; queries return optimized read DTOs—possibly from different stores or denormalized views.</p>
<p>Adds complexity—use when read/write shapes diverge significantly; often paired with Event Sourcing but not required.</p>
<pre><code>// Command side
public record CreateOrderCommand(int CustomerId, decimal Total);
public class CreateOrderHandler {
  public async Task Handle(CreateOrderCommand cmd) {
    // validate, persist event/entity
  }
}

// Query side
public class OrderSummaryQuery {
  public async Task&lt;OrderDto&gt; Get(int id) =&gt;
    await _readDb.OrderSummaries.FindAsync(id);
}</code></pre>
<h3>Key Points</h3>
<ul>
<li>Scales reads and writes independently; read models can be denormalized.</li>
<li>Adds complexity—use when read/write shapes diverge significantly.</li>
<li>Often paired with Event Sourcing but not required.</li>
</ul>
<h3>Interview Answer</h3>
<p>CQRS splits commands that mutate state from queries that read it, allowing optimized read models and clear validation paths. I adopt it when read patterns differ heavily from writes—not for simple CRUD apps.</p>""",
}
