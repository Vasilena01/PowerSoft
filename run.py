from app import create_app

app = create_app()

context = ('cert.pem', 'cert-key.pem')
app.run(ssl_context=context)

