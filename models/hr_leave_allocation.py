# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round


class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    _duration_check = models.Constraint(
        "CHECK( ( number_of_days >= 0 AND allocation_type='regular') or (allocation_type != 'regular'))",
        'The duration must be greater than or equal to 0.',
    )

    balance_adjustment = fields.Float(
        string='Balance Adjustment',
        default=0.0,
        tracking=True,
        help='Extra days/hours deducted manually (e.g. leaves taken outside the system, or negative to grant bonus days).'
    )
    remaining_balance = fields.Float(
        string='Remaining Balance',
        compute='_compute_remaining_balance',
        inverse='_set_remaining_balance',
        store=False,
        help="Current remaining balance of this allocation. You can edit this directly to adjust the allocation balance."
    )

    @api.depends('number_of_days_display', 'number_of_hours_display', 'type_request_unit', 'leaves_taken', 'balance_adjustment')
    def _compute_remaining_balance(self):
        for alloc in self:
            total = alloc.number_of_hours_display if alloc.type_request_unit == 'hour' else alloc.number_of_days_display
            alloc.remaining_balance = float_round(
                total - alloc.leaves_taken - alloc.balance_adjustment,
                precision_digits=2
            )

    def _set_remaining_balance(self):
        for alloc in self:
            total = alloc.number_of_hours_display if alloc.type_request_unit == 'hour' else alloc.number_of_days_display
            old_balance = float_round(total - alloc.leaves_taken - alloc.balance_adjustment, precision_digits=2)
            new_balance = float_round(alloc.remaining_balance, precision_digits=2)
            new_adjustment = float_round(total - alloc.leaves_taken - new_balance, precision_digits=2)
            alloc.balance_adjustment = new_adjustment
            if old_balance != new_balance and isinstance(alloc.id, int):
                unit = _('hour(s)') if alloc.type_request_unit == 'hour' else _('day(s)')
                alloc.message_post(
                    body=_("Balance manually changed from %s to %s %s (Balance adjustment updated to %s %s).") % (
                        old_balance, new_balance, unit, new_adjustment, unit
                    )
                )
