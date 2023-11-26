from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
# from app.models.contact import Contact
# from app.models.contactBlog import BlogEntry
from app.models.authuser import AuthUser, PrivateBoxpost
from app.models.boxpost import FindBlog


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        AuthUser(email="flask@204212", name='สมชาย ทรงแบด',password=generate_password_hash('1234',method='sha256'),avatar_url='https://ui-avatars.com/api/?name=\สมชาย+ทรงแบด&background=83ee03&color=fff'))
    # db.session.add(
    #     PrivateContact(firstname='ส้มโอ', lastname='โอเค',phone='081-111-1112', owner_id=1))
    # db.session.add(
    #     PrivateContactblog(name='สมชาย ทรงแบด', message='วันนี้กินไรดีอ่ะ', email='somchan@gmail.com', owner_id=1))
    # db.session.add(
    #     Contact(firstname='สมชาย', lastname='ทรงแบด', phone='081-111-1111'))
    db.session.add(
        PrivateBoxpost(name='สมชาย ทรงแบด', email='somchan@gmail.com',category='Pet', idPet='ตามหาเจ้าของ' ,filenameIMG='_cow.jpeg', subdist="บ้านทับ", district="แม่แจ่ม",province="เชียงใหม่" ,detail="น้องหมามีลายขาวดำคล้ายวัว", tel="0801235674", owner_id=1))
    #db.session.add(
       #(name='สมชาย ทรงแบด', email='somchan@gmail.com',category='Pet', filenameIMG='_cow.jpeg', subdist="บ้านทับ", district="แม่แจ่ม",province="เชียงใหม่" ,detail="น้องหมามีลายขาวดำคล้ายวัว", tel="0801235674"))
    db.session.commit()


if __name__ == "__main__":
    cli()