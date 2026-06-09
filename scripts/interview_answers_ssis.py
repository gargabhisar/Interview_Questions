ANSWERS = {
"q_ssis_intro": """<h2>What is SSIS? Why Use It? Where to Use It?</h2>
<h3>What is SSIS?</h3>
<p><strong>SQL Server Integration Services (SSIS)</strong> is a Microsoft platform for building <strong>data integration</strong> and <strong>workflow</strong> solutions. It is part of the SQL Server data platform and is used to move, transform, and load data between systems.</p>
<p>Core components:</p>
<ul>
<li><strong>Control Flow</strong> — orchestrates tasks (Execute SQL, File System, loops, precedence constraints)</li>
<li><strong>Data Flow</strong> — extracts, transforms, and loads rows (sources, transforms, destinations)</li>
<li><strong>Connection Managers</strong> — define connections to SQL Server, flat files, Excel, Azure, etc.</li>
<li><strong>Packages</strong> — the deployable unit (.dtsx); can be stored in SSISDB catalog</li>
</ul>
<p>SSIS is the primary <strong>ETL/ELT tool</strong> in the Microsoft stack for batch data movement and transformation.</p>
<h3>Why use SSIS?</h3>
<ul>
<li><strong>Visual ETL design</strong> — drag-and-drop packages in Visual Studio / SSDT</li>
<li><strong>High-volume data movement</strong> — bulk load, parallel execution, buffer tuning</li>
<li><strong>Rich transformations</strong> — lookup, merge, aggregate, derived column, data conversion</li>
<li><strong>SQL Server integration</strong> — native connectors, T-SQL tasks, SSISDB deployment and logging</li>
<li><strong>Scheduling</strong> — SQL Server Agent, Azure Data Factory, or third-party orchestrators</li>
<li><strong>Enterprise features</strong> — error handling, logging, checkpoints, configuration, security</li>
</ul>
<p>Use SSIS when you need a mature, on-prem or hybrid ETL tool tightly integrated with SQL Server and .NET.</p>
<h3>Where to use SSIS?</h3>
<table>
<tr><th>Scenario</th><th>Example</th></tr>
<tr><td><strong>Data warehouse loading</strong></td><td>Extract from OLTP → stage → transform → load star schema</td></tr>
<tr><td><strong>Database migration</strong></td><td>Move data from legacy system to SQL Server</td></tr>
<tr><td><strong>Flat file / Excel import</strong></td><td>Daily CSV feeds into staging tables</td></tr>
<tr><td><strong>Data cleansing</strong></td><td>Standardize formats, dedupe, validate before load</td></tr>
<tr><td><strong>Incremental sync</strong></td><td>CDC / watermark-based loads between systems</td></tr>
<tr><td><strong>Operational reporting</strong></td><td>Nightly refresh of summary tables</td></tr>
<tr><td><strong>Cross-system integration</strong></td><td>ERP + CRM + SQL Server consolidation</td></tr>
</table>
<p><strong>Not ideal for:</strong> real-time streaming (use Event Hubs/Kafka), simple one-off scripts (use BCP or ADF copy), or heavy application business logic (prefer .NET services).</p>
<h3>Interview Answer</h3>
<p>SSIS is Microsoft’s ETL platform for extracting, transforming, and loading data using packages with control flow and data flow. I use it for batch warehouse loads, file imports, migrations, and incremental syncs where SQL Server is the hub. I choose it for visual design, bulk performance, and SSISDB deployment—not for real-time streaming.</p>""",

"q_ssis_performance_optimization": """<h2>SSIS Performance Optimization Interview Questions &amp; Answers</h2>
<p>Strong technical interview points for <strong>ETL / SSIS performance optimization</strong> in a .NET / SQL Server environment.</p>
<h3>1. How do you improve SSIS package performance?</h3>
<p>Key techniques:</p>
<ul>
<li>Use <strong>SQL Server source queries</strong> instead of loading full tables</li>
<li>Filter data at source using <code>WHERE</code> clause</li>
<li>Use <strong>Fast Load</strong> option in OLE DB Destination</li>
<li>Increase <code>Rows Per Batch</code> and <code>Maximum Insert Commit Size</code></li>
<li>Avoid unnecessary transformations</li>
<li>Prefer <strong>SQL operations</strong> over row-by-row transformations</li>
<li>Use <strong>Lookup cache</strong> efficiently</li>
<li>Run packages in parallel where possible</li>
<li>Use proper indexing on source and destination tables</li>
<li>Disable constraints/indexes during bulk load if applicable</li>
<li>Use staging tables</li>
<li>Tune Data Flow buffer settings</li>
</ul>
<h3>2. What is Fast Load in SSIS?</h3>
<p>Fast Load uses <strong>bulk insert</strong> internally.</p>
<p><strong>Benefits:</strong></p>
<ul>
<li>Faster inserts</li>
<li>Reduced logging</li>
<li>Better batch processing</li>
</ul>
<p><strong>Common settings:</strong></p>
<ul>
<li><code>Rows Per Batch</code></li>
<li><code>Maximum Insert Commit Size</code></li>
<li><code>TABLOCK</code></li>
</ul>
<p><strong>Example:</strong> Fast load with batch size 10,000 improves large data insert performance significantly.</p>
<h3>3. What are Data Flow buffers in SSIS?</h3>
<p>SSIS processes data using memory buffers.</p>
<p><strong>Important properties:</strong></p>
<ul>
<li><code>DefaultBufferMaxRows</code></li>
<li><code>DefaultBufferSize</code></li>
</ul>
<p><strong>Performance tuning:</strong></p>
<ul>
<li>Increase buffer size for large datasets</li>
<li>Reduce row width</li>
<li>Avoid large string columns when not required</li>
</ul>
<h3>4. Difference between synchronous and asynchronous transformations?</h3>
<h4>Synchronous</h4>
<ul>
<li>Reuses same buffer</li>
<li>Faster</li>
<li>Examples: Derived Column, Data Conversion</li>
</ul>
<h4>Asynchronous</h4>
<ul>
<li>Creates new buffer</li>
<li>Slower</li>
<li>Examples: Sort, Aggregate</li>
</ul>
<p><strong>Interview point:</strong> Avoid unnecessary asynchronous transformations because they consume more memory and reduce performance.</p>
<h3>5. Why is Sort transformation slow?</h3>
<p>Sort transformation is <strong>blocking/asynchronous</strong>.</p>
<p><strong>Better approach:</strong></p>
<ul>
<li>Sort data in SQL query using <code>ORDER BY</code></li>
<li>Use indexed tables</li>
</ul>
<h3>6. How do you optimize Lookup transformation?</h3>
<h4>Full Cache</h4>
<ul>
<li>Fastest</li>
<li>Loads all reference data into memory</li>
</ul>
<h4>Partial Cache</h4>
<ul>
<li>Loads data when needed</li>
</ul>
<h4>No Cache</h4>
<ul>
<li>Slowest</li>
</ul>
<p><strong>Optimization:</strong></p>
<ul>
<li>Use indexed lookup columns</li>
<li>Use Full Cache for smaller datasets</li>
</ul>
<h3>7. How do you handle large-volume ETL loads?</h3>
<p><strong>Approach:</strong></p>
<ul>
<li>Use staging tables</li>
<li>Incremental loading</li>
<li>Partitioning</li>
<li>Parallel package execution</li>
<li>Bulk insert</li>
<li>Disable indexes temporarily</li>
<li>Use CDC/change tracking</li>
</ul>
<h3>8. What is incremental load?</h3>
<p>Instead of loading entire data every time, load only changed/new records.</p>
<p><strong>Methods:</strong></p>
<ul>
<li>Timestamp column</li>
<li>Identity column</li>
<li>Change Data Capture (CDC)</li>
<li>Change Tracking</li>
</ul>
<p><strong>Benefits:</strong></p>
<ul>
<li>Faster execution</li>
<li>Less server load</li>
</ul>
<h3>9. What causes SSIS package bottlenecks?</h3>
<p>Common reasons:</p>
<ul>
<li>Network latency</li>
<li>Poor SQL queries</li>
<li>Unindexed tables</li>
<li>Blocking transformations</li>
<li>Large row size</li>
<li>Excessive logging</li>
<li>Memory pressure</li>
</ul>
<h3>10. How do you monitor SSIS performance?</h3>
<p><strong>Methods:</strong></p>
<ul>
<li>SSIS logging</li>
<li>SQL Profiler</li>
<li>Execution reports</li>
<li>Performance Monitor</li>
<li>Catalog reports in SSISDB</li>
</ul>
<p><strong>Check:</strong></p>
<ul>
<li>Slow tasks</li>
<li>Buffer usage</li>
<li>Row counts</li>
<li>Memory consumption</li>
</ul>
<h3>Scenario: Package taking 3 hours to load data — what will you check?</h3>
<ol>
<li>Check source query performance</li>
<li>Verify indexes</li>
<li>Check transformations</li>
<li>Replace Sort/Aggregate with SQL operations</li>
<li>Enable Fast Load</li>
<li>Tune buffers</li>
<li>Reduce logging</li>
<li>Check server CPU/memory</li>
<li>Parallelize tasks if possible</li>
</ol>
<h3>Scenario: Lookup transformation is slow — what will you do?</h3>
<ul>
<li>Use Full Cache</li>
<li>Filter lookup dataset</li>
<li>Add indexes</li>
<li>Avoid unnecessary columns</li>
<li>Use SQL join if suitable</li>
</ul>
<h3>Scenario: How do you process millions of records efficiently?</h3>
<ul>
<li>Bulk load</li>
<li>Partitioning</li>
<li>Incremental load</li>
<li>Parallel execution</li>
<li>Staging tables</li>
<li>Optimized indexes</li>
<li>Minimize transformations</li>
</ul>
<h3>Real-Time Experience Answer</h3>
<p>In my ETL projects, we improved SSIS performance by replacing blocking transformations with SQL-based operations, enabling Fast Load, implementing incremental loads, and optimizing lookup caching. We also tuned buffer settings and used staging tables for bulk processing, which reduced execution time significantly.</p>
<h3>Important Keywords for Interview</h3>
<ul>
<li>Fast Load</li>
<li>Buffer tuning</li>
<li>Blocking transformation</li>
<li>Incremental load</li>
<li>CDC</li>
<li>Parallel execution</li>
<li>Staging tables</li>
<li>Bulk insert</li>
<li>Lookup cache</li>
<li>Partitioning</li>
<li>SSISDB monitoring</li>
<li>Batch processing</li>
</ul>
<h3>Interview Answer</h3>
<p>I optimize SSIS by filtering and sorting in SQL, using Fast Load with tuned batch sizes, Full Cache Lookups for reference data, incremental loads via CDC or watermark columns, staging tables for bulk work, and SSISDB reports to find bottlenecks in buffers, row counts, and slow tasks.</p>""",

"q_ssis_email_alerts": """<h2>How Do You Setup Email Triggers When ETL/SSIS Jobs Fail?</h2>
<p>A very common ETL/SSIS interview question — answer both <strong>functionally</strong> (what ops needs) and <strong>technically</strong> (how it is built).</p>
<h3>High-level answer</h3>
<p>In ETL systems, email alerts notify support or operations when a package/job <strong>fails</strong>, <strong>partially loads</strong>, or <strong>exceeds thresholds</strong>. In SSIS this is commonly done with SQL Server Agent notifications, Event Handlers, logging tables, or Script Tasks integrated with SMTP/Database Mail.</p>
<h3>1. SQL Server Agent job notifications (most common)</h3>
<p>When the SSIS package runs via SQL Server Agent:</p>
<ol>
<li>Create SQL Server Agent job</li>
<li>Add SSIS package step</li>
<li>Configure Operator in SQL Server</li>
<li>Configure Database Mail</li>
<li>Set notification: On Failure / On Success / On Completion</li>
</ol>
<p><strong>Interview line:</strong> We configure SQL Server Agent job notifications using Database Mail and Operators so automatic emails trigger whenever ETL execution fails.</p>
<h3>2. SSIS Event Handlers</h3>
<p>Use built-in handlers:</p>
<ul>
<li><code>OnError</code></li>
<li><code>OnTaskFailed</code></li>
<li><code>OnWarning</code></li>
</ul>
<p>Inside the handler: Send Mail Task, Execute SQL Task, or Script Task.</p>
<p><strong>Example:</strong> If a Data Flow Task fails, <code>OnError</code> sends email with package name, error message, execution time, and failed component.</p>
<h3>3. Send Mail Task</h3>
<p>Direct SSIS solution — configure SMTP server, To/CC, subject, and dynamic error body.</p>
<pre><code>Subject: ETL Failure Alert - Customer Load Package

Package Name: LoadCustomerData
Error: Primary Key Violation
Execution Time: 02:15 AM
Server: PROD-ETL-01</code></pre>
<h3>4. Logging + monitoring table (enterprise)</h3>
<p><strong>Flow:</strong></p>
<ol>
<li>Package logs failures into audit table</li>
<li>Monitoring procedure checks failures</li>
<li>Stored procedure sends email</li>
</ol>
<p><strong>Advantages:</strong> centralized monitoring, dashboards, retry mechanism, historical tracking.</p>
<h3>5. Script Task (advanced)</h3>
<p>C# in SSIS Script Task when you need dynamic HTML emails, log attachments, or custom escalation. Can integrate with SMTP, APIs, Teams, or Slack.</p>
<h3>Production-level best practice</h3>
<p>In production we use a combination of SQL Server Agent notifications and SSIS Event Handlers. Critical failures are logged to audit tables; emails include package details, execution ID, error description, and server name. Enterprise setups also use centralized ETL logging and dashboards.</p>
<h3>What should the email contain?</h3>
<ul>
<li>Package name, task name, failed step</li>
<li>Error description, execution timestamp, execution ID</li>
<li>Environment (DEV/UAT/PROD), server name</li>
<li>Row counts (loaded vs rejected) when available</li>
</ul>
<h3>Scenario: Package partially succeeds</h3>
<ul>
<li>Use checkpoints to resume from last successful step</li>
<li>Log failed records separately (error output / dead-letter table)</li>
<li>Send <strong>warning</strong> emails (not same as hard failure)</li>
<li>Retry failed batch only</li>
</ul>
<h3>Best practice points</h3>
<ul>
<li>Avoid emailing on every warning — use severity-based alerts</li>
<li>Do not hardcode email addresses — store recipients in config table</li>
<li>Use retry logic for transient failures (network, timeout)</li>
</ul>
<h3>One-line strong interview answer</h3>
<p>We implemented automated ETL failure notifications using SQL Server Agent alerts, SSIS OnError event handlers, centralized logging tables, and dynamic email alerts through Database Mail to ensure proactive monitoring and faster issue resolution.</p>""",

"q_ssis_control_data_flow": """<h2>Control Flow vs Data Flow in SSIS</h2>
<p>Every SSIS package has two distinct layers. Interviewers expect you to explain <strong>what each layer does</strong>, <strong>how they interact</strong>, and <strong>when to use which</strong>.</p>
<h3>Quick comparison</h3>
<table>
<tr><th>Aspect</th><th>Control Flow</th><th>Data Flow</th></tr>
<tr><td><strong>Purpose</strong></td><td>Orchestrate <strong>when</strong> and <strong>in what order</strong> work runs</td><td>Move and transform <strong>rows</strong> of data</td></tr>
<tr><td><strong>Unit of work</strong></td><td>Tasks (Execute SQL, File System, Send Mail, etc.)</td><td>Sources, transforms, destinations in a pipeline</td></tr>
<tr><td><strong>Execution model</strong></td><td>Workflow / precedence constraints</td><td>In-memory buffers, row-by-row or batch processing</td></tr>
<tr><td><strong>Containers</strong></td><td>Sequence, For Loop, Foreach Loop</td><td>Data Flow Task wraps one pipeline</td></tr>
<tr><td><strong>Typical use</strong></td><td>Truncate staging, run stored proc, send alert, loop files</td><td>Extract CSV → cleanse → lookup → load warehouse</td></tr>
</table>
<h3>Control Flow — orchestration layer</h3>
<p><strong>Control Flow</strong> defines the <strong>workflow</strong> of the package: which tasks run, in what order, and under what conditions. It does <strong>not</strong> move data rows itself (except indirectly by calling a Data Flow Task).</p>
<p><strong>Key elements:</strong></p>
<ul>
<li><strong>Tasks</strong> — Execute SQL Task, File System Task, Script Task, Send Mail Task, Execute Package Task, Data Flow Task, etc.</li>
<li><strong>Precedence constraints</strong> — success (green), failure (red), completion (blue); can add expressions for conditional branching</li>
<li><strong>Containers</strong> — Sequence Container (group tasks), For Loop (counter), Foreach Loop (files, ADO recordset, items in collection)</li>
<li><strong>Checkpoints</strong> — restart package from last successful task after failure (Control Flow only; Data Flow restarts from beginning of that task)</li>
<li><strong>Variables &amp; expressions</strong> — drive dynamic file paths, connection strings, loop counters</li>
<li><strong>Event handlers</strong> — OnError, OnWarning, OnPreExecute at package or task level</li>
</ul>
<p><strong>Think of Control Flow as:</strong> the project manager — "truncate staging, then run the load, then call the reconciliation proc, then email ops if anything failed."</p>
<h3>Data Flow — ETL pipeline layer</h3>
<p><strong>Data Flow</strong> lives <strong>inside</strong> a Data Flow Task. It is the pipeline that reads rows from a source, applies transformations, and writes to a destination.</p>
<p><strong>Key elements:</strong></p>
<ul>
<li><strong>Sources</strong> — OLE DB Source, Flat File Source, Excel Source, ODBC Source</li>
<li><strong>Transformations</strong> — Derived Column, Lookup, Conditional Split, Merge Join, Aggregate, Data Conversion, Sort</li>
<li><strong>Destinations</strong> — OLE DB Destination, Flat File Destination, SQL Server PDW, etc.</li>
<li><strong>Paths</strong> — connect components; metadata flows left to right</li>
<li><strong>Buffers</strong> — SSIS loads rows into memory buffers for high-throughput processing (tuned via DefaultBufferSize / DefaultBufferMaxRows)</li>
<li><strong>Error outputs</strong> — redirect bad rows to a separate path (error column + error code) instead of failing the whole pipeline</li>
<li><strong>Synchronous vs asynchronous transforms</strong> — sync transforms (Derived Column) modify rows in place; async transforms (Sort, Aggregate, Merge Join) may require new buffers and block downstream until complete</li>
</ul>
<p><strong>Think of Data Flow as:</strong> the assembly line — "take account rows, standardize dates, lookup branch code, split valid vs invalid, load warehouse and dead-letter table."</p>
<h3>How they work together</h3>
<ol>
<li>Control Flow runs an <strong>Execute SQL Task</strong> to truncate <code>stg.AccountDaily</code></li>
<li>Control Flow runs a <strong>Data Flow Task</strong> that extracts, transforms, and loads account rows</li>
<li>Control Flow runs another <strong>Execute SQL Task</strong> to execute <code>usp_LoadAccountFact</code></li>
<li>On failure, Control Flow <strong>Event Handler</strong> sends email via Send Mail Task</li>
</ol>
<p>The Data Flow Task is just <strong>one task</strong> in Control Flow. Multiple Data Flow Tasks can run in sequence or in parallel (separate precedence branches).</p>
<h3>PNC Bank ETL example</h3>
<p><strong>Scenario:</strong> Nightly load of retail account balances from core banking extract into the data warehouse for regulatory and customer reporting.</p>
<p><strong>Control Flow (orchestration):</strong></p>
<ul>
<li>Foreach Loop Container — iterate over daily CSV files dropped by the core system</li>
<li>Execute SQL Task — log file name and start time to <code>ETL.AuditLog</code></li>
<li>Data Flow Task — load and transform rows (see below)</li>
<li>Execute SQL Task — run <code>usp_ReconcileAccountCounts</code> (source count vs loaded count)</li>
<li>Execute SQL Task — merge staging into <code>dw.AccountBalanceFact</code></li>
<li>Send Mail Task (OnError handler) — alert ETL ops if reconciliation fails</li>
</ul>
<p><strong>Data Flow (inside the Data Flow Task):</strong></p>
<ul>
<li><strong>Flat File Source</strong> — read <code>AccountBalance_YYYYMMDD.csv</code></li>
<li><strong>Data Conversion</strong> — fix decimal and date formats</li>
<li><strong>Derived Column</strong> — compute <code>LoadDate</code>, normalize account type codes</li>
<li><strong>Lookup</strong> — match <code>BranchId</code> against <code>dim.Branch</code> (Full Cache for small reference table)</li>
<li><strong>Conditional Split</strong> — valid rows vs rows with missing branch or invalid balance</li>
<li><strong>OLE DB Destination</strong> — valid rows → <code>stg.AccountDaily</code> (Fast Load)</li>
<li><strong>OLE DB Destination (error path)</strong> — rejected rows → <code>stg.AccountDaily_Reject</code></li>
</ul>
<p>Control Flow decides <strong>when</strong> each step runs and handles failure/retry. Data Flow handles <strong>how</strong> millions of account rows are cleansed and loaded efficiently.</p>
<h3>Common interview follow-ups</h3>
<p><strong>Q: Can you put a SQL query in Control Flow?</strong></p>
<p>Yes — Execute SQL Task runs T-SQL (truncate, merge, audit). It does not pipe result rows into transformations; use Execute SQL Task + result set into variable + Foreach Loop, or move row processing into Data Flow.</p>
<p><strong>Q: What happens if a Data Flow Task fails?</strong></p>
<p>The Data Flow Task fails in Control Flow. Precedence constraints route to failure path (logging, email, checkpoint restart). Rows already committed to destination depend on transaction/batch settings; uncommitted batches may roll back.</p>
<p><strong>Q: Why use staging tables?</strong></p>
<p>Separate Control Flow (bulk load to staging via Data Flow) from Control Flow (set-based merge in SQL). Easier restart, reconciliation, and performance tuning.</p>
<p><strong>Q: Sync vs async transforms?</strong></p>
<p>Synchronous transforms (Derived Column, Copy Column) are cheaper — they modify the current buffer. Asynchronous transforms (Sort, Aggregate, Lookup with partial cache issues, Merge Join) may block and use extra memory; they are common performance bottlenecks.</p>
<h3>One-line strong interview answer</h3>
<p>Control Flow orchestrates package workflow — tasks, loops, precedence, and error handling — while Data Flow is the row-level ETL pipeline inside a Data Flow Task with sources, transforms, destinations, and error outputs. In a banking nightly load, Control Flow loops files, truncates staging, runs the Data Flow, reconciles counts, and merges to the warehouse; Data Flow handles extract, cleanse, lookup, and split valid vs rejected account rows.</p>""",

"q_ssis_flat_file_etl": """<h2>End-to-End Flat File ETL / SSIS Approach</h2>
<p>Structured real-world flow for a common SSIS interview scenario: a daily flat file arrives in a shared location and must be loaded into a destination database.</p>
<h3>Scenario</h3>
<p>We receive a flat file daily in a shared location and need to load it into a destination database.</p>
<h3>1. Source file arrival</h3>
<p>A flat file (CSV/TXT) is dropped daily into a shared folder:</p>
<pre><code>\\\\SharedDrive\\DailyFiles\\</code></pre>
<p>Example file name:</p>
<pre><code>Customer_20260608.csv</code></pre>
<h3>2. File validation</h3>
<p>Before loading, validate:</p>
<ul>
<li>File exists</li>
<li>Naming convention is correct</li>
<li>File extension is valid (.csv / .txt)</li>
<li>File is not empty</li>
<li>Column count and format match the expected layout</li>
<li>File has not already been processed (duplicate check)</li>
</ul>
<p>Implement with:</p>
<ul>
<li>SSIS Script Task</li>
<li>File System Task</li>
<li>Execute SQL Task (check audit table for prior load)</li>
</ul>
<h3>3. Archive old files</h3>
<p>After successful processing, move files to archive:</p>
<pre><code>\\\\SharedDrive\\Archive\\</code></pre>
<p>Failed files go to reject folder:</p>
<pre><code>\\\\SharedDrive\\Reject\\</code></pre>
<h3>4. SSIS package design — Control Flow</h3>
<pre><code>File System Task
      ↓
Data Flow Task
      ↓
Execute SQL Task
      ↓
Send Mail Task</code></pre>
<h3>5. Data Flow Task</h3>
<pre><code>Flat File Source
      ↓
Data Conversion / Derived Column
      ↓
Lookup Transformation
      ↓
Conditional Split
      ↓
OLE DB Destination</code></pre>
<h3>6. Flat File Source</h3>
<p>Read CSV/TXT using a <strong>Flat File Connection Manager</strong>.</p>
<p>Example columns:</p>
<pre><code>CustomerID
CustomerName
City
CreatedDate</code></pre>
<h3>7. Transformations</h3>
<p><strong>Data Conversion</strong> — convert data types:</p>
<ul>
<li>string → int</li>
<li>string → datetime</li>
</ul>
<p>Example:</p>
<pre><code>CustomerID : DT_STR → DT_I4</code></pre>
<p><strong>Derived Column</strong> — add metadata columns:</p>
<ul>
<li><code>LoadDate</code> — e.g. <code>GETDATE()</code></li>
<li><code>FileName</code></li>
<li><code>CreatedBy</code> — e.g. <code>"SSIS_DailyLoad"</code></li>
</ul>
<p><strong>Lookup Transformation</strong> — check whether record already exists in destination:</p>
<ul>
<li>Existing customer → Update path</li>
<li>New customer → Insert path</li>
</ul>
<p><strong>Conditional Split</strong> — separate valid vs invalid records. Invalid rows go to error table or reject file.</p>
<h3>8. Load into destination</h3>
<p>Use <strong>OLE DB Destination</strong> with Fast Load where appropriate.</p>
<p><strong>Best practice — staging first:</strong></p>
<pre><code>Flat File → Staging Table → Final Production Table</code></pre>
<p>Load into <code>stg.CustomerDaily</code>, then merge to <code>dbo.Customer</code> via stored procedure.</p>
<h3>9. Stored procedure execution</h3>
<p>After staging load, run set-based SQL via <strong>Execute SQL Task</strong>:</p>
<ul>
<li>Merge data (INSERT/UPDATE)</li>
<li>Apply business rules</li>
<li>Deduplicate</li>
<li>Update audit table</li>
</ul>
<h3>10. Logging &amp; auditing</h3>
<p>Maintain an audit table:</p>
<table>
<tr><th>FileName</th><th>TotalRows</th><th>SuccessRows</th><th>FailedRows</th><th>LoadDate</th></tr>
<tr><td>Customer_20260608.csv</td><td>10000</td><td>9980</td><td>20</td><td>2026-06-08</td></tr>
</table>
<p>Enable:</p>
<ul>
<li>SSIS logging (SSISDB / text / SQL Server log provider)</li>
<li>Custom SQL audit table</li>
<li>Error output logging from Data Flow</li>
</ul>
<h3>11. Error handling</h3>
<p>If the package fails:</p>
<ul>
<li>Capture error message into log table</li>
<li>Move bad file to Reject folder</li>
<li>Send failure email notification</li>
<li>Use precedence constraints on failure path (Event Handlers optional)</li>
</ul>
<p><strong>Related:</strong> Section 13 item 3 — Email Alerts on ETL/SSIS Failure.</p>
<h3>12. Email notification</h3>
<p>Use <strong>Send Mail Task</strong> or SQL Server Agent notification.</p>
<pre><code>Subject: Daily Customer File Load Successful

Body:
Total Rows: 10000
Loaded: 9980
Failed: 20</code></pre>
<h3>13. Scheduling</h3>
<ul>
<li>Deploy package to <strong>SSIS Catalog (SSISDB)</strong></li>
<li>Schedule with <strong>SQL Server Agent Job</strong></li>
<li>Run daily at a fixed time (e.g. 2:00 AM after file drop)</li>
</ul>
<h3>Performance improvements (important for interview)</h3>
<p><strong>Fast Load</strong> on OLE DB Destination:</p>
<ul>
<li>Enable Table Lock</li>
<li>Use Fast Load / TABLOCK</li>
</ul>
<p><strong>Batch processing:</strong></p>
<pre><code>Maximum Insert Commit Size = 10000</code></pre>
<p><strong>Index handling:</strong></p>
<ul>
<li>Disable nonclustered indexes before huge load (if approved)</li>
<li>Rebuild indexes after load</li>
</ul>
<p><strong>Parallel execution:</strong></p>
<ul>
<li>Multiple Data Flow Tasks or parallel file processing for very large volumes</li>
</ul>
<p><strong>Related:</strong> Section 13 item 2 — SSIS Performance Optimization; Section 13 item 4 — Control Flow vs Data Flow.</p>
<h3>Interview Answer</h3>
<p>In our ETL process, we first validate the incoming flat file, load data into staging tables through SSIS transformations, handle errors separately, execute stored procedures for business logic, maintain audit logging, and schedule the package through SQL Server Agent with email notifications for monitoring.</p>""",
}
