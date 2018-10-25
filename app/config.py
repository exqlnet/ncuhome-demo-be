class Default:

    SQLALCHEMY_URI = r"sqlite:///.\demo.db"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


config = {
    "default": Default,
}
