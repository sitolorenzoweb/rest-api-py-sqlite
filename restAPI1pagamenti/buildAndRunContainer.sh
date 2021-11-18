docker build -t flaskpaymentsapi:1.0 .
docker run -p 5000:5000 --name FlaskPaymentsAPI flaskpaymentsapi:1.0