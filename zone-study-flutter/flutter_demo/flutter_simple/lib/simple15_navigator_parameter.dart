import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'navigator simple',
      home: ProductList(
          products: List.generate(
              100, (index) => Product('product-$index', 'desc info $index'))
      ),
    );
  }
}

class ProductList extends StatelessWidget {
  final List<Product> products;

  ProductList({Key key, @required this.products});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('product list page'),
      ),
      body: ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) =>
            ListTile(
              title: Text(products[index].title),
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => ProductDetail(product: products[index]))
              ),
            ),
      ),
    );
  }
}

class ProductDetail extends StatelessWidget {
  final Product product;

  ProductDetail({Key key, @required this.product});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(product.title),
      ),
      body: Center(
        child: Text(product.desc),
      )
    );
  }
}

class Product {
  final String title;
  final String desc;

  Product(this.title, this.desc);
}

