/* Bizimkent FEST — sosyal medya post verisi
   Tekrarlanan etkinlikler (birden fazla gün yapılanlar) tek postta toplanır. */

export const FEST = {
  tarih: '24–27 EYLÜL 2026',
  yer: 'Bizimkent Meydanı · Beylikdüzü',
  ig: '@bizimkentfest',
  site: 'bizimkentfest.com'
};

export const GUNLER = {
  per: { kisa: 'Perşembe', tarih: '24 Eylül' },
  cum: { kisa: 'Cuma',     tarih: '25 Eylül' },
  cmt: { kisa: 'Cumartesi',tarih: '26 Eylül' },
  paz: { kisa: 'Pazar',    tarih: '27 Eylül' }
};

/* renk: red | orange | yellow | green | blue | purple | pink | navy */
export const POSTLAR = [
  /* ---------- TEKRARLANAN ETKİNLİKLER — TEK POST ---------- */
  {
    id: '01-bizim-pazar', tip: 'etkinlik', renk: 'orange', kat: 'ÇARŞI & PANAYIR',
    baslik: 'Bizim PAZAR\n& Panayır',
    serif: 'Dört gün boyunca meydan kurulu.',
    zamanlar: [{ gun: '24–27 Eylül', alt: 'Perşembe · Cuma · Cumartesi · Pazar', saat: '11:00 – 23:00' }],
    rozet: 'HER GÜN',
    not: 'El emeği tezgâhlar, lezzet durakları ve panayır oyunları.'
  },
  {
    id: '02-eglenceli-yarismalar', tip: 'etkinlik', renk: 'red', kat: 'YARIŞMA · ÖDÜLLÜ',
    baslik: 'Eğlenceli\nYarışmalar',
    serif: 'Yetişkinler için, ödüller sahnede.',
    zamanlar: [
      { gun: 'Perşembe',  alt: '24 Eylül', saat: '17:00 – 18:00' },
      { gun: 'Cuma',      alt: '25 Eylül', saat: '16:00 – 17:00' },
      { gun: 'Cumartesi', alt: '26 Eylül', saat: '19:00 – 20:30' }
    ],
    rozet: '3 GÜN',
    not: 'Katılım ücretsiz — kayıt sahne önünde.'
  },
  {
    id: '03-acik-hava-sinemasi', tip: 'etkinlik', renk: 'navy', kat: 'SİNEMA · SÖYLEŞİ',
    baslik: 'Açık Hava\nSineması',
    serif: 'Yıldızların altında film ve sohbet.',
    zamanlar: [
      { gun: 'Perşembe', alt: '24 Eylül', saat: '20:30 – 23:00' },
      { gun: 'Cuma',     alt: '25 Eylül', saat: '20:30 – 23:00' }
    ],
    rozet: '2 GECE',
    not: 'Basketbol sahasında · Söyleşi & film gösterimi'
  },
  {
    id: '04-saglik-sahnesi', tip: 'etkinlik', renk: 'green', kat: 'SAĞLIK SAHNESİ',
    baslik: 'Sağlık\nSahnesi',
    serif: 'Uzmanlardan mahalleye açık sohbet.',
    zamanlar: [
      { gun: 'Cuma',  alt: '25 Eylül', saat: '17:00 – 17:30' },
      { gun: 'Pazar', alt: '27 Eylül', saat: '17:00 – 18:00' }
    ],
    rozet: '2 GÜN',
    not: 'Soru sormak serbest, katılım ücretsiz.'
  },
  {
    id: '05-yetenekler-sahnesi', tip: 'etkinlik', renk: 'purple', kat: 'SAHNE',
    baslik: 'Yetenekler\nSahnesi',
    serif: 'Mahallenin yetenekleri sahneye çıkıyor.',
    zamanlar: [
      { gun: 'Cumartesi', alt: '26 Eylül', saat: '17:00 – 18:00' },
      { gun: 'Pazar',     alt: '27 Eylül', saat: '16:00 – 17:00' }
    ],
    rozet: '2 GÜN',
    not: 'Dans, müzik, gösteri — sahne herkesin.'
  },
  {
    id: '06-dj-performans', tip: 'etkinlik', renk: 'pink', kat: 'DJ PERFORMANS',
    baslik: 'DJ\nPerformans',
    serif: 'Meydanı dans pistine çeviriyoruz.',
    zamanlar: [
      { gun: 'Perşembe', alt: '24 Eylül', saat: '19:30 – 20:30' },
      { gun: 'Pazar',    alt: '27 Eylül', saat: '20:00 – 21:15' }
    ],
    rozet: '2 GÜN',
    not: 'Açılış ve kapanış gecelerinin ritmi.'
  },

  /* ---------- 24 EYLÜL PERŞEMBE ---------- */
  {
    id: '07-kortej-acilis', tip: 'etkinlik', renk: 'red', kat: 'AÇILIŞ',
    baslik: 'Kortej &\nResmî Açılış',
    serif: 'Festival ilk adımını mahalleyle atıyor.',
    zamanlar: [{ gun: 'Perşembe', alt: '24 Eylül', saat: '16:00 – 16:30' }],
    rozet: 'AÇILIŞ GÜNÜ',
    not: 'Kortejde buluşuyor, birlikte başlıyoruz.'
  },
  {
    id: '08-ritim-show', tip: 'etkinlik', renk: 'orange', kat: 'SAHNE',
    baslik: 'Ritim\nShow',
    serif: 'Açılışın nabzı davullarla atıyor.',
    zamanlar: [{ gun: 'Perşembe', alt: '24 Eylül', saat: '16:30 – 17:00' }],
    rozet: 'AÇILIŞ GÜNÜ',
    not: 'Kortejin hemen ardından ana sahnede.'
  },
  {
    id: '09-karaoke-sahnesi', tip: 'etkinlik', renk: 'blue', kat: 'SAHNE',
    baslik: 'Karaoke\nSahnesi',
    serif: 'Mikrofon sende, meydan seni dinliyor.',
    zamanlar: [{ gun: 'Perşembe', alt: '24 Eylül', saat: '18:00 – 19:30' }],
    rozet: 'YENİ',
    not: 'Şarkını seç, sahneye çık.'
  },

  /* ---------- 25 EYLÜL CUMA ---------- */
  {
    id: '10-thm', tip: 'etkinlik', renk: 'green', kat: 'TÜRK HALK MÜZİĞİ',
    baslik: 'THM\nKonseri',
    serif: 'Türkülerle dolu bir cuma akşamı.',
    zamanlar: [{ gun: 'Cuma', alt: '25 Eylül', saat: '17:30 – 18:15' }],
    rozet: 'CANLI MÜZİK',
    not: 'Ana sahnede, herkese açık.'
  },
  {
    id: '11-misafir-sanatcilar', tip: 'etkinlik', renk: 'purple', kat: 'MİSAFİR SANATÇILAR',
    baslik: 'Pelin Dalkılıç\n& İbrahim\nKadıoğlu',
    serif: 'Festivalin misafir sahnesi.',
    zamanlar: [{ gun: 'Cuma', alt: '25 Eylül', saat: '18:15 – 19:15' }],
    rozet: 'SAHNEDE',
    not: 'Ana sahne · Ücretsiz katılım'
  },
  {
    id: '12-siir-gecesi', tip: 'etkinlik', renk: 'navy', kat: 'EDEBİYAT',
    baslik: 'Şiir\nGecesi',
    serif: 'Dizelerle yavaşlayan bir akşam.',
    zamanlar: [{ gun: 'Cuma', alt: '25 Eylül', saat: '19:15 – 20:30' }],
    rozet: 'CUMA AKŞAMI',
    not: 'Dinlemek de okumak da serbest.'
  },

  /* ---------- 26 EYLÜL CUMARTESİ ---------- */
  {
    id: '13-zumba', tip: 'etkinlik', renk: 'pink', kat: 'SPOR & DANS',
    baslik: 'Zumba',
    serif: 'Cumartesiye hareketle başlıyoruz.',
    zamanlar: [{ gun: 'Cumartesi', alt: '26 Eylül', saat: '16:00 – 17:00' }],
    rozet: 'HERKESE AÇIK',
    not: 'Rahat kıyafet ve su şişeni getir.'
  },
  {
    id: '14-tsm-korosu', tip: 'etkinlik', renk: 'yellow', kat: 'TÜRK SANAT MÜZİĞİ',
    baslik: 'TSM\nDernek Korosu',
    serif: 'Mahallenin kendi korosu sahnede.',
    zamanlar: [{ gun: 'Cumartesi', alt: '26 Eylül', saat: '18:15 – 19:00' }],
    rozet: 'CANLI MÜZİK',
    not: 'Bizimkent Derneği korosu · Ana sahne'
  },
  {
    id: '15-bizim-star', tip: 'etkinlik', renk: 'red', kat: 'SES YARIŞMASI · ÖDÜLLÜ',
    baslik: 'Bizim STAR',
    serif: 'Mahallenin sesi bu gece seçiliyor.',
    zamanlar: [{ gun: 'Cumartesi', alt: '26 Eylül', saat: '20:30 – 23:00' }],
    rozet: 'ÖDÜLLÜ FİNAL',
    not: 'Ödüllü ses yarışması · Ana sahne'
  },

  /* ---------- 27 EYLÜL PAZAR ---------- */
  {
    id: '16-heybemizdeki-turkuler', tip: 'etkinlik', renk: 'orange', kat: 'CANLI MÜZİK',
    baslik: 'Heybemizdeki\nTürküler',
    serif: 'Yolculuğun sesi, memleketin türküsü.',
    zamanlar: [{ gun: 'Pazar', alt: '27 Eylül', saat: '18:00 – 18:45' }],
    rozet: 'KAPANIŞ GÜNÜ',
    not: 'Ana sahnede, hep birlikte.'
  },
  {
    id: '17-diapason', tip: 'etkinlik', renk: 'blue', kat: 'CANLI MÜZİK',
    baslik: 'Diapason\nGrubu',
    serif: 'Pazar akşamına çok sesli bir dokunuş.',
    zamanlar: [{ gun: 'Pazar', alt: '27 Eylül', saat: '19:00 – 19:45' }],
    rozet: 'KAPANIŞ GÜNÜ',
    not: 'Ana sahne · Ücretsiz katılım'
  },
  {
    id: '18-murat-balkan', tip: 'etkinlik', renk: 'purple', kat: 'KAPANIŞ KONSERİ',
    baslik: 'Murat Balkan\nKonseri',
    serif: 'Festivalin final gecesi.',
    zamanlar: [{ gun: 'Pazar', alt: '27 Eylül', saat: '21:30 – 22:30' }],
    rozet: 'FİNAL',
    not: 'Ana sahne · Ücretsiz katılım'
  },
  {
    id: '19-odul-toreni', tip: 'etkinlik', renk: 'yellow', kat: 'KAPANIŞ',
    baslik: 'Ödül Töreni\n& Kapanış',
    serif: 'Dört günü birlikte uğurluyoruz.',
    zamanlar: [{ gun: 'Pazar', alt: '27 Eylül', saat: '22:30 – 23:00' }],
    rozet: 'FİNAL',
    not: 'Yarışma ödülleri ve teşekkürler.'
  },

  /* ---------- GÜNLÜK PROGRAM POSTLARI ---------- */
  {
    id: '20-program-24-persembe', tip: 'gun', renk: 'red',
    gun: 'PERŞEMBE', tarih: '24 EYLÜL', sira: '1. GÜN',
    serif: 'Kortejle başlıyoruz.',
    program: [
      ['11:00 – 23:00', 'Bizim PAZAR ve Panayır'],
      ['16:00 – 16:30', 'Kortej ve Resmî Açılış Seremonisi'],
      ['16:30 – 17:00', 'Ritim Show'],
      ['17:00 – 18:00', 'Eğlenceli Yarışmalar (ödüllü)'],
      ['18:00 – 19:30', 'Karaoke Sahnesi'],
      ['19:30 – 20:30', 'DJ Performans'],
      ['20:30 – 23:00', 'Açık Hava Sineması · söyleşi & film']
    ]
  },
  {
    id: '21-program-25-cuma', tip: 'gun', renk: 'green',
    gun: 'CUMA', tarih: '25 EYLÜL', sira: '2. GÜN',
    serif: 'Türküler, şiirler, misafirler.',
    program: [
      ['11:00 – 23:00', 'Bizim PAZAR ve Panayır'],
      ['16:00 – 17:00', 'Eğlenceli Yarışmalar (ödüllü)'],
      ['17:00 – 17:30', 'Sağlık Sahnesi'],
      ['17:30 – 18:15', 'THM Konseri'],
      ['18:15 – 19:15', 'Pelin Dalkılıç & İbrahim Kadıoğlu'],
      ['19:15 – 20:30', 'Şiir Gecesi'],
      ['20:30 – 23:00', 'Açık Hava Sineması · söyleşi & film']
    ]
  },
  {
    id: '22-program-26-cumartesi', tip: 'gun', renk: 'blue',
    gun: 'CUMARTESİ', tarih: '26 EYLÜL', sira: '3. GÜN',
    serif: 'Bizim STAR gecesi.',
    program: [
      ['11:00 – 23:00', 'Bizim PAZAR ve Panayır'],
      ['16:00 – 17:00', 'Zumba'],
      ['17:00 – 18:00', 'Yetenekler Sahnesi'],
      ['18:15 – 19:00', 'TSM Dernek Korosu'],
      ['19:00 – 20:30', 'Eğlenceli Yarışmalar (ödüllü)'],
      ['20:30 – 23:00', 'Bizim STAR Ödüllü Ses Yarışması']
    ]
  },
  {
    id: '23-program-27-pazar', tip: 'gun', renk: 'purple',
    gun: 'PAZAR', tarih: '27 EYLÜL', sira: '4. GÜN · FİNAL',
    serif: 'Final günü, ödüller ve konser.',
    program: [
      ['11:00 – 23:00', 'Bizim PAZAR ve Panayır'],
      ['16:00 – 17:00', 'Yetenekler Sahnesi'],
      ['17:00 – 18:00', 'Sağlık Sahnesi'],
      ['18:00 – 18:45', 'Heybemizdeki Türküler'],
      ['19:00 – 19:45', 'Diapason Grubu'],
      ['20:00 – 21:15', 'DJ Performans'],
      ['21:30 – 22:30', 'Murat Balkan Konseri'],
      ['22:30 – 23:00', 'Ödül Töreni ve Kapanış']
    ]
  },

  /* ---------- GENEL DUYURU ---------- */
  {
    id: '00-duyuru', tip: 'duyuru', renk: 'blue',
    serif: 'Dört gün, tek bir meydan.',
    gunler: [
      ['24', 'PER', 'Kortej & Açılış'],
      ['25', 'CUM', 'Türküler & Şiir'],
      ['26', 'CMT', 'Bizim STAR'],
      ['27', 'PAZ', 'Final Konseri']
    ],
    not: 'Ücretsiz katılım — herkes davetli.'
  }
];
