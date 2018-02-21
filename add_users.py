from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

"""
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
"""

engine = create_engine('sqlite:///tutorial.db', echo=True)

Session = sessionmaker(bind=engine)
s = Session()
    
usuario = User(username="python", password="python")
s.add(usuario)
s.commit()

usuario = User(username="admin", password="password")
s.add(usuario)
s.commit()