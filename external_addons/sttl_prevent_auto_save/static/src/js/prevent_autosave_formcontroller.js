/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { useSetupView } from "@web/views/view_hook";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";

const webSetup = FormController.prototype.setup;
const webonPagerUpdate = FormController.prototype.onPagerUpdate;

let models;
let auto_save_boolean_all;
let auto_save_boolean;

const Formsetup = function () {

    this.orm = useService("orm");

    const getFormData =  async () => {
        models = await this.orm.searchRead('prevent.model.line', [], ['model']);
        auto_save_boolean_all = await this.orm.searchRead('prevent.model', [], ['auto_save_prevent_all']);
        auto_save_boolean = await this.orm.searchRead('prevent.model', [], ['auto_save_prevent']);
    }
    getFormData();

    useSetupView({
        beforeLeave: () => {
            var root = this.model.root
            if (root.isDirty) {
                var model_lst = models.map(dict => dict.model)
                var boolean_all_lst = auto_save_boolean_all.map(dict => dict.auto_save_prevent_all)
                var boolean_lst = auto_save_boolean.map(dict => dict.auto_save_prevent)
                if (boolean_all_lst.includes(true)) {
                    root.discard();
                    return true;
                }
                else {
                    if (model_lst.includes(root.resModel) && boolean_lst.includes(true)) {
                        root.discard();
                        return true;
                    }
                }
            }
        },
        beforeUnload: () => {
            var root = this.model.root
            var model_lst = models.map(dict => dict.model)
            var boolean_all_lst = auto_save_boolean_all.map(dict => dict.auto_save_prevent_all)
            var boolean_lst = auto_save_boolean.map(dict => dict.auto_save_prevent)
            if (boolean_all_lst.includes(true)) {
                root.discard();
                return true;
            } else {
                if (model_lst.includes(root.resModel) && boolean_lst.includes(true)) {
                    root.discard();
                    return true;
                } else {
                    root.urgentSave();
                    return true;
                }
            }
            return true
        },
    });
    const res = webSetup.apply(this, arguments);
    return res;
};
FormController.prototype.setup = Formsetup;

const beforeUnload = async function (ev) {};

const onPagerUpdate = async function () {
    var root = this.model.root
    // root.askChanges();
    if (root.isDirty) {
        root.discard();
    }
    return webonPagerUpdate.apply(this, arguments);
};

FormController.prototype.beforeUnload = beforeUnload;
FormController.prototype.onPagerUpdate = onPagerUpdate;