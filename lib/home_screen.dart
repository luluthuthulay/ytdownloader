import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  InAppWebViewController? webViewController;
  String currentUrl = "https://m.youtube.com"; // စစချင်း ပွင့်မည့် Web
  double progress = 0;
  final TextEditingController urlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    urlController.text = currentUrl;
  }

  // ဒေါင်းလုဒ်ခလုတ် နှိပ်လိုက်လျှင် အလုပ်လုပ်မည့် Function
  void _onDownloadClicked() {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return Container(
          padding: const EdgeInsets.all(20),
          height: 200,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "ဗီဒီယို ဒေါင်းလုဒ်လုပ်ရန်",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Text("လက်ရှိလင့်ခ်: $currentUrl"),
              const SizedBox(height: 20),
              const Text(
                "မှတ်ချက် - ဤနေရာတွင် နောက်ပိုင်း yt-dlp ဖြင့်ချိတ်ဆက်ပြီး Video Quality များ (1080p, 720p, MP3) ရွေးချယ်နိုင်သော စနစ် ထည့်သွင်းပါမည်။",
                style: TextStyle(color: Colors.red),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.redAccent,
        title: TextField(
          controller: urlController,
          decoration: const InputDecoration(
            hintText: "Search or enter URL",
            filled: true,
            fillColor: Colors.white,
            contentPadding: EdgeInsets.symmetric(horizontal: 10),
            border: OutlineInputBorder(borderSide: BorderSide.none),
          ),
          onSubmitted: (value) {
            String url = value;
            if (!url.startsWith("http")) {
              url = "https://www.google.com/search?q=$value";
            }
            webViewController?.loadUrl(
                urlRequest: URLRequest(url: WebUri(url)));
          },
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.arrow_back, color: Colors.white),
            onPressed: () {
              webViewController?.goBack();
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          InAppWebView(
            initialUrlRequest: URLRequest(url: WebUri(currentUrl)),
            onWebViewCreated: (controller) {
              webViewController = controller;
            },
            onLoadStart: (controller, url) {
              setState(() {
                currentUrl = url.toString();
                urlController.text = currentUrl;
              });
            },
            onProgressChanged: (controller, progress) {
              setState(() {
                this.progress = progress / 100;
              });
            },
          ),
          if (progress < 1.0)
            LinearProgressIndicator(value: progress, color: Colors.red),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _onDownloadClicked,
        backgroundColor: Colors.redAccent,
        child: const Icon(Icons.download, color: Colors.white),
      ),
    );
  }
}
