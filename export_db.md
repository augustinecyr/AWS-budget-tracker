# Exporting .sql file script

#!/bin/bash

# Variables

```
RDS_ENDPOINT="rds_endpoint_url"
USERNAME="admin"
DATABASE_NAME="budget_tracker"
EXPORT_FILE="/tmp/budget_tracker.sql"
```

# Export database to a file

```
mysqldump -h $RDS_ENDPOINT -u $USERNAME -p $DATABASE_NAME > $EXPORT_FILE
```

# Check if the dump was successful

```
if [ $? -eq 0 ]; then
    echo "Database export successful"
else
    echo "Database export failed"
    exit 1
fi
```

# Clean up

```
rm $EXPORT_FILE
```
