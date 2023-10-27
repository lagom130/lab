import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'column simple',
      home: Scaffold(
          appBar: AppBar(
            title: Text('column widget demo'),
          ),
          body: Center(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('hi'),
                Expanded(child: Text('flutter')),
                Text('android app'),
              ],
            ),
          ),
      ),
    );
  }
}
