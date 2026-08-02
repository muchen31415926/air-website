from db_wrapper import DBWrapper


def main():
    db = DBWrapper()
    db.delete_docs()


if __name__ == "__main__":
    main()
