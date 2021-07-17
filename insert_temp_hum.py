import os
import time

import dht11
import psycopg2
import RPi.GPIO as GPIO

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=14)


def execute_sql() -> None:

    try:
        # connect DB
        con = psycopg2.connect(
            dbname="sieep",
            user="pi",
            password=os.environ.get("DB_PASSWORD"),
        )
        cursor = con.cursor()

        while True:
            # Get temperature and humidity
            result = instance.read()
            if result.is_valid():
                print("Temperature: %-3.1f C" % result.temperature)
                print("Humidity: %-3.1f %%" % result.humidity)
                cursor.execute(
                    f"INSERT INTO room_status(temperature, humidity) VALUES({result.temperature}, {result.humidity});"
                )
                con.commit()
            time.sleep(1)

    except Exception as e:
        print(e)

    finally:
        GPIO.cleanup()
        cursor.close()
        con.close()


if __name__ == "__main__":
    execute_sql()
