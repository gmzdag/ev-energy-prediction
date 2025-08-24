# 🚗 Elektrikli Araçlarda Enerji Tüketimi ve Menzil Tahmini

## 0. Projenin Amacı
Bu projenin amacı, **gerçek araç verileri** kullanılarak elektrikli araçlarda **enerji tüketimi** ve **menzil tahmini** yapabilmektir. Çalışmada batarya **State of Charge (SoC)** değişimi üzerinden hem anlık enerji tüketimi hem de kalan menzil öngörülmüş, farklı makine öğrenmesi modelleri karşılaştırmalı olarak değerlendirilmiştir.  

---
## 1. Veri Seti
Bu çalışmada, **Eskişehir Osmangazi Üniversitesi’nde yürütülen OPEVA projesi** kapsamında oluşturulmuş ve *Elsevier Data in Brief* dergisinde yayımlanan veri seti kullanılmıştır:

> Polat, A., Dağ, G., Pehlivan, N., Sarıçek, İ., Okyay, S., Yazıcı, A. (2025).  
> *A dataset for state of charge and range estimation of an L5 type electric vehicle that is used for Urban Logistic.*  
> DOI: [10.1016/j.dib.2025.111933](https://doi.org/10.1016/j.dib.2025.111933)

- **Araç:** L5 sınıfı elektrikli araç  
- **Testler:** 35 ayrı sürüş, her biri ~2 km sabit parkur  
- **Koşullar:** hız (15/25/35 km/s), yük (var/yok), yön (gidiş/dönüş), mevsim (yaz/kış)  
- **Birleştirme:** 35 sürüş birleştirilerek `ev_dataset.csv` adlı bütünleşik veri seti oluşturulmuştur  

---

## 2. Target (Hedef) Değişkenleri 🎯
Batarya SoC düşüşünü modellemek için farklı pencerelerde hedef değişkenler üretilmiştir:

- `soc_net_per_s` → SoC’nin saniyelik net değişim oranı  
- `soc_net_per_s_smooth5` → 5 saniyelik pencerede yumuşatılmış SoC değişimi  
- `soc_net_per_s_smooth10` → 10 saniyelik pencerede yumuşatılmış SoC değişimi  
- `soc_net_per_s_30s` → 30 saniyelik pencerede hesaplanan SoC değişimi  
- `soc_net_per_s_60s` → 60 saniyelik pencerede hesaplanan SoC değişimi  

Bu hedefler, hem **anlık enerji tüketimi** hem de **menzil tahmini** için kullanılmıştır.  

---

## 3. Kullanılan Metrikler 📏
Modellerin performansı üç ölçüt üzerinden değerlendirilmiştir:  

- **R² (Determinasyon Katsayısı):** Açıklanabilen varyans oranı  
- **MAE (Mean Absolute Error):** Ortalama mutlak hata  
- **RMSE (Root Mean Squared Error):** Kök ortalama kare hata  

---

## 4. Kullanılan Modeller 🤖
Çalışmada üç farklı makine öğrenmesi yaklaşımı uygulanmıştır:  

- **Random Forest (RF):** Dengeli performans, yüksek yorumlanabilirlik; gürültülü verilerde sınırlı olabilir.  
- **XGBoost (XGB):** Boosting yöntemi ile en düşük hata değerlerini vermiştir; parametre ayarlarına duyarlıdır.  
- **Yapay Sinir Ağı (NN):** Karmaşık ilişkileri öğrenebilme kapasitesine sahiptir; ancak sınırlı veri nedeniyle diğer modellere göre daha düşük performans göstermiştir.  

---

## 5. Sonuçlar 📊
Elde edilen performans değerleri aşağıdaki tabloda özetlenmiştir:  

| Model           | R² (Test) | MAE      | RMSE     | Açıklama |
|-----------------|-----------|----------|----------|----------|
| Random Forest   | ≈ 0.89    | 0.0011   | 0.0015   | Dengeli, hızlı eğitim; gürültüye duyarlı |
| XGBoost         | 0.89–0.92 | 0.00057  | 0.0012   | En yüksek doğruluk, en düşük hata |
| Neural Network  | 0.87–0.90 | 0.00065  | 0.0014   | Veri arttıkça gelişebilir |

---

## 6. Menzil Tahmini ve Faktör Analizi 🔍

### Menzil Tahmini
Menzil tahminleri, bataryanın başlangıç ve bitiş SoC değerlerinden hareketle hesaplanan **gerçek tüketim** ile modellerin tahmin ettiği tüketim karşılaştırılarak yapılmıştır. Özellikle **XGBoost modeli**, kalan menzili en düşük hata ile öngörmüştür.  

### Enerji Tüketimine Etki Eden Faktörler
Korelasyon analizine göre tüketimi en güçlü biçimde etkileyen değişkenler **DC_Link_Current** ve **power_W** olmuştur. Ayrıca tork, hız ve ivme tüketimi artırıcı yönde; voltaj tabanlı değişkenler ise (özellikle **DC_Link_Voltage**) ters yönde ilişki göstermiştir.  


## 7. Genel Sonuç ✅
- **XGBoost**, en düşük hata ve en yüksek doğruluk oranına ulaşmıştır.  
- Enerji tüketimi ile menzil arasında güçlü bir doğrusal ilişki saptanmıştır.  
- Kısa vadeli hedefler anlık tüketim değişimlerini en iyi şekilde yakalamıştır.  

---

## 8. Repo Yapısı 📂

```bash
data/                         
 ├── raw_data/                    # Ham veriler
 ├── ev_dataset.csv               # Birleştirilmiş veri seti
 ├── ev_dataset_multi_target.csv  # Çok hedefli versiyon
 └── ev_dataset_prepared.csv      # Ön işlenmiş veri

models/                          # Eğitim notebookları
 ├── RandomForest.ipynb
 ├── xgboost.ipynb
 └── nn.ipynb

notebooks/                        # Veri analizi
 └── ev_enerji_tuketimi_EDA.ipynb

src/                           
 └── merge_data.py

.gitignore
```
---
## 9. Katkıda Bulunanlar

- Gamze Dağ  
- Nisanur Pehlivan

## 10. Lisans

Bu proje **MIT Lisansı** ile sunulmaktadır.  
Ayrıntılar için [LICENSE](LICENSE) dosyasına bakınız.
