/** @odoo-module **/
import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';
import Session from 'web.session';


patch(BarcodePickingModel.prototype, 'stock_barcode_mrp_subcontracting', {


    updateLineNotes(virtualId, notes = "default notes") {
        this.actionMutex.exec(() => {
            const line = this.pageLines.find(l => l.virtual_id === virtualId);
            this.updateLine(line, {notes: notes});
            line.notes= notes;
            this.trigger('update');
        });
    },



    _getFieldToWrite() {
        return [
            'location_id',
            'location_dest_id',
            'lot_id',
            'lot_name',
            'package_id',
            'owner_id',
            'qty_done',
            'result_package_id',
            'notes'
        ];
    },

    async processBarcode(barcode) {
        this.actionMutex.exec(() => {
            this._processBarcode(barcode);
             Session.rpc(
                '/stock_barcode/save_barcode_scan_time',
                {
                    model:this.params.model,
                    res_id:this.params.id,
                });
        });
    },

    async _parseBarcode(barcode, filters) {
    debugger;
        const result = {
            barcode,
            match: false,
        };
        // First, simply checks if the barcode is an action.
        if (this.commands[barcode]) {
            result.action = this.commands[barcode];
            result.match = true;
            return result; // Simple barcode, no more information to retrieve.
        }
        // Then, parses the barcode through the nomenclature.
        await this.parser.is_loaded();
        try {
            const parsedBarcode = this.parser.parse_barcode(barcode);
            if (parsedBarcode.length) { // With the GS1 nomenclature, the parsed result is a list.
                for (const data of parsedBarcode) {
                    const { rule, value } = data;
                    if (['location', 'location_dest'].includes(rule.type)) {
                        const location = await this.cache.getRecordByBarcode(value, 'stock.location');
                        if (!location) {
                            continue;
                        }
                        // TODO: should be overrided, as location dest make sense only for pickings.
                        if (rule.type === 'location_dest' || this.messageType === 'scan_product_or_dest') {
                            result.destLocation = location;
                        } else {
                            result.location = location;
                        }
                        result.match = true;
                    } else if (rule.type === 'lot') {
                        if (this.useExistingLots) {
                            result.lot = await this.cache.getRecordByBarcode(value, 'stock.production.lot');
                        }
                        if (!result.lot) { // No existing lot found, set a lot name.
                            result.lotName = value;
                        }
                        if (result.lot || result.lotName) {
                            result.match = true;
                        }
                    } else if (rule.type === 'package') {
                        const stockPackage = await this.cache.getRecordByBarcode(value, 'stock.quant.package');
                        if (stockPackage) {
                            result.package = stockPackage;
                        } else {
                            // Will be used to force package's name when put in pack.
                            result.packageName = value;
                        }
                        result.match = true;
                    } else if (rule.type === 'package_type') {
                        const packageType = await this.cache.getRecordByBarcode(value, 'stock.package.type');
                        if (packageType) {
                            result.packageType = packageType;
                            result.match = true;
                        } else {
                            const message = _t("An unexisting package type was scanned. This part of the barcode can't be processed.");
                            this.notification.add(message, { type: 'warning' });
                        }
                    } else if (rule.type === 'product') {
                        const product = await this.cache.getRecordByBarcode(value, 'product.product');
                        if (product) {
                            result.product = product;
                            result.match = true;
                        }
                    } else if (rule.type === 'quantity') {
                        result.quantity = value;
                        // The quantity is usually associated to an UoM, but we
                        // ignore this info if the UoM setting is disabled.
                        if (this.groups.group_uom) {
                            result.uom = await this.cache.getRecord('uom.uom', rule.associated_uom_id);
                        }
                        result.match = result.quantity ? true : false;
                    }
                    else{

                    }
                }
                if(result.match) {
                    return result;
                }
            } else if (parsedBarcode.type === 'weight') {
                result.weight = parsedBarcode;
                result.match = true;
                barcode = parsedBarcode.base_code;
            }
        } catch (err) {
            // The barcode can't be parsed but the error is caught to fallback
            // on the classic way to handle barcodes.
            console.log(`%cWarning: error about ${barcode}`, 'text-weight: bold;');
            console.log(err.message);
        }
        const recordByData = await this.cache.getRecordByBarcode(barcode, false, false, filters);
        if (recordByData.size > 1) {
            const message = sprintf(
                _t("Barcode scan is ambiguous with several model: %s. Use the most likely."),
                Array.from(recordByData.keys()));
            this.notification.add(message, { type: 'warning' });
        }

        if (this.groups.group_stock_multi_locations) {
            const location = recordByData.get('stock.location');
            if (location) {
                this._setLocationFromBarcode(result, location);
                result.match = true;
            }
        }

        if (this.groups.group_tracking_lot) {
            const packageType = recordByData.get('stock.package.type');
            const stockPackage = recordByData.get('stock.quant.package');
            if (stockPackage) {
                // TODO: should take packages only in current (sub)location.
                result.package = stockPackage;
                result.match = true;
            }
            if (packageType) {
                result.packageType = packageType;
                result.match = true;
            }
        }

        const product = recordByData.get('product.product');
        if (product) {
            result.product = product;
            result.match = true;
        }
        const product_pkg = recordByData.get('product.packaging');
        console.log('product_pkg',product_pkg);
        if(!product && product_pkg){
            result.product = await this.cache.getRecord('product.product', product_pkg.product_id);
            result.quantity = product_pkg.qty;
            result.match= true;
        }
        if (this.useExistingLots) {
            const lot = recordByData.get('stock.production.lot');
            if (lot) {
                result.lot = lot;
                result.match = true;
            }
        }
        const quantPackage = recordByData.get('stock.quant.package');
        if (this.groups.group_tracking_lot && quantPackage) {
            result.package = quantPackage;
            result.match = true;
        }

        if (!result.match && this.packageTypes.length) {
            // If no match, check if the barcode begins with a package type's barcode.
            for (const [packageTypeBarcode, packageTypeId] of this.packageTypes) {
                if (barcode.indexOf(packageTypeBarcode) === 0) {
                    result.packageType = await this.cache.getRecord('stock.package.type', packageTypeId);
                    result.packageName = barcode;
                    result.match = true;
                    break;
                }
            }
        }
        return result;
    }

});














