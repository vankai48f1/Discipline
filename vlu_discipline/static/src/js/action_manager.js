import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import framework from "web.framework";
import session from "web.session";

registry. ("ir.actions.report handlers").add("xlsx", async (action) => {
    if (action.report_type === "xlsx"){
        framework.blockUI();
        var def = $.Deferred();
        session.get_xlsx({
            url: '/xlsx_reports',
            data: action.data,
            success: def.resolve.bind(def),
            complete: framework.unblockUI,
        });
        return def
    }
});