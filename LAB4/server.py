import http.server
import socketserver
import json
import re

with open('products.json') as f:
    products = json.load(f)

home_page = "<h2>Welcome to the Home Page</h2>"
about_page = "<h2>About Us</h2>"
contacts_page = "<h2>Contact Us</h2>"
product_template = "<h2>{name}</h2><p><b>Author:</b> {author}</p><p><b>Price:</b> {price}</p><p><b>Description:</b> {description}</p>"
product_list = "<h2>Products</h2>"

class handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(home_page.encode())
        elif self.path == '/about':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(about_page.encode())
        elif self.path == '/contacts':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(contacts_page.encode())
        elif self.path == '/product':
            product_page = product_list
            for i in range(len(products)):
                product_page += (f"<p><a href=\"/product/{i+1}\">{products[i]['name']}</a></p>")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(product_page.encode())
        elif re.match(r'/product/\d+', self.path):
            product_id = int(self.path.split('/')[-1])
            if 0 < product_id <= len(products):
                product = products[product_id - 1]
                product_page = product_template.format(**product)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(product_page.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write("Product not found".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Page not found".encode())

with socketserver.TCPServer(("", 8080), handler) as httpd:
    print("Server started on port 8080")
    httpd.serve_forever()