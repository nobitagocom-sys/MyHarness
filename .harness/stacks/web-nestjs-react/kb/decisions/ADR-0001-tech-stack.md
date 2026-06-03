# ADR-0001: Technology Stack

**Date:** 2026-06-03  
**Status:** Accepted

## Decision
Backend: NestJS (latest) + Node.js (latest LTS) + TypeScript (latest)  
Frontend: React (latest) + Vite (latest)  
Database: PostgreSQL (latest stable, production), SQLite (local dev)  
Cache: Redis (latest stable)  
ORM: Prisma (latest)  

Actual pinned versions live in `package.json` of each stack template — this ADR records the technology choices, not the version numbers.

## Rationale
NestJS provides structured DI and module system compatible with team conventions.
React + Vite gives fast HMR for frontend development.
Prisma enables portable schema between SQLite (dev) and PostgreSQL (prod).
Always using latest versions ensures security patches and new language features are available from project start.
