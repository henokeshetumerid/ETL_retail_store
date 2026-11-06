
#!/bin/bash

# Check the number of arguments
if [ "$#" -ne 2 ]; then
    echo "Incorrect number of arguments."
    echo "Usage: $0 destination database"
else
    backup_file_name="$1/backup_$(date +%Y%m%d_%H%M%S).sql"

    # Check whether the database exists
    if ! psql -h postgres -U postgres -p 5432 -lqt |
        cut -d '|' -f 1 | grep -qw "$2"; then
        echo "Database does not exist"
    else
        # Create the backup
        if pg_dump -h postgres -U postgres -p 5432 \
            -d "$2" -f "$backup_file_name"; then

            echo "Backup completed: $backup_file_name"

            # Keep the latest two backups
            ls -1t "$1"/backup_*.sql |
                tail -n +3 | xargs -r rm --

        else
            echo "Backup failed"
            exit 1
        fi
    fi
fi