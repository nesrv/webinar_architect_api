
### ** Проектирование API – SOAP**  



## **1. Введение **  
### **1.1 Что такое SOAP?**  
- **SOAP** (Simple Object Access Protocol) – протокол для обмена структурированными сообщениями в распределённых системах.  
- Работает поверх **HTTP/HTTPS**, использует **XML**.  
- Основные компоненты:  
  - **Envelope** – корневой элемент.  
  - **Header** (опционально) – метаданные (аутентификация, логирование).  
  - **Body** – данные запроса/ответа.  

### **1.2 Когда используют SOAP?**  
- **Корпоративные системы** (банки, госучреждения).  
- **Сложные транзакции** (например, платежи).  
- **Строгая типизация и безопасность** (WS-Security, SSL).  

**Пример SOAP-запроса:**  
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUserRequest xmlns="http://example.com/">
      <UserId>123</UserId>
    </GetUserRequest>
  </soap:Body>
</soap:Envelope>
```

---

