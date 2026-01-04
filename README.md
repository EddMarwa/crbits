Corebits – Investment Platform (MVP)
Overview

Corebits is a dark-themed, serious investment platform that allows users to deposit funds, allocate them to pooled trading bots, and earn returns based on real trading performance.

The platform is designed with ledger-based accounting, auditability, and future regulatory compliance in mind.

This repository contains the MVP implementation intended for controlled testing before scaling to full production.

Core Principles

No guaranteed returns

Ledger-first accounting

Pooled fund management

Transparency and auditability

Security over speed

MVP now, scalable later

Technology Stack
Backend

Python

FastAPI

PostgreSQL

SQLAlchemy

JWT Authentication

Frontend

HTML

CSS

Vanilla JavaScript

REST API–driven

How Corebits Works
User Flow

User registers and logs in

User deposits funds via crypto

Funds are credited via ledger entries

User allocates funds to a trading bot

Bots trade pooled capital

Profits/losses are distributed proportionally

User can request withdrawals

Accounting Model (Very Important)

Corebits uses a ledger-based accounting system.

Balances are never stored

Every transaction is immutable

User balance is calculated as:

SUM(ledger.amount WHERE status = confirmed)

Ledger Transaction Types

Deposit

Profit

Loss

Withdrawal

Platform Fee

This design ensures accuracy, auditability, and legal defensibility.

Trading Bots

Each bot manages a shared pool of funds

Users allocate funds to bots

Bots execute trades (semi-automated, manually supervised)

PnL is calculated per cycle

Distribution is proportional to allocation

Dashboard Features (MVP)

Total invested capital

Current account value

Profit/Loss

ROI percentage

Bot allocations

Transaction history

Security Measures (MVP)

JWT authentication

Role-based access control

Manual withdrawal approvals

KYC required before withdrawals

Admin action logging

Roadmap
Phase 1 – MVP (Build First)

✅ User authentication
✅ Ledger system
✅ Crypto deposits
✅ Bot fund pooling
✅ PnL distribution
✅ Dashboard analytics
✅ Manual withdrawals

Phase 2 – Stability & Trust

⬜ Automated blockchain listeners
⬜ Improved bot performance analytics
⬜ Admin dashboards
⬜ Rate limiting & alerts
⬜ Email notifications

Phase 3 – Compliance & Scale

⬜ Full KYC/AML integration
⬜ Fiat payment gateways
⬜ Strategy-level transparency
⬜ Regulatory compliance tooling
⬜ Investor reports (PDF/CSV)

Phase 4 – Global Expansion

⬜ Multi-currency support
⬜ Multi-region compliance
⬜ Mobile-first UI
⬜ Advanced projections
⬜ Public performance pages

Disclaimer

Corebits does not guarantee profits. All investments carry risk. Projections are estimates based on historical data and market conditions.

Final Notes

This MVP is intentionally conservative, transparent, and audit-focused.
Excitement is optional. Trust is mandatory.