import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var card = new Card(
      child: Column(
        children: [
          ListTile(
            title: Text(
              '江苏省苏州市工业园区XX街XX号',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: Text('路人甲: 1XXXXXXXXXX'),
            leading: Icon(Icons.account_box, color: Colors.lightBlue,),
          ),
          Divider(),
          ListTile(
            title: Text(
              '江苏省苏州市工业园区XX街XX号',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: Text('路人甲: 1XXXXXXXXXX'),
            leading: Icon(Icons.account_box, color: Colors.lightBlue,),
          ),
        ],
      ),
    );

    var card2 = new Card(
      child: Column(
        children: [
          ListTile(
            title: Text(
              '江苏省苏州市工业园区XX街XX号',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: Text('路人甲: 1XXXXXXXXXX'),
            leading: Icon(Icons.account_box, color: Colors.lightBlue,),
          ),
          Divider(),
          ListTile(
            title: Text(
              '江苏省苏州市工业园区XX街XX号',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: Text('路人甲: 1XXXXXXXXXX'),
            leading: Icon(Icons.account_box, color: Colors.lightBlue,),
          ),
          Divider(),
          ListTile(
            title: Text(
              '江苏省苏州市工业园区XX街XX号',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: Text('路人甲: 1XXXXXXXXXX'),
            leading: Icon(Icons.account_box, color: Colors.lightBlue,),
          ),
        ],
      ),
    );
    return MaterialApp(
      title: 'position simple',
      home: Scaffold(
        appBar: AppBar(
          title: Text('positioned widget demo'),
        ),
        body: Column(
          children: [
            card,
            card2
          ],
        ),
      ),
    );
  }
}
