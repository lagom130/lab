import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Stack stack = Stack(
      alignment: const FractionalOffset(0.5, 0.8),
      children: [
        CircleAvatar(
          backgroundImage: NetworkImage(
              'https://tvax3.sinaimg.cn/crop.0.0.1006.1006.1024/a8ae9c88ly8g6s4yhba01j20ry0ryq4e.jpg?KID=imgbed,tva&Expires=1613215504&ssig=Ha%2Bu5BSIpL'),
          radius: 100.0,
        ),
        Container(
          decoration: BoxDecoration(color: Colors.lightBlue),
          padding: EdgeInsets.all(5.0),
          child: Text(
            'RIKU',
            style: TextStyle(color: Colors.white),
          ),
        )
      ],
    );
    return MaterialApp(
      title: 'stack simple',
      home: Scaffold(
        appBar: AppBar(
          title: Text('stack widget demo'),
        ),
        body: Center(
          child: stack,
        ),
      ),
    );
  }
}
