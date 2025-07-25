from .sql import *


with open("output.sql", "w") as f:
    f.write(create_table_sql)
    f.write(create_view_sql)
    f.write(create_index_sql)
    f.write(create_trigger_sql)
    f.write(finalized_sql)
