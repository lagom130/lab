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
        body: Center(
          child: Container(
            height: 200.0,
            child: MyList(),
          ),
        ),
      ),
    );
  }
}

class MyList extends StatelessWidget{
  @override
  Widget build(BuildContext context) {
    return ListView(
      scrollDirection: Axis.horizontal,
      children: [
        new Container(
          width: 150.0,
          color: Colors.indigoAccent,
        ),
        new Container(
          width: 150.0,
          color: Colors.lightGreen,
        ),
        new Container(
          width: 150.0,
          color: Colors.yellowAccent,
        ),
        new Container(
          width: 150.0,
          color: Colors.blueGrey,
        ),
      ],
    );
  }

}