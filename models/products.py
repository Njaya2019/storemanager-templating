from models.data_base import DataBase
import psycopg2

d_b=DataBase()
class products():
    
    def __init__(self, p_name, price, quantity):
        self.p_name= p_name
        self.price= price
        self.quantity= quantity
        self.cur_con=d_b.connect_to_store_db()
        self.cur=self.cur_con[0]
        self.con=self.cur_con[1]

    def add_product(self):
        insert_sql="INSERT INTO products(product_name,product_price,product_qty) VALUES(%s,%s,%s)"
        product_data=(self.p_name,self.price,self.quantity)
        self.cur.execute(insert_sql,product_data)
        self.con.commit()
        return 'The product has been added'

    def get_a_product(self, product_id):
        product_query="SELECT * FROM products WHERE product_id=%s"
        self.cur.execute(product_query,[product_id])
        prodct=self.cur.fetchone()
        if prodct:
            return prodct
        else:
            return "The product wasn\'t found."
           
    def get_products(self):
        products_query="SELECT * FROM products"
        self.cur.execute(products_query)
        products_table_rows=self.cur.fetchall()
        if products_table_rows:
            #for product_row in products_table_row:
                #products_dict.update({'product_id':product_row['product_id'], 'Product_name':product_row['product_name'], 'Product_price':product_row['product_price'],'Quantity_available':product_row['pro']})
                #another_product_list.append(products_dict.copy())
            return products_table_rows
        else:
            return 'There are no products yet'
    def update_product(self,product_id,product_name,price,qty):
        try:
            update_psql="UPDATE products SET product_name=%s, product_price=%s, product_qty=%s WHERE product_id=%s RETURNING product_id,product_name,product_price"
            self.cur.execute(update_psql,(product_name,price,qty,product_id))
            updated_product=self.cur.fetchone()
            if updated_product==None:
                return 'The product dosen\'t exists'
            self.con.commit()
            return updated_product
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def delete_product(self,product_id):
        delete_product_psql="DELETE FROM products WHERE product_id=%s RETURNING product_id"
        self.cur.execute(delete_product_psql, [product_id])
        returned_id=self.cur.fetchone()
        self.con.commit()
        if returned_id==None:
            return 'The product id doesn\'t exist'
        return 'The product was deleted'





