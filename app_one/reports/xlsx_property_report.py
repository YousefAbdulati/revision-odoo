from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter





class XlsxPropertyReport(http.Controller):


    @http.route("/property/excel/report/<string:property_ids>", auth="user" , type="http")
    def download_property_excel_report(self,property_ids):

        property_ids = request.env["property"].browse(literal_eval(property_ids))
        print(property_ids)

        output=io.BytesIO()
        workbook= xlsxwriter.Workbook(output ,{"in_memory":True})
        worksheet= workbook.add_worksheet("Properties")

        header_format=workbook.add_format({"bold":True , "bg_color": "#3C90A5" ,"align":"center"})
        property_format=workbook.add_format({"bg_color": "#A7EDFF" ,"align":"center"})
        price_format=workbook.add_format({"num_format":"$ ##,## 00.00", "bg_color": "#A7EDFF" ,"align":"center"})

        headers=["Name" ,"Postcode", "Beadrooms" ,"Selling Price" ,"Garden"]

        for index, header in enumerate(headers) :
            worksheet.write(0, index, header, header_format)

        for index, property in enumerate(property_ids,1) :
            worksheet.write(index, 0, property.name, property_format)
            worksheet.write(index, 1, property.postcode, property_format)
            worksheet.write(index, 2, property.bedrooms, property_format)
            worksheet.write(index, 3, property.selling_price, price_format)
            worksheet.write(index, 4, "Yes" if property.garden else "No", property_format)

        workbook.close()
        output.seek(0)

        file_name='Property-Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers =[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment;filename={file_name}')
            ]
        )



