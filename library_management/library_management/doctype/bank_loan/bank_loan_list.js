frappe.listview_settings['Bank Loan'] = {
    get_indicator(doc) {
        // customize indicator color
        if (doc.status=='Paid') {
            return [__("Paid"), "green", "status,=,Paid"];
        } else if (doc.status=='Partially paid') {
            return [__("Partially paid"), "orange", "status,=,Partially paid"];
        } else if (doc.status=='Unpaid') {
            return [__("Unpaid"), "yellow", "status,=,Unpaid"];
        } else if (doc.status=='Accrued') {
            return [__("Accrued"), "blue", "status,=,Unpaid"];
        }
    }
}