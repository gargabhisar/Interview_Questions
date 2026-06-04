ANSWERS = {
"q_cicd_pipeline": """<h2>CI/CD Pipeline</h2>
<p>A <strong>CI/CD pipeline</strong> is an automated workflow used in software development to <strong>build</strong>, <strong>test</strong>, and <strong>deploy</strong> code changes quickly and reliably.</p>
<h3>CI = Continuous Integration</h3>
<p>Developers frequently merge code into a shared repository. Whenever new code is pushed:</p>
<ol>
<li>Code is compiled / built</li>
<li>Automated tests run</li>
<li>Bugs and errors are detected early</li>
</ol>
<p><strong>Goal:</strong> Catch issues early and keep the codebase stable.</p>
<h3>CD = Continuous Delivery / Continuous Deployment</h3>
<p>After CI succeeds, the application is automatically prepared for release.</p>
<table>
<tr><th>Term</th><th>Meaning</th></tr>
<tr><td><strong>Continuous Delivery</strong></td><td>Code is automatically tested and packaged; deployment to production still requires <strong>manual approval</strong></td></tr>
<tr><td><strong>Continuous Deployment</strong></td><td>Code is automatically deployed to production <strong>without</strong> manual intervention</td></tr>
</table>
<h3>Typical CI/CD flow</h3>
<pre><code>Developer Pushes Code
        ↓
Source Control (GitHub / GitLab / Bitbucket)
        ↓
Build Stage
        ↓
Automated Testing
        ↓
Code Quality / Security Checks
        ↓
Package Artifact (Docker / JAR / etc.)
        ↓
Deploy to Staging
        ↓
Deploy to Production</code></pre>
<h3>Common tools</h3>
<table>
<tr><th>Purpose</th><th>Tools</th></tr>
<tr><td>Source control</td><td>GitHub, GitLab, Bitbucket</td></tr>
<tr><td>CI/CD</td><td>Jenkins, GitHub Actions, GitLab CI/CD, CircleCI, Azure DevOps</td></tr>
<tr><td>Containerization</td><td>Docker</td></tr>
<tr><td>Orchestration</td><td>Kubernetes</td></tr>
<tr><td>Cloud deployment</td><td>AWS, Azure, GCP</td></tr>
</table>
<h3>Example: GitHub Actions (.NET)</h3>
<pre><code>name: CI Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: 8.0.x
      - name: Restore Packages
        run: dotnet restore
      - name: Build
        run: dotnet build --no-restore
      - name: Run Tests
        run: dotnet test --no-build</code></pre>
<h3>Benefits</h3>
<ul>
<li>Faster releases</li>
<li>Reduced manual work</li>
<li>Early bug detection</li>
<li>Better code quality</li>
<li>Reliable deployments and easier rollback</li>
</ul>
<h3>Interview Answer</h3>
<p>CI/CD automates the software delivery process. CI runs build and tests on every commit so issues are caught early. CD packages and deploys to staging or production—either with manual approval (Continuous Delivery) or fully automatic (Continuous Deployment). In .NET projects I have used GitHub Actions or Azure DevOps for restore, build, test, and deploy stages.</p>""",
}
