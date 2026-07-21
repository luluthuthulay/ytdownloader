import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  InAppWebViewController? webViewController;
  String currentUrl = "https://www.youtube.com";
  bool isDownloading = false;
  double downloadProgress = 0.0;

  @override
  void initState() {
    super.initState();
    requestPermissions();
  }

  // ဖုန်းထဲတွင် ဖိုင်သိမ်းဆည်းရန် ခွင့်တောင်းခြင်း
  Future<void> requestPermissions() async {
    var status = await Permission.storage.request();
    if (!status.isGranted) {
      await Permission.manageExternalStorage.request();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("VidMate Clone - Browser"),
        backgroundColor: Colors.red,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              webViewController?.reload();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Browser အပိုင်း
          Expanded(
            child: InAppWebView(
              initialUrlRequest: URLRequest(url: WebUri(currentUrl)),
              onWebViewCreated: (controller) {
                webViewController = controller;
              },
              onLoadStop: (controller, url) {
                setState(() {
                  currentUrl = url.toString();
                });
              },
            ),
          ),
          
          // အောက်ခြေမှ ဗီဒီယိုဒေါင်းလုပ်ဆွဲမည့် ခလုတ်နှင့် နေရာ
          Container(
            padding: const EdgeInsets.all(12.0),
            color: Colors.grey[200],
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (isDownloading)
                  LinearProgressIndicator(value: downloadProgress),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        currentUrl,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontSize: 12),
                      ),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton.icon(
                      onPressed: isDownloading ? null : () {
                        // ဤနေရာတွင် ဒေါင်းလုဒ်လုပ်မည့် လုပ်ဆောင်ချက်ကို ထည့်သွင်းနိုင်ပါသည်
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("ဒေါင်းလုဒ်ဆွဲရန် လင့်ခ်ကို ရယူနေပါပြီ...")),
                        );
                      },
                      icon: const Icon(Icons.download),
                      label: const Text("Download"),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        foregroundColor: Colors.white,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
