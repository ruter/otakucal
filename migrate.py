# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
"""
python migrate.py db init, migrate, upgrade
"""
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()