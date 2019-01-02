from flask.views import MethodView
from flask import request, jsonify, abort, render_template
from models.products import products
from models.users import users
from Validators.validate_json import validate_json_numeric_value,validate_json_string_value
from decorators import token_required


class admin(MethodView):
    decorators=[token_required]
    p=products(p_name=None, price=None,quantity=None)
    
    def get(self,current_user_id,product_id):
        if not product_id:
            available_products=self.p.get_products()
            return jsonify({'Products':available_products}), 200
        if product_id:
            requested_product=self.p.get_a_product(product_id)
            return jsonify({'Product':requested_product}), 200
    
    def post(self,current_user_id):
        #u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
        #u=users(full_name=None,email=None,role=None,password=None,confirm_pwd=None)
        pro_name=request.json['product_name']
        pro_price=request.json['price']
        pro_qty=request.json['quantity']
        if not validate_json_numeric_value(pro_price) or not validate_json_string_value(pro_name) or not validate_json_numeric_value(pro_qty):
            return jsonify({'message':'Please provide valid strings or integers'})
        if not pro_name or not pro_price or not pro_qty:
            return jsonify({'message':'Please provide all values'})
        pr=products(pro_name,pro_price, pro_qty)
        msg=pr.add_product()
        return #jsonify({'message':msg}), 200
    def put(self,current_user_id,product_id):
        
        p_name=request.json['product_name']
        p_price=request.json['price']
        p_qty=request.json['quantity']
        pro_duct=self.p.update_product(product_id,p_name,p_price,p_qty)
        return jsonify({'product_updated':pro_duct}),200
    
    def delete(self,current_user_id,product_id):
        delete_message=self.p.delete_product(product_id)
        return jsonify({'message':delete_message}) 




