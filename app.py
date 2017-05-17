"""Udacity assignment for creating a Neighborhood-map."""

import sys
from config import configure_app
from models import (db, Manufacturor, Product,
                   ProductSpec, ProductType, lookup_vk)
from vk_objects import nexans
from flask import (
    Flask,
    request,
    redirect,
    render_template,
)


app = Flask(__name__, instance_relative_config=True)
configure_app(app)

db.init_app(app)


@app.route('/')
def view_form():
    """View for home."""
    lookup_vk('Nexans', 17, 500)
    return render_template(
        'form.html',
    )


@app.route('/nexans.html', methods=['POST'])
def fill_document():
    """Fill a document with data from form, and smart usage."""
    nexans.set_fields_from_dict(request.form)  # TODO: is this safe?
    nexans.create_filled_pdf('output.pdf')
    return redirect('/')


# hook up extensions to app
if __name__ == "__main__":
    if '--setup' in sys.argv:
        print('Setup')
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.drop_all()
            db.create_all()
            Nexans = Manufacturor(name='Nexans', description="It's nexans")
            db.session.add(Nexans)
            txlp = ProductType(name='TXLP/2R/17',
                               mainSpec='TXLP',
                               watt_per_meter=17,
                               ledere=2,
                               manufacturor=Nexans)
            txlp_tull = ProductType(name='TXLP/TULL/17',
                               mainSpec='TXLPTULL',
                               watt_per_meter=16,
                               ledere=2,
                               manufacturor=Nexans)
            db.session.add(txlp)
            db.session.add(txlp_tull)
            import Nexans_TXLP
            for vk in Nexans_TXLP.vks:
                name = vk.pop('Betegnelse')
                effekt = vk.pop('Effekt ved 230V')
                if name:
                    new_vk = Product(
                        name=name, product_type=txlp, effekt=effekt)
                    new_vk.add_keys_from_dict(vk)
                    db.session.add(new_vk)
            tulle_vk = Product(
                name='TULL', product_type=txlp_tull, effekt=500)
            db.session.add(tulle_vk)
            db.session.commit()
            print("Database tables created")

    else:
        app.run(host='0.0.0.0', port=app.config['PORT'])
