ANSWERS = {
"q_quick_highest_in_array": """<h2>How to Find the Highest Integer in an Array?</h2>
<p>Common coding and C# fundamentals interview question.</p>
<h3>Loop approach — O(n)</h3>
<pre><code>int FindMax(int[] numbers)
{
    if (numbers.Length == 0)
        throw new ArgumentException("Array is empty");

    int max = numbers[0];
    for (int i = 1; i &lt; numbers.Length; i++)
    {
        if (numbers[i] &gt; max)
            max = numbers[i];
    }
    return max;
}</code></pre>
<h3>LINQ</h3>
<pre><code>int max = numbers.Max();</code></pre>
<h3>Interview Answer</h3>
<p>I scan the array once keeping track of the current maximum — O(n) time. In C# I can also use <code>numbers.Max()</code> for clarity on in-memory collections.</p>""",

"q_quick_pagination_alternatives": """<h2>Is Skip/Take (OFFSET) the Only Way to Paginate?</h2>
<p><strong>No.</strong> OFFSET pagination is the most common approach, but not the only one — and not always the best for very large tables.</p>
<h3>1. OFFSET / FETCH (Skip / Take)</h3>
<pre><code>SELECT * FROM Orders
ORDER BY OrderId
OFFSET @Skip ROWS FETCH NEXT @PageSize ROWS ONLY;</code></pre>
<p><strong>Pros:</strong> simple, supports jumping to page N.<br/>
<strong>Cons:</strong> deep pages slow down (database still scans skipped rows).</p>
<h3>2. Keyset / cursor pagination</h3>
<pre><code>SELECT * FROM Orders
WHERE OrderId &gt; @LastSeenOrderId
ORDER BY OrderId
FETCH NEXT @PageSize ROWS ONLY;</code></pre>
<p><strong>Pros:</strong> stable performance for "next page" / infinite scroll.<br/>
<strong>Cons:</strong> harder to jump to arbitrary page numbers.</p>
<h3>3. API patterns</h3>
<ul>
<li>Page number + size → maps to OFFSET</li>
<li>Cursor token from previous response → keyset pagination</li>
</ul>
<p><strong>Related:</strong> See also REST API and EF Core topics — filter at database level before paging.</p>
<h3>Interview Answer</h3>
<p>Skip/Take is the simplest pagination but not the only option. For large datasets I prefer keyset pagination using the last seen ID. I choose based on whether the UI needs random page jumps or infinite scroll.</p>""",

"q_quick_dotnet_vs_angular_preference": """<h2>If There Are .NET and Angular Projects, Which Would You Prefer?</h2>
<p>Behavioral interview question — answer honestly, then show flexibility.</p>
<h3>Strong answer structure</h3>
<ol>
<li>State your core strength (.NET API, SQL, auth, deployment — or Angular UI)</li>
<li>Show full-stack awareness (DTOs, JWT flow, HttpClient, CORS)</li>
<li>Align with the role — prefer the project that matches job focus</li>
<li>Offer to support both when the team needs it</li>
</ol>
<div class="interview-tip"><p>"I'd prefer the <strong>.NET API project</strong> because that's where I deliver most value — REST design, EF Core, security, and deployment. I still work with Angular teams on API contracts and integration, and I can take UI tasks when needed."</p></div>
<h3>Interview Answer</h3>
<p>I lead with my strongest stack, explain I understand both sides of the integration, and say I'd prefer the project where I can deliver the most impact while still supporting the other when needed.</p>""",
}
