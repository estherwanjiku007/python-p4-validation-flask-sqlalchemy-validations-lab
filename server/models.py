from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String,db.CheckConstraint("phone_number==10"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    @validates("name")
    def validate_name(self,key,name) :
        # if len(name)<1 and name in Author.name:
        #     raise ValueError("Name must be unique")  
        # return name 
        if not name:
            raise ValueError("Author must have a name")
        elif name in [author.name for author in Author.query.all()]:
            raise ValueError("Author name must be unique")
        else:
            return name
    @validates("phone_number")
    def validate_phone_no(self,key,phone_number) :
        phone_number2="".join(filter(str.isdigit,phone_number))
        if len(phone_number2)!=10:
            raise ValueError("Phone number should be an integer of length  10")  
    
        else:
            return phone_number# Add validators 

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
#     "Won't Believe"
#    - "Secret"
#    -  
#    - "Guess"
   # __table_args__=(db.CheckConstraint("(title!=Won't beleive) or (title!=Secret) or (title!=Top) or (title!=Guess)")raise ValueError )
    # Add validatos  
    @validates("content")
    def validates_content(self,key,content):
        if len(content)<250:
            raise ValueError("post content should be at least 250 characters")
        else:
            return content
    
    @validates("summary")
    def validate_summary(self,key,summary):
        if len(summary)>250:
            raise ValueError("Summary should be a max of 250 characters ")
        else:
            return summary
    
   


    @validates("title")
    def validate_title(self,key,title):
        all_titles=["Won't Believe","Secret","Top", "Guess"]
        if   not  title and title not in all_titles:
            raise ValueError("Title is invalid")
        else:
            return title
        
    @validates("category")
    def validate_category(self,key,category):
        if category!="Fiction" and category!="Non-Fiction":
            raise ValueError("Category should either be fiction on non-fiction") 
        else:
            return category   
      
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
