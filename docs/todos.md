# Document Copilot — Implementation Plan

Based on `docs/architecture.md` 13-step sequence. Each phase depends on the previous.

---

## Phase 0: Prerequisites

- [ ] Add real OpenAI API key to `backend/.env` (currently placeholder)
- [ ] Scaffold frontend: Vite + React + TypeScript + Tailwind + shadcn/ui (`docs/guides/frontend-setup.md`)

## Phase 1: Backend Foundation

- [x] Create `backend/app/` package: `main.py` (FastAPI app entrypoint), `config.py` (pydantic-settings)
- [x] Add SQLAlchemy models for all 6 tables: `profiles`, `chat_threads`, `chat_messages`, `message_citations`, `source_documents`, `document_chunks`
- [x] Set up Alembic (`alembic.ini`, `alembic/env.py`) wired to Supabase Postgres
- [x] Write and run first migration: enable `pgvector` extension, create all tables

## Phase 2: Auth

- [ ] Backend: Supabase JWT verification dependency (`app/auth/dependencies.py`)
- [ ] Frontend: Supabase Auth client, login/signup pages, session management

## Phase 3: API Client + Chat Skeleton

- [ ] Frontend: shared HTTP client with automatic bearer-token injection (`src/lib/http.ts`, `src/lib/api.ts`)
- [ ] Backend: chat streaming endpoint with stubbed assistant response (`app/api/chat.py`)
- [ ] Frontend: AI SDK chat UI pointed at FastAPI streaming endpoint

## Phase 4: Document Ingestion

- [ ] Build ingestion pipeline: Markdown extraction from HTML filings, chunking strategy, OpenAI embeddings, Supabase writes (`ingest/`)
- [ ] Run ingestion on all 25 downloaded 10-K filings
- [ ] Verify chunks + embeddings + FTS vectors in Supabase

## Phase 5: Retrieval

- [ ] Semantic search with `pgvector` cosine similarity (`app/retrieval/queries.py`)
- [ ] Postgres full-text search (`app/retrieval/fts.py`)
- [ ] Python RRF (Reciprocal Rank Fusion) to merge result sets (`app/retrieval/fusion.py`, `app/retrieval/retriever.py`)

## Phase 6: AI Agent

- [ ] PydanticAI document agent with typed dependencies and typed answer output (`app/assistant/`)
- [ ] Wire agent into chat endpoint with retrieval context
- [ ] Citation validation and grounding enforcement (`app/grounding/validator.py`)

## Phase 7: UI Polish

- [ ] Citation display组件: source passages, document references
- [ ] Empty states and error handling in chat UI
- [ ] Final end-to-end testing: upload → ingest → query → grounded answer with citations
