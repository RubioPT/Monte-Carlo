# Monte Carlo Algoritması ile Özel Eleman Tespiti

Bu proje, büyük bir veri seti ($n = 10^6$) içerisinde belirli bir matematiksel koşulu (`eleman % 7 == 3`) sağlayan sayıların oranını, **Monte Carlo Algoritması** kullanarak tahmin etmek ve bu tahminlerin doğruluğunu teorik hata sınırlarıyla analiz etmek amacıyla geliştirilmiştir.

## 📋 Proje Özeti
Algoritma, tüm veri setini taramak yerine rastgele seçilen örneklemler ($k$) üzerinden olasılıksal bir sayım yapar. Elde edilen sonuçlar, istatistiksel güvenilirlik açısından **Hoeffding** ve **Chebyshev** eşitsizlikleri ile kıyaslanır.

### Algoritma Parametreleri
* **Öğrenci No:** 1240505066
* **Veri Hacmi ($n$):** $1.000.000$ eleman
* **Koşul:** `x % 7 == 3`
* **Deney Sayısı:** Her $k$ değeri için 100 tekrar
* **Hata Toleransı ($\epsilon$):** $0.01$

## 🚀 Özellikler
* **Deterministik Sayım:** Veri kümesindeki gerçek (ground truth) değeri hesaplar.
* **Monte Carlo Tahmini:** Farklı örneklem boyutları ($k = 100$ ile $100.000$ arası) için tahmin yürütür.
* **Hata Analizi:** Deneysel hata oranlarını teorik üst sınırlar olan Hoeffding ve Chebyshev değerleri ile karşılaştırır.
* **Zaman Analizi:** Rastgele örnekleme sürecinin işlem süresi üzerindeki etkisini ve standart sapmasını (CV) ölçer.

## 🛠 Kullanılan Teknolojiler
Kod, herhangi bir dış kütüphaneye ihtiyaç duymadan standart Python 3 kütüphaneleriyle yazılmıştır:
* `random`: Rastgele örneklem seçimi için.
* `time`: Performans ve süre ölçümü için.
* `math`: Teorik hata sınırlarının hesaplanması için.
* `statistics`: Ortalama ve standart sapma hesaplamaları için.

## 💻 Çalıştırma
Projeyi yerel makinenizde çalıştırmak için:

```bash
python main.py
