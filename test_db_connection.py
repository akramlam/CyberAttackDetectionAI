from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists
import psycopg2

# Use the same connection string from your config.yaml
connection_string = "postgresql://ids_user:123@localhost:5432/ids_db"

def test_psycopg2_connection():
    """Test direct connection using psycopg2"""
    try:
        conn = psycopg2.connect(
            dbname="ids_db",
            user="ids_user",
            password="123",
            host="localhost",
            port="5432"
        )
        print("✅ Direct psycopg2 connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Psycopg2 connection error: {str(e)}")

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        # Create engine
        engine = create_engine(connection_string)
        
        # Test connection
        if database_exists(engine.url):
            print("✅ SQLAlchemy connection successful!")
            
            # Try to create a test table
            with engine.connect() as conn:
                # Create table
                create_table_sql = text("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY,
                        test_column VARCHAR(50)
                    )
                """)
                conn.execute(create_table_sql)
                print("✅ Created test table!")
                
                # Insert data
                insert_sql = text("""
                    INSERT INTO test_table (test_column) 
                    VALUES ('test_value')
                """)
                conn.execute(insert_sql)
                print("✅ Inserted test data!")
                
                # Clean up
                cleanup_sql = text("DROP TABLE test_table")
                conn.execute(cleanup_sql)
                print("✅ Cleaned up test table!")
                
                # Commit the transaction
                conn.commit()
                
    except Exception as e:
        print(f"❌ SQLAlchemy error: {str(e)}")

if __name__ == "__main__":
    print("Testing database connections...")
    print("\n1. Testing psycopg2 connection:")
    test_psycopg2_connection()
    print("\n2. Testing SQLAlchemy connection:")
    test_sqlalchemy_connection() 