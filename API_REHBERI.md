# Veloc API Entegrasyon Rehberi

## Base URL
```
https://a35823-51ce.e.jrnm.app
```

## Kimlik Dogrulama
Tum isteklerde header'da API key gerekli:
```
Authorization: Bearer veloc-XXXXXXXXXXXXXXXX
```

## Endpoint
```
POST /chat
```

## Request Body
```json
{
  "message": "Merhaba, nasılsın?"
}
```

## Response
```json
{
  "reply": "selam kanka iyiyim sende naber",
  "model": "veloc-ai",
  "status": "ok"
}
```

---

## Kullanim Ornekleri

### Python
```python
import requests

r = requests.post(
    "https://a35823-51ce.e.jrnm.app/chat",
    json={"message": "merhaba"},
    headers={"Authorization": "Bearer veloc-XXXXXXXXXXXXXXXX"}
)
print(r.json()["reply"])
```

### JavaScript (Node.js)
```javascript
const r = await fetch("https://a35823-51ce.e.jrnm.app/chat", {
  method: "POST",
  headers: {
    "Authorization": "Bearer veloc-XXXXXXXXXXXXXXXX",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({message: "merhaba"})
});
const data = await r.json();
console.log(data.reply);
```

### JavaScript (Browser)
```javascript
fetch("https://a35823-51ce.e.jrnm.app/chat", {
  method: "POST",
  headers: {
    "Authorization": "Bearer veloc-XXXXXXXXXXXXXXXX",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({message: "merhaba"})
})
.then(r => r.json())
.then(data => console.log(data.reply));
```

### cURL
```bash
curl -X POST https://a35823-51ce.e.jrnm.app/chat \
  -H "Authorization: Bearer veloc-XXXXXXXXXXXXXXXX" \
  -H "Content-Type: application/json" \
  -d '{"message": "merhaba"}'
```

### PHP
```php
$ch = curl_init("https://a35823-51ce.e.jrnm.app/chat");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer veloc-XXXXXXXXXXXXXXXX",
    "Content-Type: application/json"
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(["message" => "merhaba"]));
$result = json_decode(curl_exec($ch), true);
echo $result["reply"];
```

### Java
```java
import java.net.http.*;

HttpClient client = HttpClient.newHttpClient();
String json = "{\"message\": \"merhaba\"}";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://a35823-51ce.e.jrnm.app/chat"))
    .header("Authorization", "Bearer veloc-XXXXXXXXXXXXXXXX")
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
```

### Go
```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
    body, _ := json.Marshal(map[string]string{"message": "merhaba"})
    req, _ := http.NewRequest("POST", "https://a35823-51ce.e.jrnm.app/chat", bytes.NewBuffer(body))
    req.Header.Set("Authorization", "Bearer veloc-XXXXXXXXXXXXXXXX")
    req.Header.Set("Content-Type", "application/json")

    resp, _ := http.DefaultClient.Do(req)
    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    fmt.Println(result["reply"])
}
```

### Ruby
```ruby
require 'net/http'
require 'json'

uri = URI("https://a35823-51ce.e.jrnm.app/chat")
req = Net::HTTP::Post.new(uri)
req["Authorization"] = "Bearer veloc-XXXXXXXXXXXXXXXX"
req["Content-Type"] = "application/json"
req.body = {message: "merhaba"}.to_json

response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
puts JSON.parse(response.body)["reply"]
```

### Swift
```swift
import Foundation

let url = URL(string: "https://a35823-51ce.e.jrnm.app/chat")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("Bearer veloc-XXXXXXXXXXXXXXXX", forHTTPHeaderField: "Authorization")
request.setValue("application/json", forHTTPHeaderField: "Content-Type")
request.httpBody = try? JSONSerialization.data(withJSONObject: ["message": "merhaba"])

let task = URLSession.shared.dataTask(with: request) { data, response, error in
    let json = try? JSONSerialization.jsonObject(with: data!) as? [String: Any]
    print(json?["reply"] ?? "")
}
task.resume()
```

### Dart (Flutter)
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

final response = await http.post(
  Uri.parse('https://a35823-51ce.e.jrnm.app/chat'),
  headers: {
    'Authorization': 'Bearer veloc-XXXXXXXXXXXXXXXX',
    'Content-Type': 'application/json',
  },
  body: jsonEncode({'message': 'merhaba'}),
);
print(jsonDecode(response.body)['reply']);
```

### C# (.NET)
```csharp
using System.Net.Http;
using System.Net.Http.Headers;

var client = new HttpClient();
client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", "veloc-XXXXXXXXXXXXXXXX");

var response = await client.PostAsJsonAsync("https://a35823-51ce.e.jrnm.app/chat", new { message = "merhaba" });
var result = await response.Content.ReadFromJsonAsync<dynamic>();
Console.WriteLine(result.reply);
```

### Rust
```rust
use reqwest::Client;
use serde_json::json;

#[tokio::main]
async fn main() {
    let client = Client::new();
    let resp = client.post("https://a35823-51ce.e.jrnm.app/chat")
        .header("Authorization", "Bearer veloc-XXXXXXXXXXXXXXXX")
        .json(&json!({"message": "merhaba"}))
        .send().await.unwrap()
        .json::<serde_json::Value>().await.unwrap();
    println!("{}", resp["reply"]);
}
```

---

## Hata Kodlari
| Kod | Anlam |
|-----|-------|
| 200 | Basarili |
| 401 | Gecersiz API key |
| 400 | Message alani bos |
| 429 | Cok fazla istek (rate limit) |
| 500 | Sunucu hatasi |

## Ornek Hata Response
```json
{
  "error": "Gecersiz API key"
}
```
