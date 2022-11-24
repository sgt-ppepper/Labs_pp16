from models import *


def create_entry(model_class, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return session.query(model_class).filter_by(**kwargs).one()


def create_entry_by_uid(model_class, user_id, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(user_iduser=user_id, **kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return []


def create_access_entry(model_class, note_id, time, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(note_id=note_id, time=time, **kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return []


def create_change_entry(model_class, user_id, note_id, time, commit=True):
    session = SessionFactory()
    entry = model_class(user_id=user_id, note_id=note_id, time=time)
    session.add(entry)
    if commit:
        session.commit()
    return []


def get_all_entry(model_class):
    session = SessionFactory()
    return session.query(model_class).all()


def get_entry_by_id(model_class, id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(id=id, **kwargs).one()


def get_entry_by_username(model_class, username):
    session = SessionFactory()
    return session.query(model_class).filter_by(username=username).one()


def get_entry_by_username_scalar(model_class, username):
    session = SessionFactory()
    return session.query(model_class).filter_by(username=username).scalar()


def get_entry_by_email_scalar(model_class, email):
    session = SessionFactory()
    return session.query(model_class).filter_by(email=email).scalar()


def get_all_entry_by_kwargs(model_class, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(**kwargs).all()


def get_all_entry_by_uid(model_class, user_id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_id=user_id, **kwargs).all()


def get_entry_by_two_id(model_class, user_id, note_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_iduser=user_id, id=note_id).one()


def get_entry_by_id_count(model_class, note_id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(note_id=note_id, **kwargs).count()


def get_entry_by_uid_count(model_class, user_id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_id=user_id, **kwargs).count()


def get_entry_by_two_id_access(model_class, user_id, note_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_id=user_id, note_id=note_id).scalar()


def get_entry_by_user_id(model_class, user_iduser, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_iduser=user_iduser, **kwargs).all()


def get_entry_by_title(model_class, user_id, **kwargs):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_iduser=user_id, **kwargs).all()


def get_all_entry_by_tag(model_class, user_id, tag):
    session = SessionFactory()
    return session.query(model_class).filter_by(user_iduser=user_id).filter(model_class.tags.contains(tag)).all()


def get_all_entry_by_id_tag(model_class, id, tag):
    session = SessionFactory()
    return session.query(model_class).filter_by(id=id).filter(model_class.tags.contains(tag)).all()

def update_entry(model_class, id, commit=True, **kwargs):
    session = SessionFactory()
    entry = session.query(model_class).filter_by(id=id).one()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def delete_entry(model_class, id, *, commit=True, **kwargs):
    session = SessionFactory()
    session.query(model_class).filter_by(id=id, **kwargs).one()
    session.query(model_class).filter_by(id=id, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry_by_two_id(model_class, user_id, note_id, *, commit=True, **kwargs):
    session = SessionFactory()
    session.query(model_class).filter_by(user_iduser=user_id, id=note_id, **kwargs).one()
    session.query(model_class).filter_by(user_iduser=user_id, id=note_id, **kwargs).delete()
    if commit:
        session.commit()


def delete_entry_access_by_two_id(model_class, user_id, note_id, *, commit=True):
    session = SessionFactory()
    session.query(model_class).filter_by(user_id=user_id, note_id=note_id).one()
    session.query(model_class).filter_by(user_id=user_id, note_id=note_id).delete()
    if commit:
        session.commit()


def delete_entry_access(model_class, note_id, *, commit=True, **kwargs):
    session = SessionFactory()
    session.query(model_class).filter_by(note_id=note_id, **kwargs).delete()
    if commit:
        session.commit()


def is_owner(model_class, user_id, note_id):
    if get_entry_by_two_id_access(model_class, user_id, note_id):
        return False
    return True
