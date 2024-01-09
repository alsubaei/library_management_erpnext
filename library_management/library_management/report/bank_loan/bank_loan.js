// Copyright (c) 2024, Faris Ansari and contributors
// For license information, please see license.txt
frappe.query_reports["Bank Loan"] = {
	"filters": [
		{
            fieldname: 'company',
            label: __('Company'),
            fieldtype: 'Link',
            options: 'Company',
            default: frappe.defaults.get_user_default('company')
			,reqd:1
        },{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[1],
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[2],
		},
	]
};
