# Open Manus

An alternative to Manus.im

## Key References

- [OpenAI Agent SDK](https://openai.github.io/openai-agents-python/)
- [Compute use](https://github.com/browser-use/browser-use)
- [Sandbox](https://github.com/vndee/llm-sandbox)
- [MCP]
- [Artifacts]

## Tech Stack

### Frontend

- [Next.js](https://nextjs.org)
- [NextAuth.js](https://next-auth.js.org)
- [Prisma](https://prisma.io)
- [Tailwind CSS](https://tailwindcss.com)
- [tRPC](https://trpc.io)

### Backend

- [LangGraph](https://langchain.com/langgraph)
- [Compute use](https://github.com/browser-use/browser-use)
- [Sandbox](https://github.com/vndee/llm-sandbox)
- [Multi-agents](https://github.com/geekan/MetaGPT)

## Get Started

### 1. Clone the Repository

```sh
git clone https://github.com/Yat3s/open-manus.git
cd open-manus
```

### 2. Install Dependencies

```sh
pnpm install
```

### 3. Set Up Environment Variables

```sh
cp .env.example .env
```

### 4. Run the Development Server

```sh
pnpm dev
```

The frontend will be available at `http://localhost:3000`

### 5. Set Up Python Virtual Environment

```sh
python -m venv venv
source venv/bin/activate
```

### 6. Install Backend Dependencies

```sh
pip install -e .
```

### 7. Run the Backend Service

```sh
fastapi dev src/core
```

The backend will be available at `http://localhost:8000`.
