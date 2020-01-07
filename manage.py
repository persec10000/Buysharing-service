from app import create_app

# from app import blueprint

app = create_app('dev')
# api.init_app(app)


# app.register_blueprint(blueprint)
# app.app_context().push()
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)



# @manager.command
# def run():
#     app.run(host='0.0.0.0')


if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host='192.168.207.74', port=5001)
