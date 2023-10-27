import 'package:flutter/material.dart';

main () => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Image widget',
        home: Scaffold(
          body: Center(
            child: Container(
              child: new Image.network(
                'https://tvax3.sinaimg.cn/crop.0.0.1006.1006.1024/a8ae9c88ly8g6s4yhba01j20ry0ryq4e.jpg?KID=imgbed,tva&Expires=1613215504&ssig=Ha%2Bu5BSIpL',
                fit: BoxFit.contain,
                color: Colors.grey,
                colorBlendMode: BlendMode.color,
                repeat: ImageRepeat.repeatX,
              ),
              width: 300.0,
              height: 200.0,
              color: Colors.lightBlue,
            ),
          ),
        )
    );
  }

}