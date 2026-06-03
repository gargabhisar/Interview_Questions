ANSWERS = {
"q_ef_adonet": """<h2>What is ADO.NET?</h2>
<p><strong>ADO.NET</strong> is the low-level data access framework in .NET for connecting to databases, executing commands, and reading/writing data. Entity Framework Core, Dapper, and other ORMs are built on top of ADO.NET providers such as <code>Microsoft.Data.SqlClient</code>.</p>
<h3>Core ADO.NET objects</h3>
<table>
<tr><th>Object</th><th>Role</th></tr>
<tr><td><code>Connection</code></td><td>Opens a channel to the database (e.g. <code>SqlConnection</code>)</td></tr>
<tr><td><code>Command</code></td><td>Executes SQL or stored procedures (<code>SqlCommand</code>)</td></tr>
<tr><td><code>DataReader</code></td><td>Forward-only, read-only stream of rows</td></tr>
<tr><td><code>DataAdapter</code></td><td>Fills <code>DataSet</code> / <code>DataTable</code> (older pattern)</td></tr>
<tr><td><code>Parameter</code></td><td>Typed, safe parameter binding (<code>SqlParameter</code>)</td></tr>
</table>
<pre><code>await using var conn = new SqlConnection(connectionString);
await conn.OpenAsync();

await using var cmd = new SqlCommand(
    "SELECT Id, Name FROM Employees WHERE DeptId = @DeptId", conn);
cmd.Parameters.Add("@DeptId", SqlDbType.Int).Value = deptId;

await using var reader = await cmd.ExecuteReaderAsync();
while (await reader.ReadAsync())
{
    var id = reader.GetInt32(0);
    var name = reader.GetString(1);
}</code></pre>
<h3>ADO.NET vs EF Core</h3>
<table>
<tr><th>ADO.NET</th><th>EF Core</th></tr>
<tr><td>Manual SQL and mapping</td><td>LINQ, change tracking, migrations</td></tr>
<tr><td>Maximum control and performance</td><td>Higher productivity for CRUD</td></tr>
<tr><td>No built-in object graph tracking</td><td>DbContext tracks entities</td></tr>
</table>
<h3>Interview Answer</h3>
<p>ADO.NET is .NET's foundational database API — Connection, Command, DataReader, and parameters. I use it directly or via Dapper when I need raw SQL control; EF Core sits on ADO.NET and adds ORM features like LINQ and migrations.</p>""",

"q_ef_adonet_sp": """<h2>Can We Use Stored Procedures with ADO.NET?</h2>
<p><strong>Yes.</strong> ADO.NET fully supports stored procedures by setting <code>CommandType.StoredProcedure</code> on <code>SqlCommand</code> and passing parameters.</p>
<pre><code>await using var conn = new SqlConnection(connectionString);
await conn.OpenAsync();

await using var cmd = new SqlCommand("dbo.GetEmployeesByDept", conn);
cmd.CommandType = CommandType.StoredProcedure;
cmd.Parameters.Add("@DeptId", SqlDbType.Int).Value = 3;

// ExecuteReader for result sets
await using var reader = await cmd.ExecuteReaderAsync();
while (await reader.ReadAsync())
{
    Console.WriteLine(reader["Name"]);
}

// Or ExecuteNonQuery for INSERT/UPDATE/DELETE
// Or ExecuteScalar for single value (COUNT, SCOPE_IDENTITY)</code></pre>
<h3>Output / return parameters</h3>
<pre><code>var outParam = new SqlParameter("@TotalCount", SqlDbType.Int)
{
    Direction = ParameterDirection.Output
};
cmd.Parameters.Add(outParam);
await cmd.ExecuteNonQueryAsync();
int total = (int)outParam.Value;</code></pre>
<h3>EF Core can call SPs too</h3>
<pre><code>var employees = await _context.Employees
    .FromSqlRaw("EXEC dbo.GetEmployeesByDept @DeptId = {0}", deptId)
    .ToListAsync();</code></pre>
<h3>Interview Answer</h3>
<p>Yes — set CommandType to StoredProcedure, name the SP, and add SqlParameters. ADO.NET executes it and returns results via DataReader or affected rows via ExecuteNonQuery. EF Core can also map SP results with FromSqlRaw when needed.</p>""",

"q_ef_adonet_query_vs_sp": """<h2>Difference Between SQL Query &amp; Stored Procedure in ADO.NET</h2>
<p>Both are executed through <code>SqlCommand</code>, but configuration and behavior differ.</p>
<table>
<tr><th></th><th>Ad-hoc SQL query</th><th>Stored procedure</th></tr>
<tr><td>Command text</td><td><code>SELECT ... FROM ...</code></td><td>SP name e.g. <code>dbo.GetOrders</code></td></tr>
<tr><td>CommandType</td><td><code>CommandType.Text</code> (default)</td><td><code>CommandType.StoredProcedure</code></td></tr>
<tr><td>Location</td><td>SQL in application code</td><td>SQL compiled and stored in DB</td></tr>
<tr><td>Parameters</td><td><code>@param</code> in SQL string</td><td><code>@param</code> mapped to SP parameters</td></tr>
<tr><td>Plan caching</td><td>Depends on query text consistency</td><td>Plan often reused for SP</td></tr>
<tr><td>Security</td><td>Risk if concatenated — use parameters</td><td>Grant EXEC without table access</td></tr>
</table>
<pre><code>// Ad-hoc SQL (Text)
var cmd1 = new SqlCommand(
    "SELECT Id, Name FROM Employees WHERE DeptId = @DeptId", conn);
cmd1.CommandType = CommandType.Text;
cmd1.Parameters.Add("@DeptId", SqlDbType.Int).Value = 3;

// Stored procedure
var cmd2 = new SqlCommand("dbo.GetEmployeesByDept", conn);
cmd2.CommandType = CommandType.StoredProcedure;
cmd2.Parameters.Add("@DeptId", SqlDbType.Int).Value = 3;</code></pre>
<h3>When to use which</h3>
<ul>
<li><strong>Inline SQL / Text</strong> — simple reads, dynamic reporting, Dapper queries.</li>
<li><strong>Stored procedure</strong> — complex business logic in DB, security boundaries, reused batch operations.</li>
</ul>
<h3>Interview Answer</h3>
<p>In ADO.NET both use SqlCommand with parameters. The difference is CommandType: Text for inline SQL versus StoredProcedure for a named DB object. SPs live in the database with precompiled plans and EXEC permissions; ad-hoc queries live in code and use CommandType.Text.</p>""",

"q_ef_migrations_commands": """<h2>EF Core Migrations Commands</h2>
<p>EF Core migrations version your schema in code. Install the CLI tool once, then run commands from the project directory (or specify startup project).</p>
<pre><code>dotnet tool install --global dotnet-ef

# Package references in project:
# Microsoft.EntityFrameworkCore.Design
# Microsoft.EntityFrameworkCore.SqlServer (or provider)</code></pre>
<h3>Common commands</h3>
<table>
<tr><th>Command</th><th>Purpose</th></tr>
<tr><td><code>dotnet ef migrations add InitialCreate</code></td><td>Create migration from model changes</td></tr>
<tr><td><code>dotnet ef database update</code></td><td>Apply pending migrations to DB</td></tr>
<tr><td><code>dotnet ef database update PreviousMigration</code></td><td>Rollback to named migration</td></tr>
<tr><td><code>dotnet ef migrations list</code></td><td>Show applied and pending migrations</td></tr>
<tr><td><code>dotnet ef migrations remove</code></td><td>Remove last unapplied migration</td></tr>
<tr><td><code>dotnet ef migrations script</code></td><td>Generate SQL script for CI/production</td></tr>
<tr><td><code>dotnet ef dbcontext info</code></td><td>Show provider, database name</td></tr>
</table>
<pre><code># When DbContext is in a different project
dotnet ef migrations add AddOrdersTable \\
    --project MyApp.Infrastructure \\
    --startup-project MyApp.Api

dotnet ef database update --project MyApp.Infrastructure --startup-project MyApp.Api

# Generate idempotent script for deployment
dotnet ef migrations script --idempotent -o deploy.sql</code></pre>
<h3>Workflow</h3>
<ol>
<li>Change entity classes or <code>OnModelCreating</code>.</li>
<li><code>migrations add</code> — creates Up/Down C# migration files.</li>
<li>Review migration SQL; commit to source control.</li>
<li><code>database update</code> locally; use <code>migrations script</code> for production.</li>
</ol>
<h3>Interview Answer</h3>
<p>I use dotnet ef migrations add to capture model changes, dotnet ef database update to apply them, and migrations script for production deployments. I specify --startup-project when the DbContext lives in a class library separate from the API host.</p>""",

"q_ef_asnotracking": """<h2>AsNoTracking in Entity Framework Core</h2>
<p>By default EF Core <strong>tracks</strong> entities loaded from the database in the change tracker. <code>AsNoTracking()</code> tells EF to load entities as <strong>read-only snapshots</strong> — faster and lower memory, with no <code>SaveChanges</code> updates for those entities.</p>
<pre><code>// Read-only list — no change tracking
var products = await _context.Products
    .AsNoTracking()
    .Where(p =&gt; p.IsActive)
    .ToListAsync();

// Default — tracked (for updates)
var product = await _context.Products.FindAsync(id);
product.Price = 99.99m;
await _context.SaveChangesAsync();  // UPDATE sent

// Global default for read-heavy APIs
options.UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking);</code></pre>
<h3>When to use AsNoTracking</h3>
<ul>
<li>GET/list/report queries that only return DTOs.</li>
<li>Large read-only result sets — less memory and CPU.</li>
<li>Projections with <code>Select</code> to anonymous types or DTOs (often no tracking anyway).</li>
</ul>
<h3>When NOT to use</h3>
<ul>
<li>When you load an entity, modify it, and call <code>SaveChanges</code>.</li>
<li>When you need navigation fix-up and later updates on the same context instance.</li>
</ul>
<h3>AsNoTracking vs tracking</h3>
<table>
<tr><th>Tracking (default)</th><th>AsNoTracking</th></tr>
<tr><td>Detects property changes</td><td>No change detection</td></tr>
<tr><td>Higher memory</td><td>Lower overhead</td></tr>
<tr><td>SaveChanges persists edits</td><td>Edits not persisted unless re-attached</td></tr>
</table>
<h3>Interview Answer</h3>
<p>AsNoTracking disables EF change tracking for a query. I use it on read-only API endpoints and reports for better performance. For update flows I keep tracking enabled or explicitly attach entities when modifying data loaded without tracking.</p>""",

"q_ef_code_first_db_first": """<h2>EF Code First vs Database First</h2>
<p>Both are approaches to building the object-relational model — they differ in <strong>where the schema starts</strong>.</p>
<table>
<tr><th></th><th>Code First</th><th>Database First</th></tr>
<tr><td>Source of truth</td><td>C# entity classes + Fluent API</td><td>Existing database schema</td></tr>
<tr><td>Schema creation</td><td>Migrations generate/update DB</td><td>Scaffold entities from DB</td></tr>
<tr><td>Best for</td><td>Greenfield apps, full control in code</td><td>Legacy DB, DBA-owned schema</td></tr>
<tr><td>EF Core support</td><td>Primary workflow — migrations</td><td>Reverse engineering (<code>dotnet ef dbcontext scaffold</code>)</td></tr>
</table>
<h3>Code First (typical modern approach)</h3>
<pre><code>public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public decimal Price { get; set; }
}

// DbContext + OnModelCreating for relationships
dotnet ef migrations add InitialCreate
dotnet ef database update</code></pre>
<h3>Database First (scaffold from existing DB)</h3>
<pre><code>dotnet ef dbcontext scaffold \\
    "Server=.;Database=Sales;Trusted_Connection=True;" \\
    Microsoft.EntityFrameworkCore.SqlServer \\
    --output-dir Models \\
    --context AppDbContext \\
    --force</code></pre>
<p>Generates entity classes and DbContext from tables. Schema changes are made in SQL/SSMS, then re-scaffold or hand-edit entities.</p>
<h3>Model First (legacy note)</h3>
<p>EF6 had visual designer (EDMX) — largely replaced by Code First + migrations or scaffold in EF Core.</p>
<h3>Interview Answer</h3>
<p>Code First defines entities in C# and uses migrations to evolve the database — my default for new projects. Database First scaffolds entities from an existing database with dotnet ef dbcontext scaffold. I pick based on who owns the schema: developers use Code First; legacy or DBA-controlled databases use scaffold/Database First.</p>""",
}
