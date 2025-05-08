import psycopg2
from psycopg2 import sql

# Database configuration
db_config = {
    'dbname': 'task_manager',
    'user': 'postgres',
    'password': 'Omharrydh99@',
    'host': 'localhost',
    'port': '5433'
}

def connect_db():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def create_task(title, description):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tasks (title, description) 
                    VALUES (%s, %s) RETURNING id;
                    """,
                    (title, description)
                )
                task_id = cur.fetchone()[0]
                conn.commit()
                print(f"Task created with ID: {task_id}")
        except Exception as e:
            print("Error creating task:", e)
        finally:
            conn.close()

def read_tasks():
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks;")
                tasks = cur.fetchall()
                for task in tasks:
                    print(task)
        except Exception as e:
            print("Error reading tasks:", e)
        finally:
            conn.close()

def update_task(task_id, title=None, description=None, completed=None):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                updates = []
                params = []

                if title:
                    updates.append("title = %s")
                    params.append(title)
                if description:
                    updates.append("description = %s")
                    params.append(description)
                if completed is not None:
                    updates.append("completed = %s")
                    params.append(completed)

                params.append(task_id)
                query = sql.SQL("UPDATE tasks SET {} WHERE id = %s;").format(
                    sql.SQL(", ").join(map(sql.SQL, updates))
                )
                cur.execute(query, params)
                conn.commit()
                print(f"Task {task_id} updated.")
        except Exception as e:
            print("Error updating task:", e)
        finally:
            conn.close()

def delete_task(task_id):
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
                conn.commit()
                print(f"Task {task_id} deleted.")
        except Exception as e:
            print("Error deleting task:", e)
        finally:
            conn.close()

# Main menu
def main():
    while True:
        print("\nTask Manager")
        print("1. Create Task")
        print("2. Read Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            create_task(title, description)
        elif choice == '2':
            read_tasks()
        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (leave blank to skip): ") or None
            description = input("Enter new description (leave blank to skip): ") or None
            completed = input("Is the task completed? (yes/no/skip): ")
            if completed.lower() == 'yes':
                completed = True
            elif completed.lower() == 'no':
                completed = False
            else:
                completed = None
            update_task(task_id, title, description, completed)
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
        elif choice == '5':
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
