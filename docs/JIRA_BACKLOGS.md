# Jira Backlogs & Sprint Planning
## POS Simulator Project

**Project:** Point of Sale (POS) Simulator  
**Date:** November 16, 2025  
**Team:** Narayana S, Mithun Naik, Dimpu Kumar, Darshan H V  
**Methodology:** Agile Scrum  

---

## Project Overview

**Project Duration:** 4 weeks (2 sprints)  
**Sprint Length:** 2 weeks each  
**Team Velocity:** ~40 story points per sprint  

---

## Epic Structure

### EPIC-1: Cashier Operations
**Goal:** Core checkout flows used by cashiers  
**Business Value:** High - Essential for daily operations  
**Stories:** 6  
**Total Story Points:** 34  

### EPIC-2: Manager & Admin Operations  
**Goal:** Refunds, overrides, reporting, inventory management  
**Business Value:** High - Critical for supervision and management  
**Stories:** 6  
**Total Story Points:** 36  

### EPIC-3: Security, Performance & Delivery
**Goal:** Auth, RBAC, tests, CI/CD, deployment, monitoring  
**Business Value:** High - Production readiness  
**Stories:** 2  
**Total Story Points:** 8  

**Total Project:** 3 Epics, 14 User Stories, 78 Story Points

---

## Product Backlog

### Sprint 1: Core Cashier Features

#### US-01: Add Product to Cart
**Epic:** EPIC-1 (Cashier Operations)  
**Priority:** High  
**Story Points:** 5  
**Sprint:** Sprint 1  

**User Story:**
```
As a cashier,
I want to add products to the cart using barcode or manual entry
So that I can quickly create a customer order
```

**Acceptance Criteria:**
1. ✅ Cashier can scan or paste barcode and product appears in cart
2. ✅ Product shows name, price, SKU, tax class
3. ✅ Manual add UI accepts SKU or product name with autocomplete
4. ✅ Invalid SKU shows error and prevents add
5. ✅ Stock validation before adding to cart

**Tasks:**
- [x] Create cart API endpoint (`/api/cart/add`)
- [x] Implement barcode input field
- [x] Build autocomplete search component
- [x] Add validation logic
- [x] Create unit tests
- [x] Integration testing

**Definition of Done:**
- [x] Code reviewed and merged
- [x] Unit tests passing
- [x] API tested
- [x] Documented

**Status:** ✅ **DONE**

---

#### US-02: Manage Cart & Quantities
**Epic:** EPIC-1  
**Priority:** High  
**Story Points:** 3  
**Sprint:** Sprint 1  

**User Story:**
```
As a cashier,
I want to maintain a cart with multiple items and quantities
So that I can handle multi-item orders
```

**Acceptance Criteria:**
1. ✅ Update quantity increments/decrements update subtotal instantly
2. ✅ Remove item updates totals and UI
3. ✅ Cart persists locally (session) until checkout completes
4. ✅ Cart displays all items with details

**Tasks:**
- [x] Create cart state management (React)
- [x] Build quantity control components
- [x] Implement remove item functionality
- [x] Add clear cart feature
- [x] API endpoints: `/api/cart/update`, `/api/cart/remove`
- [x] Session persistence

**Status:** ✅ **DONE**

---

#### US-03: Tax & Discount Calculation
**Epic:** EPIC-1  
**Priority:** Highest  
**Story Points:** 8  
**Sprint:** Sprint 1  

**User Story:**
```
As a cashier,
I want automatic calculation of subtotal, discounts, and taxes
So that customers see accurate totals
```

**Acceptance Criteria:**
1. ✅ Item-level and order-level discounts supported
2. ✅ Tax rules applied per item tax class
3. ✅ Totals match business rules
4. ✅ Calculations visible in UI and API responses
5. ✅ Real-time updates (< 200ms)

**Tasks:**
- [x] Implement tax calculation logic
- [x] Create discount application system
- [x] Build pricing breakdown UI component
- [x] Unit tests for calculation accuracy
- [x] Edge case testing (negative values, large numbers)

**Status:** ✅ **DONE**

---

#### US-04: Stock Validation Before Checkout
**Epic:** EPIC-1  
**Priority:** High  
**Story Points:** 5  
**Sprint:** Sprint 1  

**User Story:**
```
As a cashier,
I want stock validated before checkout
So that I don't sell out-of-stock items
```

**Acceptance Criteria:**
1. ✅ Checkout blocked if requested quantity > available stock
2. ✅ On checkout success, stock reduced in DB (transactional)
3. ✅ Clear error message indicating stock issue
4. ✅ Real-time stock checking

**Tasks:**
- [x] Add stock validation in checkout API
- [x] Implement transactional inventory updates
- [x] Create error handling for insufficient stock
- [x] Build UI error display
- [x] Test race conditions

**Status:** ✅ **DONE**

---

#### US-05: Mock Payment Processing
**Epic:** EPIC-1  
**Priority:** Highest  
**Story Points:** 8  
**Sprint:** Sprint 1  

**User Story:**
```
As a cashier,
I want to process mock payments (cash, card, UPI)
So that I can complete sales
```

**Acceptance Criteria:**
1. ✅ Payment API accepts payment type and returns success/failure
2. ✅ On success, sale is recorded and receipt generated
3. ✅ On failure, rollback sale and show error
4. ✅ Three payment methods supported (cash, card, UPI)
5. ✅ Change calculated for cash payments

**Tasks:**
- [x] Create payment simulator module
- [x] Build checkout API (`/api/checkout/process`)
- [x] Implement transaction rollback logic
- [x] Create payment method UI
- [x] Test success and failure scenarios

**Status:** ✅ **DONE**

---

#### US-06: PDF Receipt Generation & Sale Recording
**Epic:** EPIC-1  
**Priority:** Medium  
**Story Points:** 5  
**Sprint:** Sprint 1  

**User Story:**
```
As a cashier,
I want to generate PDF receipts and record sales
So that customers get proof of purchase
```

**Acceptance Criteria:**
1. ✅ On payment success, DB stores transaction with unique ID
2. ✅ PDF receipt generated with all transaction details
3. ✅ Receipt downloadable/printable
4. ✅ Transaction stored with line items

**Tasks:**
- [x] Integrate ReportLab for PDF generation
- [x] Create receipt template
- [x] Build transaction model
- [x] Implement transaction_items relationship
- [x] Add receipt download endpoint
- [x] Test PDF generation

**Status:** ✅ **DONE**

---

**Sprint 1 Summary:**
- **Stories Completed:** 6/6
- **Story Points:** 34/34
- **Status:** ✅ **100% COMPLETE**

---

### Sprint 2: Manager & Admin Features

#### US-07: Refund & Void Transactions
**Epic:** EPIC-2 (Manager Operations)  
**Priority:** Medium  
**Story Points:** 8  
**Sprint:** Sprint 2  

**User Story:**
```
As a manager,
I want to perform refunds and voids
So that I can correct erroneous sales
```

**Acceptance Criteria:**
1. ✅ Refund references original transaction ID
2. ✅ Refund updates database
3. ✅ Refund triggers inventory restock
4. ✅ Access restricted to Manager role
5. ✅ Partial refunds supported
6. ✅ Refund reason required

**Tasks:**
- [x] Create Refund model
- [x] Build refund API endpoints (`/api/refunds/*`)
- [x] Implement inventory restock logic
- [x] Create Refunds.jsx page
- [x] Add refund authorization check
- [x] Build refund search functionality

**Status:** ✅ **DONE**

---

#### US-08: Manager Override for Restricted Actions
**Epic:** EPIC-2  
**Priority:** Low  
**Story Points:** 5  
**Sprint:** Sprint 2  

**User Story:**
```
As a manager,
I want to authorize restricted actions
So that I can approve large discounts
```

**Acceptance Criteria:**
1. ✅ System prompts for manager credential when restricted action attempted
2. ✅ Action logs user ID and timestamp
3. ✅ PIN verification required
4. ✅ All overrides audit logged

**Tasks:**
- [x] Create ManagerOverride.jsx component
- [x] Build PIN verification API (`/api/auth/verify-pin`)
- [x] Implement audit logging
- [x] Add PIN field to User model
- [x] Test authorization flow

**Status:** ✅ **DONE**

---

#### US-09: Automatic Inventory Update
**Epic:** EPIC-2  
**Priority:** High  
**Story Points:** 5  
**Sprint:** Sprint 2  

**User Story:**
```
As an admin,
I want inventory updated after sale/refund
So that stock levels stay accurate
```

**Acceptance Criteria:**
1. ✅ Inventory read/write transactional behavior verified with tests
2. ✅ API endpoints for inventory adjustment exist for admin
3. ✅ All changes logged to inventory_logs
4. ✅ Transactional integrity maintained

**Tasks:**
- [x] Create InventoryLog model
- [x] Implement automatic inventory updates
- [x] Add transaction wrapping
- [x] Build inventory adjustment API
- [x] Test concurrent transactions

**Status:** ✅ **DONE**

---

#### US-10: Reports & Sales History Search
**Epic:** EPIC-2  
**Priority:** Low  
**Story Points:** 8  
**Sprint:** Sprint 2  

**User Story:**
```
As a manager,
I want daily reports and sales search
So that I can review performance
```

**Acceptance Criteria:**
1. ✅ Generate CSV and PDF reports by date range, cashier, product
2. ✅ Search API returns transactions filtered by criteria
3. ✅ Reports exportable
4. ✅ Report generation < 5 seconds

**Tasks:**
- [x] Create Reports.jsx page
- [x] Build report API endpoints (`/api/reports/*`)
- [x] Implement CSV export
- [x] Implement PDF export
- [x] Add date range picker
- [x] Build search filters

**Status:** ✅ **DONE**

---

#### US-11: Role-Based Access Control
**Epic:** EPIC-2  
**Priority:** High  
**Story Points:** 5  
**Sprint:** Sprint 2  

**User Story:**
```
As an admin,
I want RBAC to ensure only authorized actions are allowed
```

**Acceptance Criteria:**
1. ✅ Roles: Cashier, Manager, Admin with permissions matrix
2. ✅ APIs enforce permission checks
3. ✅ UI hides restricted actions
4. ✅ 403 Forbidden for unauthorized access

**Tasks:**
- [x] Define role enum in User model
- [x] Implement permission checking decorator
- [x] Add JWT role claims
- [x] Build frontend permission checks
- [x] Test all role scenarios

**Status:** ✅ **DONE**

---

#### US-12: Secure Login & Credential Encryption
**Epic:** EPIC-3 (Security)  
**Priority:** Highest  
**Story Points:** 8  
**Sprint:** Sprint 2  

**User Story:**
```
As an admin,
I want secure login, encrypted credentials, and logging
So that the system is protected
```

**Acceptance Criteria:**
1. ✅ Passwords hashed (bcrypt) in DB
2. ✅ Login returns JWT
3. ✅ Failed attempts logged
4. ✅ 5 failed attempts → lockout (configurable)
5. ✅ Refresh tokens supported

**Tasks:**
- [x] Implement bcrypt password hashing
- [x] Create JWT authentication
- [x] Build RefreshToken model
- [x] Add failed login tracking
- [x] Implement account lockout
- [x] Create auth API endpoints

**Status:** ✅ **DONE**

---

#### US-13: Fast Checkout & Data Consistency
**Epic:** EPIC-3  
**Priority:** High  
**Story Points:** 5  
**Sprint:** Sprint 2  

**User Story:**
```
As a cashier,
I want fast and consistent checkout
```

**Acceptance Criteria:**
1. ✅ 90% of checkout ops < 2s under load
2. ✅ No data inconsistency across 100 transactions
3. ✅ Database transactions ensure atomicity

**Tasks:**
- [x] Optimize database queries
- [x] Add database indexes
- [x] Implement connection pooling
- [x] Test with stress testing
- [x] Verify data consistency

**Status:** ✅ **DONE**

---

#### US-14: Simple & Intuitive UI
**Epic:** EPIC-3  
**Priority:** Medium  
**Story Points:** 3  
**Sprint:** Sprint 2  

**User Story:**
```
As a cashier,
I want a simple UI with tooltips
```

**Acceptance Criteria:**
1. ✅ Tooltips available for key actions
2. ✅ UI passes basic usability test
3. ✅ Accessibility checks (keyboard navigation, labels)
4. ✅ Responsive design

**Tasks:**
- [x] Apply TailwindCSS styling
- [x] Add tooltips to components
- [x] Implement responsive grid
- [x] Test keyboard navigation
- [x] Conduct usability testing

**Status:** ✅ **DONE**

---

**Sprint 2 Summary:**
- **Stories Completed:** 8/8
- **Story Points:** 44/44
- **Status:** ✅ **100% COMPLETE**

---

## Sprint Reports

### Sprint 1 Report

**Sprint Duration:** Weeks 1-2  
**Sprint Goal:** Implement core cashier checkout functionality  

**Planned vs. Actual:**
- Planned Story Points: 34
- Completed Story Points: 34
- Completion Rate: 100%

**Burndown Chart:**
```
Story Points
34 |■
30 |  ■
25 |    ■
20 |      ■
15 |        ■
10 |          ■
 5 |            ■
 0 |______________■
   D1 D3 D5 D7 D9
```

**Completed User Stories:**
- ✅ US-01: Add Product to Cart (5 SP)
- ✅ US-02: Manage Cart & Quantities (3 SP)
- ✅ US-03: Tax & Discount Calculation (8 SP)
- ✅ US-04: Stock Validation (5 SP)
- ✅ US-05: Mock Payment Processing (8 SP)
- ✅ US-06: PDF Receipt Generation (5 SP)

**Key Achievements:**
- Complete checkout workflow functional
- Payment simulator integrated
- PDF receipt generation working
- Real-time cart calculations
- Stock validation implemented

**Challenges:**
- Tax calculation edge cases required additional testing
- Payment rollback logic needed refinement

**Team Velocity:** 34 story points

**Sprint Retrospective:**
- **What Went Well:** Clear requirements, good teamwork, rapid progress
- **What Could Improve:** Earlier testing of edge cases
- **Action Items:** Increase test coverage for Sprint 2

---

### Sprint 2 Report

**Sprint Duration:** Weeks 3-4  
**Sprint Goal:** Implement manager/admin features and security  

**Planned vs. Actual:**
- Planned Story Points: 44
- Completed Story Points: 44
- Completion Rate: 100%

**Burndown Chart:**
```
Story Points
44 |■
40 |  ■
35 |    ■
30 |      ■
25 |        ■
20 |          ■
15 |            ■
10 |              ■
 5 |                ■
 0 |__________________■
   D1 D2 D3 D4 D5 D6 D7 D8 D9 D10
```

**Completed User Stories:**
- ✅ US-07: Refund & Void (8 SP)
- ✅ US-08: Manager Override (5 SP)
- ✅ US-09: Inventory Updates (5 SP)
- ✅ US-10: Reports & Search (8 SP)
- ✅ US-11: RBAC (5 SP)
- ✅ US-12: Secure Login (8 SP)
- ✅ US-13: Performance (5 SP)
- ✅ US-14: UI Usability (3 SP)

**Key Achievements:**
- Complete refund system implemented
- Manager override with PIN verification
- Comprehensive reporting module
- JWT authentication with refresh tokens
- Role-based access control fully functional
- Performance optimization completed
- All security requirements met

**Challenges:**
- Complex refund logic with inventory restocking
- Manager override authorization flow needed multiple iterations
- Performance testing revealed optimization opportunities

**Team Velocity:** 44 story points (improved from Sprint 1)

**Sprint Retrospective:**
- **What Went Well:** Excellent team collaboration, high productivity, all goals met
- **What Could Improve:** More comprehensive performance testing earlier
- **Action Items:** Document lessons learned for future projects

---

## Project Summary

### Overall Project Statistics

**Duration:** 4 weeks (2 sprints)  
**Total User Stories:** 14  
**Total Story Points:** 78  
**Completed:** 78 (100%)  
**Average Velocity:** 39 SP per sprint  

**Epic Completion:**
- ✅ EPIC-1: Cashier Operations (34 SP) - 100%
- ✅ EPIC-2: Manager & Admin (36 SP) - 100%
- ✅ EPIC-3: Security & Performance (8 SP) - 100%

**Quality Metrics:**
- Test Coverage: 70%+
- Defects Found: 0 critical, 0 high
- Code Reviews: 100% completed
- Documentation: Comprehensive

---

## Backlog Grooming Notes

### Backlog Refinement Sessions

**Session 1 (Week 0):**
- Reviewed PROJECT_SPEC.md requirements
- Broke down epics into user stories
- Estimated story points using planning poker
- Prioritized backlog

**Session 2 (Week 2):**
- Refined Sprint 2 stories
- Clarified acceptance criteria
- Identified dependencies
- Updated estimates

**Estimation Technique:** Planning Poker (Fibonacci sequence: 1, 2, 3, 5, 8, 13)

**Story Point Guidelines:**
- 1 SP = Few hours of work
- 3 SP = 1 day of work
- 5 SP = 2-3 days of work
- 8 SP = 4-5 days of work
- 13 SP = Full week (needs breakdown)

---

## Definition of Ready (DoR)

Before a story enters a sprint:
- ✅ User story clearly written
- ✅ Acceptance criteria defined
- ✅ Story estimated by team
- ✅ Dependencies identified
- ✅ Technical approach discussed
- ✅ Testable

---

## Definition of Done (DoD)

A story is complete when:
- ✅ Code written and reviewed
- ✅ Unit tests written and passing
- ✅ Integration tests passing
- ✅ Acceptance criteria met
- ✅ Documentation updated
- ✅ Deployed to test environment
- ✅ Demo ready

---

## Jira Board Structure

### Board Columns

1. **Backlog** - Prioritized list of future work
2. **Selected for Development** - Sprint backlog
3. **In Progress** - Actively being worked on
4. **Code Review** - PR submitted, awaiting review
5. **Testing** - QA testing in progress
6. **Done** - Meets DoD, ready for release

### Swim Lanes

- Epic 1: Cashier Operations
- Epic 2: Manager Operations
- Epic 3: Security & Performance
- Bugs
- Technical Debt

---

## Team Ceremonies

### Daily Standup (15 minutes)
**Questions:**
- What did I complete yesterday?
- What will I work on today?
- Any blockers?

**Frequency:** Daily at 10:00 AM

---

### Sprint Planning (2 hours)
**Activities:**
- Review sprint goal
- Select user stories from backlog
- Break down stories into tasks
- Commit to sprint backlog

**Frequency:** First day of sprint

---

### Sprint Review/Demo (1 hour)
**Activities:**
- Demo completed features
- Gather stakeholder feedback
- Update product backlog

**Frequency:** Last day of sprint

---

### Sprint Retrospective (1 hour)
**Activities:**
- What went well?
- What could be improved?
- Action items for next sprint

**Frequency:** After sprint review

---

### Backlog Refinement (1 hour)
**Activities:**
- Clarify upcoming stories
- Estimate new stories
- Prioritize backlog

**Frequency:** Mid-sprint

---

## Velocity Tracking

| Sprint | Planned SP | Completed SP | Velocity |
|--------|-----------|--------------|----------|
| Sprint 1 | 34 | 34 | 34 |
| Sprint 2 | 44 | 44 | 44 |
| **Average** | **39** | **39** | **39** |

**Trend:** ↗️ Increasing velocity (team improving)

---

## Risk Register

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Scope creep | Low | High | Strict backlog grooming | Product Owner |
| Technical debt | Medium | Medium | Regular refactoring | Dev Team |
| Integration issues | Low | High | Early integration testing | Dev Team |
| Resource unavailability | Low | Medium | Cross-training | Scrum Master |

---

## Release Plan

### Release 1.0 (Current)

**Target Date:** November 16, 2025  
**Status:** ✅ **RELEASED**

**Included Features:**
- All 14 user stories
- Complete POS functionality
- Manager overrides
- Refund system
- Reporting module
- Security features

**Release Notes:**
- See FINAL_REPORT.md for complete details

---

## Future Backlog (Post-MVP)

### Potential Enhancements (Not Committed)

**P3 - Low Priority:**
- Multiple payment methods in single transaction
- Customer loyalty program integration
- Advanced analytics dashboard
- Mobile responsive improvements
- Barcode scanner hardware integration
- Cloud synchronization
- Multi-store support

**Technical Improvements:**
- Microservices architecture
- Real-time notifications
- Advanced caching
- API rate limiting
- GraphQL API option

---

## Stakeholder Communication

### Status Reports

**Weekly Status Email:**
- Sprint progress update
- Completed stories
- Upcoming work
- Risks/issues
- Velocity trending

**Distribution List:**
- Course evaluators
- Project sponsors
- Team members

---

## Conclusion

✅ **Project Successfully Completed**

**Achievements:**
- 100% of planned user stories delivered
- Zero critical defects
- High-quality codebase
- Comprehensive documentation
- Production-ready system

**Team Performance:**
- Consistent velocity
- Excellent collaboration
- High code quality
- Strong commitment to quality

**Next Steps:**
- Final demo and review
- Production deployment
- Post-implementation support
- Lessons learned documentation

---

**Document Status:** ✅ Final  
**Last Updated:** November 16, 2025  
**Maintained By:** Scrum Master (Narayana S)  

---

*End of Jira Backlogs & Sprint Planning Document*
