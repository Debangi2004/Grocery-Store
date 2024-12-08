from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao

def get_all_products(connection):
    cursor = connection.cursor()
    query = ("select products.product_id, products.name, products.unit_of_measurement, products.price_per_unit, unit_of_measurement.unit_of_measurement from products inner join unit_of_measurement on products.unit_of_measurement_id=unit_of_measurement.unit_of_measurement_id")
    cursor.execute(query)
    response = []
    for (product_id, name, unit_of_measurement, price_per_unit, unit_of_measurement_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'unit_of_measurement': unit_of_measurement,
            'price_per_unit': price_per_unit,
            'unit_of_measurement_name': unit_of_measurement_name
        })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products "
             "(name, unit_of_measurement, price_per_unit)"
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['unit_of_measurement'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_products(connection))
    print(insert_new_product(connection, {
        'product_name': 'potatoes',
        'uom_id': '1',
        'price_per_unit': 10
    }))