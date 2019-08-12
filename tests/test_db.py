import pytest
from spending_tracker import create_app, db
import tempfile
import os
from spending_tracker.db_models.db_models import UserModel, WalletModel, CategoryModel
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_db():
    app = create_app()
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
    app.app_context().push()
    yield db

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def _get_user():
    user = UserModel(
        user='tester',
        balance=12
    )
    return user


def _get_wallet(user_id):
    wallet = WalletModel(
        user_id=user_id,
        money=12
    )
    return wallet


def _get_categories(wallet_id):
    categories = CategoryModel(
        wallet_id=wallet_id,
        travel=1,
        entertainment=2,
        eating_out=3,
        house=4,
        bills=5,
        food=6
    )
    return categories


def test_create_user(mock_db):
    user = UserModel(
        user='tester',
        balance=123
    )
    mock_db.session.add(user)
    mock_db.session.commit()
    assert UserModel.query.count() == 1


def test_create_wallet_categories(mock_db):
    user = _get_user()
    mock_db.session.add(user)
    mock_db.session.commit()

    db_user = UserModel.query.first()
    wallet = _get_wallet(db_user.id)
    mock_db.session.add(wallet)
    mock_db.session.commit()
    assert WalletModel.query.count() == 1
    assert wallet.user_id == db_user.id

    db_wallet = WalletModel.query.first()
    categories = _get_categories(db_wallet.id)
    mock_db.session.add(categories)
    mock_db.session.commit()
    assert CategoryModel.query.count() == 1
    assert categories.wallet_id == db_wallet.id


def test_user_exists(mock_db):
    user_1 = _get_user()
    user_2 = _get_user()
    mock_db.session.add(user_1)
    mock_db.session.add(user_2)
    with pytest.raises(IntegrityError):
        mock_db.session.commit()


def test_wallet_exists(mock_db):
    user = _get_user()
    mock_db.session.add(user)
    mock_db.session.commit()
    db_user = UserModel.query.first()
    wallet_1 = _get_wallet(db_user.id)
    wallet_2 = _get_wallet(db_user.id)
    mock_db.session.add(wallet_1)
    mock_db.session.add(wallet_2)
    with pytest.raises(IntegrityError):
        mock_db.session.commit()


def test_category_exists(mock_db):
    user = _get_user()
    mock_db.session.add(user)
    mock_db.session.commit()
    db_user = UserModel.query.first()
    wallet_1 = _get_wallet(db_user.id)
    mock_db.session.add(wallet_1)
    mock_db.session.commit()

    db_wallet = WalletModel.query.first()
    categories_1 = _get_categories(db_wallet.id)
    categories_2 = _get_categories(db_wallet.id)
    mock_db.session.add(categories_1)
    mock_db.session.add(categories_2)
    with pytest.raises(IntegrityError):
        mock_db.session.commit()


def test_delete_user(mock_db):
    user = _get_user()
    mock_db.session.add(user)
    mock_db.session.commit()
    db_user = UserModel.query.first()
    wallet_1 = _get_wallet(db_user.id)
    mock_db.session.add(wallet_1)
    mock_db.session.commit()
    db_wallet = WalletModel.query.first()
    categories_1 = _get_categories(db_wallet.id)
    mock_db.session.add(categories_1)
    db_user = UserModel.query.first()
    mock_db.session.delete(user)
    mock_db.session.commit()
    assert WalletModel.query.first() is None
    assert CategoryModel.query.first() is None
    assert UserModel.query.first() is None