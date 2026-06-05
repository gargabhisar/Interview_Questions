ANSWERS = {
"q_ssis_performance_optimization": """<h2>SSIS Performance Optimization</h2>
<p>Key techniques for ETL / SSIS in a .NET / SQL Server environment.</p>
<h3>1. How do you improve SSIS package performance?</h3>
<ul>
<li>Use <strong>SQL Server source queries</strong> instead of loading full tables</li>
<li>Filter at source with <code>WHERE</code></li>
<li>Enable <strong>Fast Load</strong> on OLE DB Destination</li>
<li>Increase <code>Rows Per Batch</code> and <code>Maximum Insert Commit Size</code></li>
<li>Avoid unnecessary transformations; prefer <strong>set-based SQL</strong> over row-by-row logic</li>
<li>Tune <strong>Lookup cache</strong> (Full Cache for small reference sets)</li>
<li>Run packages or tasks in <strong>parallel</strong> where possible</li>
<li>Index source and destination tables; use <strong>staging tables</strong></li>
<li>Disable constraints/indexes during bulk load when safe</li>
<li>Tune Data Flow buffer settings (<code>DefaultBufferMaxRows</code>, <code>DefaultBufferSize</code>)</li>
</ul>
<h3>2. What is Fast Load?</h3>
<p>Fast Load uses <strong>bulk insert</strong> internally for faster loads, reduced logging, and better batching.</p>
<p>Common settings: <code>Rows Per Batch</code>, <code>Maximum Insert Commit Size</code>, <code>TABLOCK</code>. Example: batch size 10,000 often improves large inserts significantly.</p>
<h3>3. Data Flow buffers</h3>
<p>SSIS moves rows through in-memory buffers. Tune <code>DefaultBufferMaxRows</code> and <code>DefaultBufferSize</code> for large datasets; reduce row width and avoid oversized string columns when not needed.</p>
<h3>4. Synchronous vs asynchronous transformations</h3>
<table>
<tr><th>Type</th><th>Behavior</th><th>Examples</th></tr>
<tr><td><strong>Synchronous</strong></td><td>Reuses same buffer; faster</td><td>Derived Column, Data Conversion</td></tr>
<tr><td><strong>Asynchronous</strong></td><td>Creates new buffer; slower, more memory</td><td>Sort, Aggregate</td></tr>
</table>
<p>Avoid unnecessary asynchronous transforms—they block the pipeline and increase memory use.</p>
<h3>5. Why is Sort slow?</h3>
<p>Sort is <strong>blocking/asynchronous</strong>. Prefer <code>ORDER BY</code> in the source SQL query or pre-sorted indexed tables instead of the Sort transform.</p>
<h3>6. Optimize Lookup transformation</h3>
<table>
<tr><th>Cache mode</th><th>When</th></tr>
<tr><td><strong>Full Cache</strong></td><td>Fastest; load all reference data into memory (small/medium sets)</td></tr>
<tr><td><strong>Partial Cache</strong></td><td>Loads matches on demand</td></tr>
<tr><td><strong>No Cache</strong></td><td>Slowest; hits DB per row/batch</td></tr>
</table>
<ul>
<li>Index lookup join columns</li>
<li>Return only needed columns</li>
<li>Consider a SQL join in source query instead of Lookup when appropriate</li>
</ul>
<h3>7. Large-volume ETL loads</h3>
<ul>
<li>Staging tables, incremental loading, partitioning</li>
<li>Parallel package execution, bulk insert</li>
<li>Temporarily disable nonclustered indexes during load (rebuild after)</li>
<li>CDC / Change Tracking for deltas</li>
</ul>
<h3>8. Incremental load</h3>
<p>Load only changed/new rows instead of full reload.</p>
<p><strong>Methods:</strong> timestamp column, identity/high-water mark, Change Data Capture (CDC), Change Tracking.</p>
<p><strong>Benefits:</strong> faster runs, less CPU/IO, smaller maintenance windows.</p>
<h3>9. Common bottlenecks</h3>
<ul>
<li>Network latency between SSIS and SQL Server</li>
<li>Missing indexes, heavy blocking transforms (Sort/Aggregate)</li>
<li>Wide rows, excessive SSIS logging, memory pressure</li>
<li>Row-by-row updates instead of set-based SQL</li>
</ul>
<h3>10. Monitor SSIS performance</h3>
<ul>
<li>SSIS logging and SSISDB catalog execution reports</li>
<li>SQL Profiler / Extended Events, Performance Monitor</li>
<li>Watch slow tasks, buffer usage, row counts, memory</li>
</ul>
<h3>Scenario: Package takes 3 hours — what do you check?</h3>
<ol>
<li>Source query plan and indexes</li>
<li>Replace Sort/Aggregate with SQL</li>
<li>Enable Fast Load; tune batch/commit sizes</li>
<li>Buffer tuning; reduce logging</li>
<li>Server CPU/memory; parallelize where safe</li>
</ol>
<h3>Scenario: Lookup is slow</h3>
<ul>
<li>Switch to Full Cache (if dataset fits memory)</li>
<li>Filter lookup query; index join columns</li>
<li>Drop unused columns; use SQL join in source if better</li>
</ul>
<h3>Scenario: Millions of records</h3>
<ul>
<li>Bulk load + staging; incremental/CDC</li>
<li>Partitioning; parallel execution</li>
<li>Optimized indexes; minimal transforms in data flow</li>
</ul>
<h3>Keywords</h3>
<p>Fast Load, buffer tuning, blocking transformation, incremental load, CDC, parallel execution, staging tables, bulk insert, lookup cache, partitioning, SSISDB, batch processing.</p>
<h3>Interview Answer</h3>
<p>In ETL projects I improve SSIS by pushing filters and sorts into SQL, enabling Fast Load with tuned batch sizes, using Full Cache Lookups for small reference data, and incremental loads via CDC or watermark columns. Staging tables, buffer tuning, and SSISDB execution reports help us cut runtime and find bottlenecks early.</p>""",
}
