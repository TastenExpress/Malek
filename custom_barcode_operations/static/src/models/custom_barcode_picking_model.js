/** @odoo-module **/
import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';


patch(BarcodePickingModel.prototype, 'stock_barcode_mrp_subcontracting', {


    updateLineNotes(virtualId, notes = "default notes") {
        this.actionMutex.exec(() => {
            const line = this.pageLines.find(l => l.virtual_id === virtualId);
            this.updateLine(line, {notes: notes});
            line.notes= notes;
            this.trigger('update');
        });
    },

});














