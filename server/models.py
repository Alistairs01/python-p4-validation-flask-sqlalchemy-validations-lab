from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, a_name):
       
        if not a_name or Author.query.filter(Author.name == a_name).first():
            raise ValueError("Name must be a unique, non-empty string")
        return a_name
    
    @validates("phone_number")
    def validate_phone_number(self, key, number):
        x = len(number)
        if not number.isdigit() or x != 10:
            raise ValueError("Phone number must be 10 digits")
        return number
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validates_title(self, key,a_title):

        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        
        if not a_title:
            raise ValueError("Title must be non-empty string")
        if not any(word in a_title for word in clickbait):
            raise ValueError("Title not clickbait-y enough")
        return a_title
    
    @validates('content')
    def validates_content(self, key, some_content):
        if len(some_content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return some_content
    
    @validates('category')
    def validates_category(self, key, a_category):
        if a_category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return a_category
    
    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be less than 250 characters long")
        return summary


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'