
/** @odoo-module **/

import LineComponent from '@stock_barcode/components/line';
import { patch } from 'web.utils';

patch(LineComponent.prototype, 'custom_barcode_operations', {
    addNotes(ev) {
        this.env.model.updateLineNotes(this.line.virtual_id,event.target.value);
    }
});