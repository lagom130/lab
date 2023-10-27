import 'package:flutter/material.dart';

main () => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Text in Container widget',
        home: Scaffold(
          body: Center(
            child: Container(
              child: new Text(
                'Hello Flutter and Dart',
                style: TextStyle(
                  fontSize: 20.0,
                ),
              ),
              alignment: Alignment.center,
              width: 500.0,
              height: 400.0,
              color: Colors.lightBlue,
            ),
          ),
        )
    );
  }

}