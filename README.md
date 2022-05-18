# Neo4j-Project
 Neo4j graf veritabanı ile web uygulaması
 
### ● Yönetici arayüzü
 Admin,kullanıcı adı ve şifresini kullanarak giriş yapabilir.\
 Admin tarafından araştırmacı eklenebilir.(ArastirmaciAdi,ArastirmaciSoyadi)\
 Admin tarafından herhangi bir araştırmacıya yayın eklenebilir. (YayinAdi, YayinYili, YayinYeri,YayinTuru)
 
  
### ● Kullanıcı Arayüzü
 Kullanıcılar bu sayfadan araştırmacı içerik araması yapabilirler.\
 Arama yapıldığında ekrana yayın arama sonuçları, araştırmacıların çalıştığı kişiler, yayın bilgileri, yıllara göre yayın bilgisi gösterilir.\
 Araştırmacının çalıştığı kişilerin üzerine tıklandığında tıklanılan araştırmacı içinde aynı bilgiler gösterilir.\
 Ayrıca farklı bir sekmede araştırmacıya ait yayınlar, birlikte yayın yaptığı diğer araştırmacılar, yayın türleri, yayın yerleri ve yıl bilgisi Neo4j çizge yapısı kullanılarak görselleştirilmiştir.
  
<img
  src="/images/1.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto;  width: 300px"> \
  <img
  src="/images/2.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto;  width: 300px"> \
   Giriş yaptıktan sonra Araştırmacı ekle sayfasından istediğimiz araştırmacıları adı ve soyadıyla ekliyoruz.\
  <img
  src="/images/3.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; width: 300px"> \
  
  Yayın ekle kısmına girdiğimizde ise istediğimiz araştırmacıyı seçerek yayın adı, yayın türü, yayın yeri, yayın yılı bilgilerini giriyoruz ve veritabanına kaydediyoruz.\

  <img
  src="/images/4.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; width: 300px">\
  <img
  src="/images/5.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; width: 300px">\
  
   Kullanıcı giriş kısmında girdiğimizde ise karşımıza direk tüm yayınlar listesi geliyor. Burda arama kısmında istediğimiz araştırmacı adını, yayın adını, yayın yerini ve yılını aratıp listelettirebiliriz. Ayrıca farklı bir butonda girdiğimiz ve ilişkilendirdiğimiz tüm verilerin grafiği bulunmakta.Yeni sekmede ise tıkladığımız 
araştırmacının çalıştığı kişiler,yazdığı yayınlar ve gerekli bilgiler neovis.js kullanarak görselleştirdiğimiz veritabanımızın grafiği geliyor.

  <img
  src="/images/6.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto;  width: 300px">\
  <img
  src="/images/7.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; width: 300px">
