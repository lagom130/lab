import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '页面跳转返回数据',
      home: FirstPage(),
    );
  }
}

class FirstPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('say hi'),
      ),
      body: Center(
        child: RouteButton(),
      ),
    );
  }
}

class RouteButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RaisedButton(onPressed: (){_navigateToGirl(context);}, child: Text('find girl'),);
  }

  _navigateToGirl(BuildContext context) async{
    final result = await Navigator.push(context, MaterialPageRoute(builder: (context) => Girl()));
    Scaffold.of(context).showSnackBar(SnackBar(content: Text('$result')));
  }
}

class Girl extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('your girl'),
      ),
      body: Center(
        child: Column(
          children: [
            RaisedButton(
              child: Text('Girl A'),
              onPressed: () => Navigator.pop(context, 'Girl A say hi'),
            ),
            RaisedButton(
              child: Text('Girl B'),
              onPressed: () => Navigator.pop(context, 'Girl B say hi'),
            ),
            RaisedButton(
              child: Text('Girl C'),
              onPressed: () => Navigator.pop(context, 'Girl C say hi'),
            )
          ],
        )
      )
    );
  }
}

