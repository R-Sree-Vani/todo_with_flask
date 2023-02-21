from flask import Flask,render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db=SQLAlchemy(app)
class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    todo = db.Column(db.String(100),nullable = False)

    def __repr__(self):
        return f"List('{self.todo}')"

@app.route("/")
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":
        item=request.form.get("todolistitem")
        listitem=ListItem(todo=item)
        
        db.session.add(listitem)
        db.session.commit()    
    ret=ListItem.query.all() 
    return render_template("index.html",ret=ret)


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    item=ListItem.query.filter_by(id=todo_id).first()
    
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/<int:todo_id>",methods=['GET','POST'])
def update(todo_id):
    item=ListItem.query.filter_by(id=todo_id).first()
    if request.method=='POST':
        

        itemtodo=request.form.get("updated")
        item.todo = itemtodo
        db.session.add(item)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("update.html",todo=item)



    

if __name__=='__main__':
    app.run(debug=True)