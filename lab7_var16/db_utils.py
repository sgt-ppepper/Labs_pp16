from lab6_var16.models import SessionFactory

#session = Session()#
#engine = create_engine(
 #     "mysql://root:Atas123456-@localhost/mydb")
#SessionFactory = sessionmaker(bind=engine)
#session = Session(engine)

def create(model_class,**kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    session.commit()
    return session.query(model_class).filter_by(**kwargs).one()

def create_return(model_class,**kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    session.commit()
    return []

def get_entry_by_id(model_class, id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(id=id,**kwargs).one()

def get_entry_by_two_id(model_class, sch_id, film_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(schelude_id=sch_id, films_id=film_id).one()

def get_entries(model_class,**kwargs):
    session = SessionFactory()
    return session.query(model_class).all()

def update_entry(entry,**kwargs):
    session = SessionFactory()
    for key, value in kwargs.items():
        setattr(entry,key,value)
    session.commit()
    return entry

def delete_entry(model_class, id, **kwargs):
    session = SessionFactory()
    a = False
    if session.query(model_class).filter_by(id=id, **kwargs).first() is not None:
        session.query(model_class).filter_by(id=id, **kwargs).delete()
        session.commit()
        a=True
    return a

def get_entry(model_class,**kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(**kwargs).order_by(model_class.id.desc()).first()

def get_entry_scalar(model_class,**kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(**kwargs).scalar()

def create_entry(model_class, user_id, sch_id):
    session = SessionFactory()
    entry = model_class(user_id=user_id, schelude_id=sch_id)
    session.add(entry)
    session.commit()
    return []