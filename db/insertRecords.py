import dbconnect
import pandas as pd
import ast
import os
import sys
from sqlalchemy import create_engine
def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Get the database connection
    conn = dbconnect.connect()
    # Create a SQLAlchemy engine
    engine = create_engine('mysql+mysqlconnector://admin:12345678@comp4442-gp.crqk44cigx2u.us-east-1.rds.amazonaws.com:3306/comp4442-gp', echo=False)

    file1 = os.path.join(script_dir, 'part-00000')
    file2 = os.path.join(script_dir, 'part-00001')

    # Read the data from the files
    with open(file1, 'r',encoding='utf-8') as f:
        data1 = [ast.literal_eval(line) for line in f]

    with open(file2, 'r',encoding='utf-8') as f:
        data2 = [ast.literal_eval(line) for line in f]

    # Concatenate the two lists
    data = data1 + data2
    flat_data = [(t[0], t[1], t[2], *l) for t, l in data]

    

    # Convert the list of tuples to a DataFrame
    df = pd.DataFrame(flat_data, columns=['DriverID', 'CarPlateNumber', 'DrivingDate',  'isRapidlySpeedup', 'isRapidlySlowdown', 'isNeutralSlide', 'isNeutralSlideFinished', 'neutralSlideTime', 'isOverspeed', 'isOverspeedFinished', 'overspeedTime', 'isFatigueDriving', 'isHthrottleStop', 'isOilLeak'])

    df.to_csv('output.csv', index=False,encoding='utf-8-sig')
    
    cursor = conn.cursor()
    try:
        # Delete all rows from the Records table
        cursor.execute("DELETE FROM Records")
        
        # Reset auto-increment counter
        cursor.execute("ALTER TABLE Records AUTO_INCREMENT = 1")
        conn.commit()   
       # Bulk insert the DataFrame into the SQL table
        df.to_sql('Records', con=engine, if_exists='append', index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print('Data stored successfully.')
    finally:
        cursor.close()
        conn.close()
        sys.exit()
if __name__ == "__main__":
    main()