from flask import Flask, render_template, request, redirect, url_for
#from flask_wtf.csrf import CSRFProtect
#from werkzeug.utils import secure_filename
from Forms_Product import CreateProductForm
import shelve, Product, os

#csrf = CSRFProtect()
#UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
app = Flask(__name__, template_folder='khansa_templates')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form, request.files)
    if request.method == 'POST' and create_product_form.validate():
        product_dict = {}
        db = shelve.open('product.db', 'c')

        try:
            product_dict = db['Product']
        except:
            print('Error in retrieving Product from product.db')

        product = Product.Product(create_product_form.name.data, create_product_form.category.data, create_product_form.price.data, create_product_form.rating.data, create_product_form.picture.data)
        product_dict[product.get_product_id()] = product
        db['Product'] = product_dict

        db.close()

        return redirect(url_for('retrieve_product'))
    return render_template('createProduct.html', form=create_product_form)


@app.route('/retrieveProduct')
def retrieve_product():
    product_dict = {}
    db = shelve.open('product.db', 'r')
    product_dict = db['Product']
    db.close()

    product_list = []
    for key in product_dict:
        product = product_dict.get(key)
        product_list.append(product)

    return render_template('retrieveProduct.html', count=len(product_list), product_list=product_list)


@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form, request.files)
    if request.method == 'POST' and update_product_form.validate():
        product_dict = {}
        db = shelve.open('product.db', 'w')
        product_dict = db['Product']

        product = product_dict.get(id)
        product.set_name(update_product_form.name.data)
        product.set_category(update_product_form.category.data)
        product.set_price(update_product_form.price.data)
        product.set_rating(update_product_form.rating.data)
        product.set_picture(update_product_form.picture.data)

        db['Product'] = product_dict
        db.close()
        return redirect(url_for('retrieveUsers'))
    else:
        product_dict = {}
        db = shelve.open('product.db', 'r')
        product_dict = db['Product']
        db.close()

        product = product_dict.get(id)
        update_product_form.name.data = product.get_name()
        update_product_form.category.data = product.get_category()
        update_product_form.price.data = product.get_price()
        update_product_form.rating.data = product.get_rating()
        update_product_form.picture.data = product.get_picture()

        return render_template('updateProduct.html', form=update_product_form)


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    product_dict = {}
    db = shelve.open('product.db', 'w')
    product_dict = db['Product']

    product_dict.pop(id)

    db['Product'] = product_dict
    db.close()

    return redirect(url_for('retrieve_product'))

if __name__ == '__main__':
    app.run()
