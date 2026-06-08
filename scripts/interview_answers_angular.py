ANSWERS = {
"q_angular_lazy_loading": """<h2>What Is Lazy Loading in Angular?</h2>
<p>In Angular, <strong>lazy loading</strong> means loading a feature module or component <strong>only when the user navigates to that route</strong> — not in the initial bundle.</p>
<h3>Why use it?</h3>
<ul>
<li>Smaller first download — faster initial load</li>
<li>Admin or reporting features load only when needed</li>
<li>Better performance on slow networks</li>
</ul>
<h3>Route lazy loading (NgModule)</h3>
<pre><code>const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () =&gt; import('./admin/admin.module').then(m =&gt; m.AdminModule)
  }
];</code></pre>
<h3>Standalone components (modern Angular)</h3>
<pre><code>{
  path: 'reports',
  loadComponent: () =&gt; import('./reports/reports.component')
    .then(c =&gt; c.ReportsComponent)
}</code></pre>
<p><strong>Note:</strong> This is route/code lazy loading — not EF Core lazy loading. See also <strong>Angular performance</strong> (Section 8) for OnPush, trackBy, and bundle tips.</p>
<h3>Interview Answer</h3>
<p>Lazy loading defers loading a feature until its route is visited, reducing initial bundle size. I use loadChildren or loadComponent in routing so heavy modules like admin aren't downloaded upfront.</p>""",

"q_angular_http_client": """<h2>How Do You Call APIs in Angular?</h2>
<p>Use <strong>HttpClient</strong> from <code>@angular/common/http</code>. It returns <strong>Observables</strong>, supports typed responses, interceptors, and error handling.</p>
<h3>Setup</h3>
<pre><code>import { provideHttpClient } from '@angular/common/http';

providers: [provideHttpClient()]</code></pre>
<h3>Service</h3>
<pre><code>@Injectable({ providedIn: 'root' })
export class CustomerService {
  constructor(private http: HttpClient) {}

  getCustomers(): Observable&lt;Customer[]&gt; {
    return this.http.get&lt;Customer[]&gt;('/api/customers');
  }

  createCustomer(customer: Customer): Observable&lt;Customer&gt; {
    return this.http.post&lt;Customer&gt;('/api/customers', customer);
  }
}</code></pre>
<h3>Component</h3>
<pre><code>this.customerService.getCustomers().subscribe({
  next: data =&gt; this.customers = data,
  error: err =&gt; this.handleError(err)
});

// Or in template: customers$ | async</code></pre>
<h3>Best practices</h3>
<ul>
<li>HTTP interceptor for JWT Bearer token and 401 refresh</li>
<li><code>environment.apiUrl</code> for base URL</li>
<li>Async pipe to avoid subscribe leaks</li>
</ul>
<p><strong>Related:</strong> Section 8 — HTTP Interceptor, JWT storage, Observable vs Promise.</p>
<h3>Interview Answer</h3>
<p>I inject HttpClient in a service, call get/post with typed Observables, and use subscribe or async pipe in the component. I add an interceptor to attach JWT tokens and handle errors globally.</p>""",
}
