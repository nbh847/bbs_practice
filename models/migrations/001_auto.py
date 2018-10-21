"""Peewee migrations -- 001_auto.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Mail(pw.Model):
        id = pw.IntegerField(primary_key=True)
        content = pw.CharField(default='', max_length=800)
        title = pw.CharField(default='', max_length=200)
        read = pw.BooleanField(default=False)
        sender_id = pw.IntegerField()
        receiver_id = pw.IntegerField()
        ct = pw.DateTimeField(default='1970-01-01')

        class Meta:
            db_table = "mail"



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('mail')
