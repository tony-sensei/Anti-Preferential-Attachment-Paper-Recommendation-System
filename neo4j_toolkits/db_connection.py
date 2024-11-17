import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file located one parent directory above
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

# Neo4j connection details
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

def get_db_driver():
    """
    Initialize and return the Neo4j database driver.
    """
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        return driver
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def close_driver(driver):
    """
    Close the Neo4j database driver.
    """
    if driver:
        driver.close()

def test_connection():
    """
    Test the connection to the Neo4j database by running a simple query.
    """
    driver = None
    try:
        print("Testing connection to Neo4j...")
        driver = get_db_driver()
        with driver.session(database="neo4j") as session:
            result = session.run("RETURN 'Connection successful!' AS message")
            for record in result:
                print(record["message"])
        print("Connection test passed.")
    except Exception as e:
        print(f"Connection test failed: {e}")
    finally:
        close_driver(driver)

# Run the connection test when this script is executed directly
if __name__ == "__main__":
    test_connection()
