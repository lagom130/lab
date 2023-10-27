import 'package:flutter/material.dart';

main() => runApp(MyApp(
  items: List<String>.generate(1000, (index) => 'Item $index')
));

class MyApp extends StatelessWidget {

  final List<String> items;

  MyApp({Key key, @required this.items}) : super(key:key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ListView Simple',
      home: Scaffold(
        appBar: AppBar(
          title: Text('Flutter Demo'),
        ),
        body: ListView.builder(
          itemCount: items.length,
          itemBuilder: (context, index) => ListTile(
            title: Text('${items[index]}'),
          ),
        ),
      ),
    );
  }
}