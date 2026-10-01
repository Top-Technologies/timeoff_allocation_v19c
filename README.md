# Time Off Allocation Enhancement & Balance Fix (`timeoff_allocation_v19c`)

## Overview
This custom module addresses two critical aspects of Time Off management in **Odoo 19 Community Edition**:

1. **FIFO Allocation Consumption (Earlier Allocation Deducted First)**:
   - When an employee holds multiple active allocations for the same time off type running simultaneously (e.g. carryover from previous period + new allocation, or multiple allocations granted during the year), approved leaves now deduct from the **earlier allocation first** before touching newer allocations.
   - Standard Odoo default searches order by `create_date desc` (newest first). This module overrides `_get_consumed_leaves` to order by:
     1. Allocation start date (`date_from` or `create_date`)
     2. Allocation expiration date (`date_to`)
     3. Allocation creation timestamp (`create_date`)
     4. Record ID (`id`)

2. **Manual Allocation Balance Adjustment & Remaining Balance**:
   - Adds `balance_adjustment` on `hr.leave.allocation` for recording days deducted manually (e.g. leaves taken outside the system, or negative for extra bonus days).
   - Adds editable `remaining_balance` on the allocation form. Modifying this field automatically updates `balance_adjustment` and logs an audit record to Chatter.
   - Synchronizes adjustments with Odoo's internal leave engine (`_get_consumed_leaves`) so available balances accurately reflect adjustments on:
     - Allocation form & list views
     - Time Off Dashboard cards
     - Employee profile `allocation_remaining_display`
     - Employee clearance reports (`hr_clearance`)
     - Leave request balance validation

## Installation / Update
To install or upgrade this module on your Odoo 19 instance:
```bash
/opt/odoo19/venv/bin/python3 /opt/odoo19/odoo/odoo-bin -c /etc/odoo19/odoo19.conf -d <database_name> -u timeoff_allocation_v19c --dev=all
```
