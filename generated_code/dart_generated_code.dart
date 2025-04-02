import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
class CodeData {
  final String language;
  final String framework;
  final String description;
  CodeData({required this.language, required this.framework, required this.description});
  Map<String, dynamic> toJson() => {
        'language': language,
        'framework': framework,
        'description': description,
      };
}
StatefulWidget createCodeSubmissionPage({required String apiUrl}) {
  final _formKey = GlobalKey<FormState>();
  String _language = '';
  String _framework = '';
  String _description = '';
  Future<void> _submitData() async {
    if (_formKey.currentState!.validate()) {
      final codeData = CodeData(language: _language, framework: _framework, description: _description);
      final response = await http.post(Uri.parse(apiUrl),
          headers: <String, String>{
            'Content-Type': 'application/json; charset=UTF-8',
          },
          body: jsonEncode(codeData.toJson()));
      if (response.statusCode == 200) {
      } else {
      }
    }
  }
  return Scaffold(
    appBar: AppBar(title: Text('Code Submission')),
    body: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          children: [
            TextFormField(
              decoration: InputDecoration(labelText: 'Language'),
              validator: (value) => value == null || value.isEmpty ? 'Please enter a language' : null,
              onChanged: (value) => _language = value,
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Framework'),
              validator: (value) => value == null || value.isEmpty ? 'Please enter a framework' : null,
              onChanged: (value) => _framework = value,
            ),
            TextFormField(
              decoration: InputDecoration(labelText: 'Code Description'),
              validator: (value) => value == null || value.isEmpty ? 'Please enter a description' : null,
              onChanged: (value) => _description = value,
              maxLines: null,
            ),
            ElevatedButton(
              onPressed: _submitData,
              child: Text('Submit'),
            ),
          ],
        ),
      ),
    ),
  );
}