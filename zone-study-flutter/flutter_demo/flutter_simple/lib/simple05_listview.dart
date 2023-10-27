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
        body: ListView(
          children: [
            ListTile(
              leading: Icon(Icons.perm_camera_mic),
              title: Text('perm_camera_mic'),
            ),
            ListTile(
              leading: Icon(Icons.add_call),
              title: Text('add_call'),
            ),
            ListTile(
              leading: Icon(Icons.games),
              title: Text('games'),
            ),
          ],
        ),
      ),
    );
  }

}