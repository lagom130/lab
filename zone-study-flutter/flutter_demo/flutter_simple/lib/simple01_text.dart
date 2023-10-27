import 'package:flutter/material.dart';

main () => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Text widget',
      home: Scaffold(
        body: Center(
          child: Text(
            'hello flutter, aba1 aba2 aba3 aba4 aba5 aba6 aba7 aba8 aba9 aba0, hello flutter, aba1 aba2 aba3 aba4 aba5 aba6 aba7 aba8 aba9 aba0, hello flutter, aba1 aba2 aba3 aba4 aba5 aba6 aba7 aba8 aba9 aba0, hello flutter, aba1 aba2 aba3 aba4 aba5 aba6 aba7 aba8 aba9 aba0',
            textAlign: TextAlign.left,
            maxLines: 4,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(
              fontSize: 18.0,
              // color: Color.fromARGB(255, 255, 0, 0),
              color: Color(0x9966CCFF),
              decoration: TextDecoration.lineThrough,
              decorationStyle: TextDecorationStyle.solid,
            ),
          ),
        ),
      )
    );
  }

}