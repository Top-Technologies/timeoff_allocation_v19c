# -*- coding: utf-8 -*-
{
    'name': 'Time Off Allocation Enhancement & Balance Fix',
    'version': '19.0.1.0.0',
    'summary': 'FIFO deduction for simultaneous allocations and manual balance adjustment with chatter tracking',
    'description': """
Time Off Customization for Odoo 19 Community
=============================================
Key Features:
1. FIFO Allocation Deduction:
   - When an employee has multiple valid allocations for the same time off type
     running at the same time, approved time off requests automatically deduct from
     the earlier allocation first before starting to deduct from the newer one.
   - Ordering considers start dates (date_from), expiration dates (date_to), and
     creation dates to ensure strict priority.

2. Manual Allocation Balance Adjustment:
   - Allows HR managers and officers to manually adjust allocation balances
     (e.g., deducting days taken outside the system or adding compensation days).
   - Enables editing the "Remaining Balance" field directly on the allocation form,
     which automatically recalculates the adjustment amount.
   - Logs all manual balance changes to the allocation chatter with old and new values.

3. Complete Odoo 19 Integration:
   - Synchronizes adjustments with Odoo's internal leave consumption engine (_get_consumed_leaves),
     ensuring accurate available days on the Time Off Dashboard, employee cards,
     clearance reports, and leave validation checks.
    """,
    'category': 'Human Resources/Time Off',
    'author': 'Top Technologies',
    'license': 'LGPL-3',
    'depends': ['hr_holidays'],
    'data': [
        'views/hr_leave_allocation_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
