import 'package:flutter/material.dart';

main() => runApp(MyApp());

class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ListView Simple',
      home: Scaffold(
        appBar: AppBar(
          title: Text('Flutter Demo'),
        ),
        body: GridView.count(
            padding: const EdgeInsets.all(20.0),
          crossAxisSpacing: 10.0,
          mainAxisSpacing: 20.0,
          crossAxisCount: 3,
          childAspectRatio: 3/4,
          children: [
            Container(
              color: Colors.indigoAccent,
            ),
            Container(
              color: Colors.blueGrey,
            ),
            Container(
              color: Colors.redAccent,
            ),
            Container(
              color: Colors.cyanAccent,
            ),
          ],
        ),
      ),
    );
  }
}