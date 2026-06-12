# Veloc API Entegrasyon

## Tek Yapman Gereken

Her dilde, her yerde calisir:

```
POST https://a35823-51ce.e.jrnm.app/chat

Header:
  Authorization: Bearer veloc-XXXXXXXXXXXXXXXX
  Content-Type: application/json

Body:
  {"message": "merhaba"}
```

---

## Ornekler

### cURL (Terminal)
```bash
curl -X POST https://a35823-51ce.e.jrnm.app/chat -H "Authorization: Bearer veloc-XXXXXXXXXXXXXXXX" -H "Content-Type: application/json" -d '{"message": "merhaba"}'
```

### Postman
1. POST sec
2. URL: `https://a35823-51ce.e.jrnm.app/chat`
3. Headers:
   - Authorization: `Bearer veloc-XXXXXXXXXXXXXXXX`
   - Content-Type: `application/json`
4. Body > raw > JSON:
```json
{"message": "merhaba"}
```
5. Send

### Insomnia
Ayni sekilde Postman gibi kur.

---

## Her Dilde Ayni Sekilde

| Dil     | Kutuphane          | Kod                                          |
|---------|--------------------|----------------------------------------------|
| Python  | requests           | `requests.post(url, json={"message":"x"}, headers={"Authorization":"Bearer KEY"})` |
| JS      | fetch              | `fetch(url, {method:"POST", headers:{"Authorization":"Bearer KEY","Content-Type":"application/json"}, body:JSON.stringify({message:"x"})})` |
| Java    | HttpURLConnection  | POST + Authorization header + JSON body      |
| Swift   | URLSession         | URLRequest + POST + Authorization header     |
| Flutter | http               | `http.post(url, headers:{...}, body: jsonEncode({...}))` |
| C#      | HttpClient         | `client.PostAsJsonAsync(url, new{message="x"})` |
| PHP     | curl               | `curl_setopt($ch, CURLOPT_HTTPHEADER, [...])`|
| Go      | net/http           | `http.NewRequest("POST", url, body)`         |
| Ruby    | Net::HTTP          | `Net::HTTP::Post.new(uri)`                   |
| Rust    | reqwest            | `client.post(url).json(&json!({...}))`       |

---

## Key Nerede?
Bot'a `/test_paid` yaz veya "API Satın Al" → "Ödeme Yap" ile key al.
Key `veloc-XXXXXXXXXXXXXXXX` formatinda olur.
