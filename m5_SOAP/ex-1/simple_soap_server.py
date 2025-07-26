from flask import Flask, request, Response
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/cinema', methods=['POST'])
def soap_service():
    # Парсим SOAP запрос
    soap_body = request.data.decode('utf-8')
    
    # Простой парсинг для демонстрации
    if 'get_movies' in soap_body:
        response = '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <get_movies_response>
            <movie>
                <id>1</id>
                <title>Матрица</title>
                <genre>Фантастика</genre>
            </movie>
            <movie>
                <id>2</id>
                <title>Титаник</title>
                <genre>Драма</genre>
            </movie>
        </get_movies_response>
    </soap:Body>
</soap:Envelope>'''
    else:
        response = '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <soap:Fault>
            <faultcode>Client</faultcode>
            <faultstring>Method not found</faultstring>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>'''
    
    return Response(response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)