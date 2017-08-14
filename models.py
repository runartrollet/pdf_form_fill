"""Database-structure for item-catalog."""

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from sqlalchemy.sql.expression import func
from flask_dance.consumer.backend.sqla import (
    OAuthConsumerMixin,
)
from flask_login import (
    UserMixin,
)
from addresses.address_pymongo import (
    get_location_from_address
)
from my_exceptions import LocationException, NotAuthorized
# import bleach
import enum
from field_dicts.helpers import id_generator
db = SQLAlchemy()

PER_PAGE = 500


class ByID(object):
    """Class which can return it's entity by id."""
    @classmethod
    def by_id(cls, this_id):
        """Return a entity by its id."""
        try:
            this_id = int(this_id)
        except (ValueError, TypeError):
            return None
        entity = cls.query.filter(cls.id == this_id).first()
        if not entity:
            return None
        return entity


class MyBaseModel(ByID):
    """Basic functionality."""

    def owns(self, user):
        """Check if owner."""
        raise NotImplementedError("{} missing owns-method".format(type(self)))

    @classmethod
    def by_id(cls, this_id, user):
        """Return a entity by its id."""
        entity = super(MyBaseModel, cls).by_id(this_id)
        if entity:
            entity.owns(user)
            return entity

    def update_entity(self, dictionary):
        """Update an entity from a dictionary."""
        for key, val, in dictionary.items():
            setattr(self, key, val)
        return self


class ContactType(enum.Enum):
    """Enumeration for types of contactfields."""
    phone = 1,
    email = 2,
    mobile = 3


class InviteType(enum.Enum):
    """Enumeration for types of invites."""
    company = 1,
    create_company = 2,


class UserRole(enum.Enum):
    """Enumeration for types of user-roles."""
    user = 1,
    companyAdmin = 2,
    admin = 3


class ProductCatagory(enum.Enum):
    """Enumeration for catagories of products."""
    cable_inside = 1,
    cable_outside = 2,
    mat_inside = 3
    mat_outside = 4
    single_inside = 5
    single_outside = 6

    @classmethod
    def split(cls, enumObject):
        """Split it."""
        catagory_type = ''
        if enumObject in [cls.cable_inside, cls.cable_outside]:
            catagory_type = 'cable'
        elif enumObject in [cls.mat_inside, cls.mat_outside]:
            catagory_type = 'mat'
        elif enumObject in [cls.single_inside, cls.single_outside]:
            catagory_type = 'single'
        return catagory_type, enumObject in [
            cls.cable_outside, cls.mat_outside, cls.single_outside
        ]


def lookup_vk(manufacturor, mainSpec, watt_total):
    """Return a specific heating_cable from a generic lookup."""
    products = Product.query\
        .filter_by(effect=watt_total)\
        .join(ProductType, aliased=True)\
        .filter_by(mainSpec=mainSpec)\
        .join(ProductType.manufacturor, aliased=True)\
        .filter_by(name=manufacturor)\
        .all()
    return products


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoAccess(Error):
    '''
    Raise when a user doesn't have access to the action or resource

    https://stackoverflow.com/a/26938914/3493586
    '''

    def __init__(self, message, *args):
        self.message = message
        super(NoAccess, self).__init__(message, *args)


class Address(db.Model, MyBaseModel):
    """Address-table for users."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    address1 = db.Column(db.String(200), nullable=False)
    address2 = db.Column(db.String(200))
    post_code = db.Column(db.SmallInteger, nullable=False)
    post_area = db.Column(db.String(200), nullable=False)

    @classmethod
    def update_or_create(
            cls, address_id, address1, address2, post_area, post_code):
        """Update if exists, else create Address."""
        address = Address.query.filter_by(
            id=address_id
        ).first()

        if not address:
            address = Address(
                address1=address1,
                address2=address2,
                post_area=post_area,
                post_code=post_code
            )
        else:
            if (
                    address.address1 != address1 or
                    address.address2 != address2 or
                    address.post_area != post_area or
                    address.post_area != post_area
            ):
                address.address1 = address1
                address.address2 = address2
                address.post_area = post_area
                address.post_area = post_area
                db.session.add(address)

        return address

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        dictionary = {
            'address1': self.address1,
            'address2': self.address2,
            'post_code': self.post_code,
            'post_area': self.post_area
        }
        return dictionary


class Contact(db.Model):
    """Contact-table for users, like phone, email"""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.Enum(ContactType))
    value = db.Column(db.String(200))
    description = db.Column(db.String(200))


class Company(db.Model):
    """Company-table for users."""
    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True)
    name = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    description = db.Column(db.String(500))
    orgnumber = db.Column(db.Integer,
                          unique=True,
                          nullable=False)
    address_id = db.Column(
        db.Integer,
        db.ForeignKey(Address.id),
        nullable=False)
    address = db.relationship(
        Address,
        primaryjoin='Company.address_id==Address.id')
    lat = db.Column(db.Numeric(8, 6))
    lng = db.Column(db.Numeric(9, 6))

    def add_contact(self, c_type, value, description):
        """Add contact to this company."""
        contact = Contact(
            type=c_type,
            value=value,
            description=description
        )
        company_contact = CompanyContact(
            contact=contact,
            company=self
        )
        db.session.add(contact)
        db.session.add(company_contact)
        return contact

    def owns(self, model):
        """Check if company has rights to access this."""
        if model.company == self:
            return True
        else:
            raise NoAccess("Company does not have access to this resource.")

    def get_forms(self, user, per_page=PER_PAGE, page=1):
        """Return all filled forms by company, not by current user."""
        return None, None
    # TODO: Fix this again
        query = Room\
            .query\
            .filter(Room.customer.company == self)\
            .paginate(
                page=page,
                per_page=per_page,
                error_out=True
            )
        filled_forms = []
        for i in query.items:
            if (
                    any(
                        True for mod in
                        i.modifications
                        if not mod.archived
                    ) and
                    any(
                        True for mod in
                        i.modifications
                        if not mod.user == user
                    )
            ):
                filled_forms.append(i)

        return filled_forms, query.pages

    @classmethod
    def update_or_create(
            cls, company_id, name, description, orgnumber, address, lat, lng):
        """Update if exists, else create Company."""
        if not isinstance(address, Address):
            raise ValueError(
                "Did not recieve an Address-type, got '{}'".format(address))
        company = Company.query.filter_by(
            id=company_id
        ).first()

        if not company:
            company = Company()
        company.name = name
        company.description = description
        company.orgnumber = orgnumber
        company.address = address
        company.lat = lat
        company.lng = lng
        db.session.add(company)

        return company

    @classmethod
    def update_or_create_all(cls, form, company=None):
        """up."""
        if company:
            company_id = company.id
        else:
            company_id = None
        if company and company.address:
            address_id = company.address.id
        else:
            address_id = None
        address = Address.update_or_create(
            address_id=address_id,
            address1=form.address.address1.data,
            address2=form.address.address1.data,
            post_area=form.address.post_area.data,
            post_code=form.address.post_code.data,
        )

        location = get_location_from_address(
            form.address.address1.data,
            form.address.post_area.data
        )
        if not location:
            raise LocationException('Fant ikke adressen i databasen')

        company = Company.update_or_create(
            company_id=company_id,
            name=form.name.data,
            description=form.description.data,
            orgnumber=form.org_nr.data,
            address=address,
            lat=location[0],
            lng=location[1]
        )
        if company.contacts:
            company.contacts[0].contact.value = form.email.data
            company.contacts[0].contact.description = form.contact_name.data
            db.session.add(company.contacts[0])
        else:
            company.add_contact(
                c_type=ContactType.email,
                value=form.email.data,
                description=form.contact_name.data
            )
        return company


class CompanyContact(db.Model):
    """Associations-table for company and contacts."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    contact = db.relationship(
        Contact, primaryjoin='CompanyContact.contact_id==Contact.id')
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='CompanyContact.company_id==Company.id',
        backref='contacts')


class User(db.Model, UserMixin):
    """User-table for users."""
    __tablename__ = 'vk_users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    given_name = db.Column(db.String(50))
    family_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    title = db.Column(db.String(50))
    role = db.Column(db.Enum(UserRole), default='user')
    signature = db.Column(db.Binary())
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship(
        Company, primaryjoin='User.company_id==Company.id')

    def get_forms(self, per_page=PER_PAGE, page=1):
        """Return all filled forms created by user."""
        return [], 0
        subq = db.session\
            .query(
                func.max(RoomItem.id)
            )\
            .filter(
                (RoomItem.user == self) &
                (RoomItem.archived != True)
            )\
            .group_by(RoomItem.room_id)\
            .subquery()
        query = RoomItem\
            .query\
            .filter(RoomItem.id.in_(subq))\
            .paginate(
                page=page,
                per_page=per_page,
                error_out=True
            )

        filled_forms = []
        for mod in query.items:
            if mod.room and not mod.room.archived:
                filled_forms.append(mod.room)

        return filled_forms, query.pages

    def owns(self, model):
        """Check if user has rights to access this."""
        if model.user == self:
            return True
        else:
            raise NoAccess("You don't have access to this resource.")

    def add_contact(self, c_type, value, description):
        """Add contact to this user."""
        contact = Contact(
            type=c_type,
            value=value,
            description=description
        )
        company_contact = UserContact(
            contact=contact,
            user=self
        )
        db.session.add(contact)
        db.session.add(company_contact)
        return contact


class Invite(db.Model):
    """Invite-table for users."""

    id = db.Column(db.String, unique=True, primary_key=True)
    type = db.Column(db.Enum(InviteType), default='company')
    company_id = db.Column(
        db.Integer,
        db.ForeignKey(Company.id)
    )
    company = db.relationship(
        Company, primaryjoin='Invite.company_id==Company.id')
    inviter_user_id = db.Column(
        db.Integer, db.ForeignKey(User.id), nullable=False)
    inviter = db.relationship(
        User,
        primaryjoin='Invite.inviter_user_id==User.id')
    invitee_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    invitee = db.relationship(
        User, primaryjoin='Invite.invitee_user_id==User.id')

    @classmethod
    def get_random_unique_invite_id(cls):
        """Return a random unique id for the invite-table."""
        rand = id_generator()
        while db.session.query(Invite).filter(
                Invite.id == rand).limit(1).first() is not None:
            rand = id_generator()

        return rand

    @classmethod
    def get_invites_from_user(cls, inviter):
        """Return all invites from user which are still valid for signup."""
        return Invite.query.filter(
            Invite.inviter_user_id == inviter.id,
            Invite.invitee_user_id == None)  # noqa

    @classmethod
    def get_invite_from_id(cls, invite_id):
        """Return a valid invite from an id."""
        return Invite.query.filter(
            Invite.id == invite_id,
            Invite.invitee_user_id == None).first()  # noqa

    @classmethod
    def create(cls, inviter):
        """Create a new invite."""
        invites = cls.get_invites_from_user(inviter).count()
        if invites < 10:
            invite = Invite(
                id=cls.get_random_unique_invite_id(),
                company=inviter.company,
                inviter=inviter,
            )
            return invite

        else:
            raise ValueError("Du har nådd din maksgrense for invitasjoner. Når noen har aktivert en av dine invitasjons-lenker og registrert seg, kan du lage nye invitasjons-lenker.")  # noqa

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        dictionary = {
            'url': self.id,
            'company_name': self.company.name,
        }
        return dictionary


class OAuth(db.Model, OAuthConsumerMixin):
    """Oath-table."""
    __tablename__ = 'oauth'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class UserContact(db.Model):
    """Associations-table for user and contacts."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    contact = db.relationship(
        Contact, primaryjoin='UserContact.contact_id==Contact.id')
    user = db.relationship(
        User, primaryjoin='UserContact.user_id==User.id')


class Manufacturor(db.Model):
    """Manufacturor-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        product_types = ProductType.query.filter_by(manufacturor=self).all()
        product_type_dict = [i.serialize for i in product_types]

        dictionary = {
            'id': self.id,
            'name': self.name,
            'product_types': product_type_dict
        }
        return dictionary


class ProductType(db.Model):
    """ProcuctTypes-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    manufacturor_id = db.Column(db.Integer, db.ForeignKey(Manufacturor.id))
    manufacturor = db.relationship(
        Manufacturor, primaryjoin='ProductType.manufacturor_id==Manufacturor.id')  # noqa
    mainSpec = db.Column(db.SmallInteger)  # meterEffekt/kvadratMeterEffekt
    # meterEffekt/kvadratMeterEffekt
    secondarySpec = db.Column(db.SmallInteger)
    catagory = db.Column(db.Enum(ProductCatagory))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        products = Product.query.filter_by(product_type=self).all()
        products_dict = [i.serialize for i in products]

        dictionary = {
            'id': self.id,
            'name': self.name,
            'mainSpec': self.mainSpec,
            'secondarySpec': self.secondarySpec,
            'products': products_dict
        }
        dictionary['type'], dictionary[
            'inside'] = ProductCatagory.split(self.catagory)
        return dictionary


class Product(db.Model, ByID):
    """Product-table."""
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    effect = db.Column(db.Numeric(8))
    product_type_id = db.Column(db.Integer, db.ForeignKey(ProductType.id))
    product_type = db.relationship(
        ProductType, primaryjoin='Product.product_type_id==ProductType.id')
    specs = db.Column(db.JSON)
    restrictions = db.Column(db.JSON)

    @classmethod
    def get_by_id(cls, p_id):
        """Return object by id."""
        return Product.query.filter_by(id=p_id).first()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        dictionary = {
            'id': self.id,
            'effect': self.effect,
            'restrictions': self.restrictions
        }
        return dictionary


class Customer(db.Model, MyBaseModel):
    """Customer-table."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    address_id = db.Column(db.Integer,
                           db.ForeignKey(Address.id),
                           nullable=False)
    address = db.relationship(
        Address, primaryjoin='Customer.address_id==Address.id')
    company_id = db.Column(
        db.Integer, db.ForeignKey(Company.id), nullable=False)
    company = db.relationship(
        Company, primaryjoin='Customer.company_id==Company.id')

    def owns(self, user):
        """Check that user has rights to this customer."""
        user.company.owns(self)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'address': self.address.serialize,
            'rooms': [i.serialize for i in self.rooms],
            'id': self.id
        }


class Room(db.Model, MyBaseModel):
    """Table of forms filled by users."""
    # __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))  # e.g. room name
    archived = db.Column(db.Boolean)
    specs = db.Column(db.JSON, nullable=False)
    customer_id = db.Column(
        db.Integer, db.ForeignKey(Customer.id), nullable=False)
    customer = db.relationship(
        Customer,
        primaryjoin='Room.customer_id==Customer.id',
        backref='rooms')

    def owns(self, user):
        """Check that user has rights to this room."""
        self.customer.owns(user)

    def archive_this(self, user):
        """Mark this as archived."""
        if user.owns(self):
            self.archived = True

    @property
    def serialize(self, user=None):
        """Return object data in easily serializeable format"""

        dictionary = {
            'id': self.id,
            'room_name': self.name,
            'heating_cables': [i.serialize for i in self.items],
        }
        dictionary.update(self.specs)
        return dictionary


class RoomItem(db.Model, MyBaseModel):
    """Holder for modifications to items."""
    id = db.Column(db.Integer, primary_key=True, unique=True)
    room_id = db.Column(
        db.Integer, db.ForeignKey(Room.id), nullable=False)
    room = db.relationship(
        Room,
        primaryjoin='RoomItem.room_id==Room.id',
        backref='items')  # noqa

    def owns(self, user):
        """Check that user has rights to this room-item."""
        self.room.owns(user)

    @property
    def serialize(self, user=None):
        """Return object data in easily serializeable format"""
        if self.modifications:
            dictionary = self.modifications[0].serialize
            # json = dictionary.pop('json')
            # measurements = {}
            dictionary['id'] = self.id
            # dictionary['product_id'] = json.pop('product_id', None)
            # dictionary['specs'] = json
            return dictionary

    @classmethod
    def update_or_create(
            cls, user, room, id=None,
            room_item=None, json={}, pdf_json={}):
        """Update or create a RoomItemModifications.."""
        if not room_item:
            room_item = RoomItem.by_id(id, user)
        if not room_item:
            room_item = RoomItem(
                room=room
            )
        if not json.get('product_id'):
            raise ValueError('Missing product_id in json: {}'.format(json))
        db.session.add(room_item)
        RoomItemModifications.update_or_create(
            user=user,
            room_item=room_item,
            json=json,
            pdf_json=pdf_json
        )
        return room_item


class RoomItemModifications(db.Model, MyBaseModel):
    """Table of modification-dated for Room-model."""
    __tablename__ = 'room_item_modifications'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(
        User, primaryjoin='RoomItemModifications.user_id==User.id')
    archived = db.Column(db.Boolean, default=False)
    room_item_id = db.Column(
        db.Integer, db.ForeignKey(RoomItem.id), nullable=False)
    room_item = db.relationship(
        RoomItem,
        primaryjoin='RoomItemModifications.room_item_id==RoomItem.id',
        backref='modifications')  # noqa
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # All data from the users-form
    json = db.Column(db.JSON, nullable=True)
    # All data actually used to fill the pdf.
    pdf_json = db.Column(db.JSON, nullable=True)

    __mapper_args__ = {
        "order_by": date.desc()
    }

    @classmethod
    def update_or_create(cls, user, room_item, json, pdf_json):
        """
        Create modification-date if last update was either not made by
        current user, or within the last 5 minutes."""
        if not user:
            ValueError('Expected a user, got {}'.format(user))
        if not room_item:
            ValueError('Expected a room_item, got {}'.format(room_item))
        last_modified = None
        if user.id:
            last_modified = RoomItemModifications.query.filter(
                RoomItemModifications.room_item == room_item).order_by(
                    desc(RoomItemModifications.date)).filter(
                        or_(
                            RoomItemModifications.user != user,
                            RoomItemModifications.date >= (
                                datetime.utcnow() - timedelta(seconds=1))
                        )).first()
        if not last_modified:
            last_modified = RoomItemModifications(
                user=user,
                room_item=room_item
            )
        last_modified.json = json
        db.session.add(last_modified)
        return last_modified

    def archive_this(self, user):
        """Mark this object as archived."""
        if user.owns(self):
            self.archived = True
            db.session.add(self)
            db.session.commit()
            return True

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        creation_time = db.session\
            .query(
                RoomItemModifications.date
            )\
            .filter(
                RoomItemModifications.room_item_id == self.room_item_id)\
            .order_by(RoomItemModifications.date)\
            .first()

        dictionary = {
            'id': self.id,
            'm_date': self.date
        }
        specs = self.json.copy()
        dictionary['product_id'] = specs.get('product_id')
        if creation_time:
            dictionary['c_date'] = creation_time
        if self.room_item:
            dictionary['specs'] = specs
        return dictionary
