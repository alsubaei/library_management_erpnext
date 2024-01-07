// Copyright (c) 2024, Faris Ansari and contributors
// For license information, please see license.txt
frappe.ui.form.on("Bank Loan", {
    // 	refresh(frm) {

    // 	},
    repayment_months: function (frm) {
        calculate_monthly_repayment(frm);
    },
    loan_amount: function (frm) {
        calculate_monthly_repayment(frm);
    },
    interest: function (frm) {
        calculate_monthly_repayment(frm);
    }
});
function calculate_monthly_repayment(frm) {
    if (frm.doc.loan_amount && frm.doc.repayment_months) {
        var monthly = frm.doc.loan_amount / frm.doc.repayment_months;
        var monthly = monthly + monthly * frm.doc.interest / 100;
        frm.doc.monthly_repayment = monthly;
        refresh_field('monthly_repayment')
    }
    else {
        frm.doc.monthly_repayment = 0;
        refresh_field('monthly_repayment')
    }
}

