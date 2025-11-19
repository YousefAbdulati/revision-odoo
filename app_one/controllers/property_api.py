import math
from odoo import http
from odoo.http import request
import json
from urllib.parse import parse_qs


def valid_response(data, meta_data=None ,status = 200 ):
    respons={
        "message":"Successfully!",
        "data":data,
    }
    if meta_data :
            respons["meta_data"] = meta_data

    return request.make_json_response(respons ,status=status)

def invalid_response(error,status):
    return request.make_json_response({
        "error":error,
    },status=status)


class PropertyApi(http.Controller):

    @http.route("/v1/property" , methods=["POST"] ,type="http" ,auth="none" ,csrf=False)
    def create_property(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        if not vals.get("name"):
            return invalid_response({
                    "message":"'name' Is Required!"
                },status=400)

        try:
            res=request.env["property"].sudo().create(vals)

            if res:
                return valid_response({
                    "message":"Property Created Successfully",
                    "id":res.id,
                    "name":res.name
                },status=201)
        except Exception as e:

            return invalid_response({
                    "message": e
                },status=400)



    @http.route("/v1/property/json" , methods=["POST"], type="json" , auth="none" ,csrf=False)
    def create_property2(self):
        args= request.httprequest.data.decode()
        vals=json.loads(args)
        res=request.env["property"].sudo().create(vals)
        if res:
            return {
                "message":"Json Property Created"
            }
        


    @http.route("/v1/property/<int:property_id>" , methods=["PUT"] , type="http" , auth="none" ,csrf=False)
    def update_property(self, property_id):
        property_id = request.env["property"].sudo().search([("id", "=" , property_id)])
        if not property_id :
            return invalid_response({
            "message":"Id Doesn't Exist !"
        },status=404)

        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            res=property_id.write(vals)
            return valid_response({
                "message":"Property has been Updated",
                "id":property_id.id,
                "name":property_id.name,
            },status=200)
        except Exception as e :
            return invalid_response({
                "message":e
            },status=400)


    @http.route("/v1/property/<int:property_id>" ,methods=["GET"] ,type="http" ,auth="none" ,csrf=False)
    def get_property(self,property_id):
        try:
            property_id=request.env["property"].sudo().search([("id", "=" , property_id)])
            if not property_id:
                return invalid_response({
                    "message":"Id Doesn't Exist !"
                },status=404)
            
            return valid_response({
                "id":property_id.id,
                "name":property_id.name,
                "seq":property_id.seq,
                "description":property_id.description,
                "beadrooms":property_id.bedrooms,
                },status=200)
        
        except Exception as error:
            return invalid_response({
                "message": error
            },status=404)
        

    @http.route("/v1/property/<int:property_id>" ,methods=["DELETE"] ,type="http" ,auth="none" ,csrf=False)
    def delete_property(self,property_id):
        try:
            property_id=request.env["property"].sudo().search([("id", "=" , property_id)])
            if not property_id:
                return invalid_response({
                    "message":"Id Doesn't Exist !"
                },status=404)
            
            property_id.unlink()
            
            return valid_response({
                "message":"Property has been deleted Successfully"
                },status=200)
        
        except Exception as error:
            return invalid_response({
                "message": error
            },status=404)
        


    @http.route("/v1/properties" ,methods=["GET"] ,type="http" ,auth="none" ,csrf=False)
    def get_property_list(self,):
        try:

            prams=parse_qs(request.httprequest.query_string.decode("utf-8"))
            
            property_domain=[]
            page = offset = None
            limit = 10
            if prams.get("state"):
                property_domain += [("state" , "=" , prams.get("state")[0])]


            if prams.get("limit"):
                limit=  int(prams.get("limit")[0])
            if prams.get("page"):
                page=  int(prams.get("page")[0])
                offset = limit * (page - 1)

            

            property_ids=request.env["property"].sudo().search(property_domain , limit=limit , offset = offset)
            property_ids_count=request.env["property"].sudo().search_count(property_domain)
            pages_count = math.ceil(property_ids_count/limit) if limit else 1

            if not property_ids:
                return invalid_response({
                    "message":"Id Doesn't Exist !"
                },status=404)
            
            
            return valid_response(
                data=[{
                "id":property_id.id,
                "name":property_id.name,
                "seq":property_id.seq,
                "description":property_id.description,
                "beadrooms":property_id.bedrooms,
                } for property_id in property_ids] ,
                meta_data=[{
                    "pages" : pages_count,
                    "page_number" : page if page else 1,
                    "limit":limit,
                    "count":property_ids_count
                }]

                ,status=200
                ) 
        
        except Exception as error:
            return invalid_response({
                "message": error
            },status=404)
        



    #with sql

    @http.route("/v1/property-sql" , methods=["POST"] ,type="http" ,auth="none" ,csrf=False)
    def create_property_sql(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        if not vals.get("name"):
            return invalid_response({
                    "message":"'name' Is Required!"
                },status=400)

        try:
            cr = request.env.cr
            columns = ",".join(vals.keys())
            values = ",".join(["%s"] * len(vals))
            query=f""" insert into property ({columns}) values ({values}) returning id, name """
            cr.execute(query , tuple(vals.values()))
            request.env.cr.commit()
            res = cr.fetchone()

            if res:
                return valid_response({
                    "message":"Property Created Successfully",
                    "id":res[0],
                    "name":res[1]
                },status=201)
            
        except Exception as e:

            return invalid_response({
                    "message": e
                },status=400)
