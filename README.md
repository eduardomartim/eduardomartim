<div align="center">

<img src="assets/header.svg" alt="Eduardo — Software Engineer | AI Systems | Agentic AI" width="100%">

</div>

<br>

I'm a software engineer focused on backend, full-stack and AI systems. I build applications end to end (architecture, implementation, automated tests, deployment) and I spend my time on the parts that are easy to get wrong: **who is allowed to do what, what a customer is charged, what happens when a message is delivered twice, and what an AI agent may and may not do.**

My rule of thumb: critical rules belong in code, in the database and in tests, not in a prompt or in the UI. That shows up in my repositories as a deterministic policy engine in front of LLM tool calls, PostgreSQL Row Level Security, signature-verified payment webhooks, transactional outbox messaging, and retrieval that refuses to answer without evidence.

I use AI coding assistants as part of my daily workflow. Nothing they produce is accepted without review, and each project is verified with its own tests, linters and manual checks.

<br>

<div align="center">

<img src="assets/system-scan.svg" alt="Terminal-style profile scan: Eduardo, Software Engineer. Focus: AI systems and agentic AI. Languages: Python, TypeScript, JavaScript. Backend: FastAPI, PostgreSQL, RabbitMQ, Redis. Frontend: Next.js, React, Vite, Tailwind. Data and auth: Supabase, Row Level Security, pgvector. Agents: LangGraph, MCP, RAG, policy engine." width="100%">

</div>

<div align="center">

<img src="assets/projects-panel.svg" alt="Projects list: Orquestrador-novamart, Asyncflow, E-commerce-voltstore and GTA-V-story-mode-ai" width="100%">

<sub>
<a href="https://github.com/eduardomartim/Orquestrador-novamart">Orquestrador-novamart</a> ·
<a href="https://github.com/eduardomartim/Asyncflow">Asyncflow</a> ·
<a href="https://github.com/eduardomartim/E-commerce-voltstore">E-commerce-voltstore</a> (<a href="https://voltstore-beta.vercel.app">demo</a>) ·
<a href="https://github.com/eduardomartim/GTA-V-story-mode-ai">GTA-V-story-mode-ai</a> (<a href="https://gta-v-story-mode-ai.vercel.app">demo</a>)
</sub>

</div>

<br>

## Tech stack

Technologies that appear in the projects above.

<table>
  <tr>
    <td><b>Languages</b></td>
    <td>
      <img src="https://skillicons.dev/icons?i=py,ts,js&theme=dark" alt="Python, TypeScript, JavaScript" height="44">
    </td>
  </tr>
  <tr>
    <td><b>Backend</b></td>
    <td>
      <img src="https://skillicons.dev/icons?i=fastapi,rabbitmq,redis&theme=dark" alt="FastAPI, RabbitMQ, Redis" height="44"><br>
      <sub>SQLAlchemy · Alembic · Starlette · Stripe API</sub>
    </td>
  </tr>
  <tr>
    <td><b>Frontend</b></td>
    <td>
      <img src="https://skillicons.dev/icons?i=react,nextjs,vite,tailwind&theme=dark" alt="React, Next.js, Vite, Tailwind CSS" height="44">
    </td>
  </tr>
  <tr>
    <td><b>Data &amp; auth</b></td>
    <td>
      <img src="https://skillicons.dev/icons?i=postgres,supabase&theme=dark" alt="PostgreSQL, Supabase" height="44"><br>
      <sub>Row Level Security · pgvector · SQLite FTS5</sub>
    </td>
  </tr>
  <tr>
    <td><b>AI &amp; agents</b></td>
    <td>
      LangGraph · Google Gemini · Model Context Protocol (MCP) · Retrieval-augmented generation · LLM provider adapters (Anthropic, OpenAI, Google)
    </td>
  </tr>
  <tr>
    <td><b>Quality &amp; delivery</b></td>
    <td>
      <img src="https://skillicons.dev/icons?i=vitest,githubactions,docker,git,vercel&theme=dark" alt="Vitest, GitHub Actions, Docker, Git, Vercel" height="44"><br>
      <sub>pytest · Playwright · pgTAP · Ruff · mypy · ESLint</sub>
    </td>
  </tr>
</table>

<br>

## Engineering focus

- **AI systems with guardrails:** policy-controlled tool execution, human approval, audit trails, grounded retrieval and evaluation harnesses.
- **Reliable backends:** transactional outbox, idempotency, retries with backoff, dead-letter queues and explicit delivery guarantees.
- **Security at the data layer:** Row Level Security, server-side pricing, signed webhooks and tests that try to break the rules.
- **Full-stack delivery:** typed interfaces, responsive UIs, CI pipelines and live deployments.

## How I build

1. **Define the invariants first.** What must never happen (an oversold item, a cross-tenant read, an unapproved write)?
2. **Put each rule where it can be enforced:** the database, a gateway or a policy engine, not only the interface.
3. **Build with AI assistants, then review everything.** I read, question and simplify generated code before it lands.
4. **Prove it.** Unit, integration, end-to-end and adversarial tests, run against real services where it matters.
5. **Document the limits.** Each README says what is simulated, untested or still open.

<br>

<div align="center">

[**All repositories →**](https://github.com/eduardomartim?tab=repositories)

</div>
