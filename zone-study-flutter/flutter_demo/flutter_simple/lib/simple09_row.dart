import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'row simple',
      home: Scaffold(
        appBar: AppBar(
         title: Text('row widget demo'),
        ),
        body: Row(
          children: [
            Expanded(
              child: RaisedButton(
                onPressed: (){},
                color: Colors.redAccent,
                child: Text('Red Button'),
              ),
            ),
            Expanded(
              child: RaisedButton(
                onPressed: (){},
                color: Colors.blueAccent,
                child: Text('Blue Button'),
              ),
            ),
            Expanded(
              child: RaisedButton(
                onPressed: (){},
                color: Colors.greenAccent,
                child: Text('Green Button'),
              ),
            ),
          ],
        ),

      ),
    );
  }

}