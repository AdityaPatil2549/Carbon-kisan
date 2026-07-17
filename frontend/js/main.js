// ── CARBON KISAN — GLOBAL JAVASCRIPT ──

// Auto-detect API base: use relative path on Vercel, localhost for dev
window.API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:8000/api/v1'
  : '/api/v1';


window.fetchWithAuth = async function(endpoint, options = {}) {
  const token = localStorage.getItem('carbn-token');
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${window.API_BASE_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (response.status === 401) {
    // Handle unauthorized
    localStorage.removeItem('carbn-token');
    localStorage.removeItem('carbn-farmer-logged');
    localStorage.removeItem('carbn-buyer-logged');
    window.location.href = 'index.html';
  }

  return response;
};
// ── TRANSLATION SYSTEM ──
const translationDictionary = {
  en: {
    "nav_how": "How it works",
    "nav_about": "About",
    "nav_marketplace": "Marketplace",
    "nav_dashboard": "Dashboard",
    "nav_log": "Log practice",
    "nav_credits": "Credits",
    "nav_refer": "Refer",
    "hero_eyebrow": "India's first farmer-led carbon marketplace",
    "hero_title": "Carbon credits for<br><span>every farmer.</span>",
    "hero_sub": "Log sustainable farming practices. Our ML model estimates carbon sequestration. CSR buyers purchase verified micro-credits — creating direct income for rural India.",
    "btn_farmer": "🌾 I'm a farmer",
    "btn_buyer": "🏢 I'm a CSR buyer",
    "btn_login": "Log in",
    "est_title": "What can <span style=\"color:var(--leaf)\">you earn</span> this season?",
    "est_sub": "No login required. Enter your land details and see your potential carbon credit income.",
    "est_label_land": "Land area (acres) / भूमि (एकड़)",
    "est_label_crop": "Crop type / फसल का प्रकार",
    "est_label_practice": "Practice type / कृषि पद्धति",
    "est_btn": "🌾 Start earning — Log practice",
    "how_title": "How Carbon Kisan works",
    "how_sub": "Three steps from sustainable farming to real income.",
    "how_step1_title": "Log your practice",
    "how_step1_desc": "Farmers log sustainable practices like no-till farming, cover cropping, or reduced pesticide use via mobile — in their own language.",
    "how_step2_title": "ML estimates carbon",
    "how_step2_desc": "Our XGBoost model calculates CO₂ sequestration and issues a verified credit in tonnes to your wallet.",
    "how_step3_title": "Buyer purchases credit",
    "how_step3_desc": "CSR teams buy verified micro-credits. Payment is transferred via UPI within 24 hours with WhatsApp notification.",
    "trust_land": "7/12 document verified land ownership",
    "trust_ml": "ML-verified carbon sequestration",
    "trust_wa": "WhatsApp notifications in your language",
    "trust_cert": "Downloadable CSR impact certificates",
    "trust_upi": "UPI payment within 24 hours",
    "f_login_title": "Choose your language",
    "f_login_sub": "Select the language you're most comfortable with / अपनी भाषा चुनें",
    "f_label_phone": "Mobile number / मोबाइल नंबर",
    "f_phone_hint": "We'll send you an OTP on this number via SMS",
    "f_btn_otp": "Send OTP →",
    "f_otp_title": "Enter OTP",
    "f_otp_timer": "Expires in",
    "f_otp_resend": "Didn't receive? Resend OTP",
    "f_verify_btn": "Verify OTP",
    "f_back_btn": "← Change number",
    "f_upload_title": "Verify land ownership or Identity",
    "f_upload_sub": "Upload your land document or Government ID to verify ownership.",
    "f_btn_complete": "Complete setup →",
    "f_btn_skip": "Skip for now (add later)",
    "f_why_title": "Why do we need this?",
    "f_why_desc": "Verification ensures credits are issued only for real registered farms. This increases buyer trust.",
    "f_welcome": "Welcome back",
    "f_greeting": "Good morning · Nashik, MH",
    "f_btn_log": "+ Log new practice",
    "f_stat_earned": "Total earned",
    "f_stat_credits": "Credits issued",
    "f_stat_co2": "CO₂ sequestered",
    "f_wallet_title": "💳 Credit wallet",
    "f_live_title": "Live activity",
    "f_refer_title": "Refer a farmer — earn ₹50 per referral",
    "f_refer_sub": "Share your link via WhatsApp in your preferred language",
    "f_copy_btn": "📋 Copy link",
    "f_share_btn": "💬 Share via WhatsApp",
    "log_title": "Log sustainable practice",
    "log_sub": "Fill in your farming details — our model will estimate your carbon credit instantly.",
    "log_voice_btn": "Voice fill (बोलकर भरें)",
    "log_sec_land": "🌾 Land details / भूमि विवरण",
    "log_label_crop": "Crop type / फसल का प्रकार",
    "log_label_practice": "Practice type / कृषि पद्धति",
    "log_label_area": "Land area (acres) / भूमि (एकड़)",
    "log_label_season": "Season / सीज़न",
    "log_sec_photo": "📸 Field photo / खेत की फोटो (optional)",
    "log_photo_hint": "Drag land photo or tap to upload",
    "log_photo_sub": "Optional — strengthens credit verification",
    "log_sec_notes": "📝 Additional notes / अतिरिक्त जानकारी",
    "log_label_desc": "Practice description / विवरण (optional)",
    "log_label_water": "Water usage reduced?",
    "log_label_fertilizer": "Chemical fertilizer reduced?",
    "log_btn_issue": "🌱 Issue credit to wallet",
    "log_btn_draft": "Save as draft",
    "log_est_res": "Estimated result",
    "log_model_note": "Model: XGBoost · ICRISAT soil data · R² 0.81. Results are estimates. Final credit is verified.",
    "b_login_title": "Welcome back",
    "b_login_sub": "Login with your corporate email to access the CSR buyer dashboard.",
    "b_label_email": "Work email / Corporate email",
    "b_label_pass": "Password",
    "b_btn_login": "🏢 Login to CSR portal"
  },
  hi: {
    "nav_how": "यह कैसे काम करता है",
    "nav_about": "हमारे बारे में",
    "nav_marketplace": "मार्केटप्लेस",
    "nav_dashboard": "डैशबोर्ड",
    "nav_log": "पद्धति दर्ज करें",
    "nav_credits": "क्रेडिट",
    "nav_refer": "रेफ़र करें",
    "hero_eyebrow": "भारत का पहला किसान-संचालित कार्बन मार्केटप्लेस",
    "hero_title": "कार्बन क्रेडिट<br><span>हर किसान के लिए।</span>",
    "hero_sub": "टिकाऊ खेती के तरीकों को दर्ज करें। हमारा ML मॉडल कार्बन अवशोषण का अनुमान लगाता है। CSR खरीदार सत्यापित माइक्रो-क्रेडिट खरीदते हैं - ग्रामीण भारत के लिए प्रत्यक्ष आय का मार्ग।",
    "btn_farmer": "🌾 मैं एक किसान हूँ",
    "btn_buyer": "🏢 मैं एक CSR खरीदार हूँ",
    "btn_login": "लॉग इन करें",
    "est_title": "आप इस सीज़न में <span style=\"color:var(--leaf)\">कितना कमा सकते हैं</span>?",
    "est_sub": "लॉगिन की आवश्यकता नहीं है। अपनी भूमि का विवरण दर्ज करें और संभावित कार्बन क्रेडिट आय देखें।",
    "est_label_land": "भूमि क्षेत्र (एकड़)",
    "est_label_crop": "फसल का प्रकार",
    "est_label_practice": "कृषि पद्धति",
    "est_btn": "🌾 कमाई शुरू करें — पद्धति दर्ज करें",
    "how_title": "Carbon Kisan कैसे काम करता है",
    "how_sub": "टिकाऊ खेती से वास्तविक आय तक तीन सरल कदम।",
    "how_step1_title": "पद्धति दर्ज करें",
    "how_step1_desc": "किसान मोबाइल के माध्यम से अपनी भाषा में नो-टिल खेती, कवर क्रॉपिंग या कम कीटनाशक उपयोग जैसे टिकाऊ तरीकों को दर्ज करते हैं।",
    "how_step2_title": "ML कार्बन का अनुमान लगाता है",
    "how_step2_desc": "हमारा XGBoost मॉडल कार्बन अवशोषण की गणना करता है और आपके वॉलेट में टन (t) में क्रेडिट जारी करता है।",
    "how_step3_title": "खरीदार खरीदता है",
    "how_step3_desc": "CSR टीमें सत्यापित माइक्रो-क्रेडिट खरीदती हैं। 24 घंटे में UPI भुगतान आ जाता है और आपकी भाषा में WhatsApp संदेश प्राप्त होता है।",
    "trust_land": "7/12 दस्तावेज़ द्वारा सत्यापित भूमि स्वामित्व",
    "trust_ml": "ML द्वारा सत्यापित कार्बन अवशोषण",
    "trust_wa": "आपकी भाषा में WhatsApp सूचनाएं",
    "trust_cert": "डाउनलोड करने योग्य CSR प्रभाव प्रमाण पत्र",
    "trust_upi": "24 घंटे के भीतर UPI भुगतान",
    "f_login_title": "अपनी भाषा चुनें",
    "f_login_sub": "उस भाषा का चयन करें जिसमें आप सबसे सहज हैं / अपनी भाषा चुनें",
    "f_label_phone": "मोबाइल नंबर / मोबाइल नंबर",
    "f_phone_hint": "हम इस नंबर पर SMS के माध्यम से एक OTP भेजेंगे",
    "f_btn_otp": "OTP भेजें →",
    "f_otp_title": "OTP दर्ज करें",
    "f_otp_timer": "समाप्ति समय",
    "f_otp_resend": "प्राप्त नहीं हुआ? OTP पुनः भेजें",
    "f_verify_btn": "OTP सत्यापित करें",
    "f_back_btn": "← नंबर बदलें",
    "f_upload_title": "भूमि स्वामित्व या पहचान सत्यापित करें",
    "f_upload_sub": "सत्यापन के लिए अपना भूमि दस्तावेज़ या सरकारी ID अपलोड करें।",
    "f_btn_complete": "सेटअप पूरा करें →",
    "f_btn_skip": "अभी छोड़ें (बाद में जोड़ें)",
    "f_why_title": "हमें इसकी आवश्यकता क्यों है?",
    "f_why_desc": "सत्यापन सुनिश्चित करता है कि क्रेडिट केवल वास्तविक पंजीकृत खेतों के लिए जारी किए जाएं। इससे खरीदार का विश्वास बढ़ता है।",
    "f_welcome": "स्वागत हे",
    "f_greeting": "शुभ प्रभात · नासिक, MH",
    "f_btn_log": "+ नई पद्धति दर्ज करें",
    "f_stat_earned": "कुल कमाई",
    "f_stat_credits": "जारी किए गए क्रेडिट",
    "f_stat_co2": "कार्बन अवशोषित",
    "f_wallet_title": "💳 क्रेडिट वॉलेट",
    "f_live_title": "लाइव गतिविधि",
    "f_refer_title": "एक किसान को रेफ़र करें — प्रति रेफ़रल ₹50 कमाएं",
    "f_refer_sub": "अपनी भाषा में WhatsApp के माध्यम से अपना लिंक साझा करें",
    "f_copy_btn": "📋 लिंक कॉपी करें",
    "f_share_btn": "💬 WhatsApp पर साझा करें",
    "log_title": "टिकाऊ पद्धति दर्ज करें",
    "log_sub": "अपने खेती का विवरण भरें — हमारा मॉडल तुरंत आपके कार्बन क्रेडिट का अनुमान लगाएगा।",
    "log_voice_btn": "बोलकर भरें (Voice fill)",
    "log_sec_land": "🌾 भूमि विवरण",
    "log_label_crop": "फसल का प्रकार",
    "log_label_practice": "कृषि पद्धति",
    "log_label_area": "भूमि क्षेत्र (एकड़)",
    "log_label_season": "सीज़न",
    "log_sec_photo": "📸 खेत की फोटो",
    "log_photo_hint": "खेत की फोटो खींचें या अपलोड करें",
    "log_photo_sub": "वैकल्पिक — क्रेडिट सत्यापन को मजबूत करता है",
    "log_sec_notes": "📝 अतिरिक्त जानकारी",
    "log_label_desc": "पद्धति का विवरण (वैकल्पिक)",
    "log_label_water": "क्या पानी का उपयोग कम किया गया?",
    "log_label_fertilizer": "क्या रासायनिक उर्वरक कम किया गया?",
    "log_btn_issue": "🌱 वॉलेट में क्रेडिट जारी करें",
    "log_btn_draft": "ड्राफ्ट के रूप में सहेजें",
    "log_est_res": "अनुमानित परिणाम",
    "log_model_note": "मॉडल: XGBoost · ICRISAT मृदा डेटा · R² 0.81. परिणाम अनुमानित हैं। अंतिम क्रेडिट सत्यापित किया जाता है।",
    "b_login_title": "स्वागत हे",
    "b_login_sub": "CSR खरीदार डैशबोर्ड तक पहुँचने के लिए अपने कॉर्पोरेट ईमेल से लॉगिन करें।",
    "b_label_email": "काम का ईमेल / कॉर्पोरेट ईमेल",
    "b_label_pass": "पासवर्ड",
    "b_btn_login": "🏢 CSR पोर्टल में लॉगिन करें"
  },
  mr: {
    "nav_how": "हे कसे काम करते",
    "nav_about": "आमच्याबद्दल",
    "nav_marketplace": "मार्केटप्लेस",
    "nav_dashboard": "डॅशबोर्ड",
    "nav_log": "पद्धत नोंदवा",
    "nav_credits": "क्रेडिट",
    "nav_refer": "रेफर करा",
    "hero_eyebrow": "भारतातील पहिले शेतकरी-चालित कार्बन मार्केटप्लेस",
    "hero_title": "कार्बन क्रेडिट<br><span>प्रत्येक शेतकऱ्यासाठी.</span>",
    "hero_sub": "शाश्वत शेती पद्धतींची नोंद करा. आमचे ML मॉडेल कार्बन शोषणाचा अंदाज लावते. CSR खरेदीदार सत्यापित क्रेडिट खरेदी करतात - ग्रामीण भारतातील शेतकऱ्यांसाठी थेट उत्पन्न.",
    "btn_farmer": "🌾 मी शेतकरी आहे",
    "btn_buyer": "🏢 मी CSR खरेदीदार आहे",
    "btn_login": "लॉग इन करा",
    "est_title": "तुम्ही या हंगामात <span style=\"color:var(--leaf)\">किती कमवू शकता</span>?",
    "est_sub": "लॉगिनची आवश्यकता नाही. तुमच्या जमिनीची माहिती टाका आणि संभाव्य कार्बन क्रेडिट उत्पन्न पहा.",
    "est_label_land": "जमीन क्षेत्र (एकर)",
    "est_label_crop": "पिकाचा प्रकार",
    "est_label_practice": "कृषि पद्धत",
    "est_btn": "🌾 कमाई सुरू करा — पद्धत नोंदवा",
    "how_title": "Carbon Kisan कसे काम करते",
    "how_sub": "शाश्वत शेतीपासून ते प्रत्यक्ष उत्पन्नापर्यंत तीन सोप्या पायऱ्या.",
    "how_step1_title": "पद्धत नोंदवा",
    "how_step1_desc": "शेतकरी मोबाईलद्वारे त्यांच्या स्वतःच्या भाषेत नो-टिल शेती, कव्हर क्रॉपिंग किंवा कमी कीटकनाशकांचा वापर नोंदवतात.",
    "how_step2_title": "ML कार्बन मोजते",
    "how_step2_desc": "आमचे XGBoost मॉडेल कार्बन शोषणाची गणना करते आणि तुमच्या वॉलेटमध्ये टन (t) मध्ये क्रेडिट जारी करते.",
    "how_step3_title": "खरेदीदार खरेदी करतो",
    "how_step3_desc": "CSR कंपन्या सत्यापित क्रेडिट खरेदी करतात. 24 तासांच्या आत UPI द्वारे पैसे मिळतात आणि WhatsApp वर संदेश येतो.",
    "trust_land": "7/12 कागदपत्राद्वारे सत्यापित जमिनीची मालकी",
    "trust_ml": "ML द्वारे सत्यापित कार्बन शोषण",
    "trust_wa": "तुमच्या भाषेत WhatsApp सूचना",
    "trust_cert": "डाउनलोड करण्यायोग्य CSR प्रभाव प्रमाणपत्रे",
    "trust_upi": "24 तासांच्या आत UPI पेमेंट",
    "f_login_title": "तुमची भाषा निवडा",
    "f_login_sub": "तुम्हाला सोयीची वाटणारी भाषा निवडा / अपनी भाषा चुनें",
    "f_label_phone": "मोबाईल नंबर / मोबाइल नंबर",
    "f_phone_hint": "आम्ही या नंबरवर SMS द्वारे OTP पाठवू",
    "f_btn_otp": "OTP पाठवा →",
    "f_otp_title": "OTP प्रविष्ट करा",
    "f_otp_timer": "कालबाह्य होईल",
    "f_otp_resend": "प्राप्त झाला नाही? पुन्हा पाठवा",
    "f_verify_btn": "OTP सत्यापित करा",
    "f_back_btn": "← नंबर बदला",
    "f_upload_title": "जमिनीची मालकी किंवा ओळख सत्यापित करा",
    "f_upload_sub": "सत्यापनासाठी जमिनीचे कागदपत्र किंवा सरकारी ID अपलोड करा.",
    "f_btn_complete": "सेटअप पूर्ण करा →",
    "f_btn_skip": "आता वगळा (नंतर जोडा)",
    "f_why_title": "आम्हाला याची गरज का आहे?",
    "f_why_desc": "सत्यापन सुनिश्चित करते की क्रेडिट्स केवळ वास्तविक शेतांसाठी जारी केले जातील. यामुळे खरेदीदारांचा विश्वास वाढतो.",
    "f_welcome": "स्वागत आहे",
    "f_greeting": "शुभ प्रभात · नाशिक, MH",
    "f_btn_log": "+ नवीन पद्धत नोंदवा",
    "f_stat_earned": "एकूण कमाई",
    "f_stat_credits": "जारी केलेले क्रेडिट्स",
    "f_stat_co2": "कार्बन शोषला",
    "f_wallet_title": "💳 क्रेडिट वॉलेट",
    "f_live_title": "लाइव्ह क्रियाकलाप",
    "f_refer_title": "शेतकऱ्याला रेफर करा — प्रति रेफरल ₹५० कमवा",
    "f_refer_sub": "तुमच्या भाषेत WhatsApp द्वारे तुमची लिंक शेअर करा",
    "f_copy_btn": "📋 लिंक कॉपी करा",
    "f_share_btn": "💬 WhatsApp वर शेअर करा",
    "log_title": "शाश्वत पद्धत नोंदवा",
    "log_sub": "तुमच्या शेतीची माहिती भरा — आमचे मॉडेल त्वरित तुमच्या कार्बन क्रेडिटचा अंदाज लावेल.",
    "log_voice_btn": "बोलून भरा (Voice fill)",
    "log_sec_land": "🌾 जमिनीची माहिती",
    "log_label_crop": "पिकाचा प्रकार",
    "log_label_practice": "कृषि पद्धत",
    "log_label_area": "जमीन क्षेत्र (एकर)",
    "log_label_season": "हंगाम",
    "log_sec_photo": "📸 शेताचा फोटो",
    "log_photo_hint": "शेताचा फोटो काढा किंवा अपलोड करा",
    "log_photo_sub": "पर्यायी — क्रेडिट सत्यापनास मदत होते",
    "log_sec_notes": "📝 अतिरिक्त माहिती",
    "log_label_desc": "पद्धतीचे वर्णन (पर्यायी)",
    "log_label_water": "पाण्याचा वापर कमी केला का?",
    "log_label_fertilizer": "रासायनिक खतांचा वापर कमी केला का?",
    "log_btn_issue": "🌱 वॉलेटमध्ये क्रेडिट जारी करा",
    "log_btn_draft": "ड्राफ्ट म्हणून साठवा",
    "log_est_res": "अंदाजित निकाल",
    "log_model_note": "मॉडेल: XGBoost · ICRISAT जमीन डेटा · R² 0.81. निकाल अंदाजित आहेत. अंतिम क्रेडिट सत्यापित केले जाईल.",
    "b_login_title": "स्वागत आहे",
    "b_login_sub": "CSR खरेदीदार डॅशबोर्डमध्ये प्रवेश करण्यासाठी तुमच्या कॉर्पोरेट ईमेलसह लॉगिन करा.",
    "b_label_email": "कामाचा ईमेल / कॉर्पोरेट ईमेल",
    "b_label_pass": "पासवर्ड",
    "b_btn_login": "🏢 CSR पोर्टलवर लॉगिन करा"
  }
};

function translatePage(lang) {
  if (!translationDictionary[lang]) lang = 'en';
  
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (translationDictionary[lang][key]) {
      el.innerHTML = translationDictionary[lang][key];
    }
  });

  // Also translate inputs with placeholders that have translations
  document.querySelectorAll('input[placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (key && translationDictionary[lang][key]) {
      el.setAttribute('placeholder', translationDictionary[lang][key]);
    }
  });
  
  localStorage.setItem('carbn-lang', lang);
}

// ── NAVBAR SCROLL BEHAVIOR ──
const navbar = document.getElementById('main-nav');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
}

// ── HAMBURGER MENU ──
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobile-menu');

if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open');
  });
}

function closeMobileMenu() {
  if (hamburger) hamburger.classList.remove('open');
  if (mobileMenu) mobileMenu.classList.remove('open');
}

// ── LANGUAGE SWITCHER CLICKS ──
function initLangSwitchers() {
  // Build interactive dropdown for .lang-switcher (navbar)
  document.querySelectorAll('.lang-switcher').forEach(switcher => {
    const btn = switcher.querySelector('.lang-tag');
    if (!btn) return;

    // If no dropdown already exists, inject one
    if (!switcher.querySelector('.lang-dropdown')) {
      const savedLang = localStorage.getItem('carbn-lang') || 'en';
      const langLabel = savedLang === 'hi' ? 'HI' : savedLang === 'mr' ? 'MR' : 'EN';
      btn.textContent = langLabel + ' \u25be';

      const dropdown = document.createElement('div');
      dropdown.className = 'lang-dropdown';
      dropdown.style.cssText = 'position:absolute;top:calc(100% + 6px);right:0;background:var(--surface-2);border:0.5px solid var(--border-strong);border-radius:var(--radius);padding:6px;min-width:120px;box-shadow:0 8px 24px rgba(0,0,0,0.3);display:none;z-index:200;';
      dropdown.innerHTML = `
        <button class="lang-dropdown-item" data-lang="en" style="display:flex;align-items:center;gap:8px;width:100%;padding:8px 10px;background:none;border:none;border-radius:var(--radius-sm);color:var(--text-primary);font-family:inherit;font-size:13px;cursor:pointer;text-align:left;" onmouseover="this.style.background='var(--surface-3)'" onmouseout="this.style.background='none'">🇬🇧 English</button>
        <button class="lang-dropdown-item" data-lang="hi" style="display:flex;align-items:center;gap:8px;width:100%;padding:8px 10px;background:none;border:none;border-radius:var(--radius-sm);color:var(--text-primary);font-family:inherit;font-size:13px;cursor:pointer;text-align:left;" onmouseover="this.style.background='var(--surface-3)'" onmouseout="this.style.background='none'">हिंदी</button>
        <button class="lang-dropdown-item" data-lang="mr" style="display:flex;align-items:center;gap:8px;width:100%;padding:8px 10px;background:none;border:none;border-radius:var(--radius-sm);color:var(--text-primary);font-family:inherit;font-size:13px;cursor:pointer;text-align:left;" onmouseover="this.style.background='var(--surface-3)'" onmouseout="this.style.background='none'">मराठी</button>
      `;
      switcher.style.position = 'relative';
      switcher.appendChild(dropdown);

      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = dropdown.style.display === 'block';
        document.querySelectorAll('.lang-dropdown').forEach(d => d.style.display = 'none');
        dropdown.style.display = isOpen ? 'none' : 'block';
      });

      dropdown.querySelectorAll('.lang-dropdown-item').forEach(item => {
        item.addEventListener('click', () => {
          const lang = item.getAttribute('data-lang');
          const label = lang === 'hi' ? 'HI' : lang === 'mr' ? 'MR' : 'EN';
          btn.textContent = label + ' \u25be';
          dropdown.style.display = 'none';
          translatePage(lang);
          // Sync mobile lang switcher
          document.querySelectorAll('.mobile-lang-switcher .lang-tag').forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-lang') === lang);
          });
          // Sync lang-section (login page)
          document.querySelectorAll('.lang-section .lang-tag').forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-lang') === lang);
          });
        });
      });
    }
  });

  // Mobile and login section lang tags
  document.querySelectorAll('.mobile-lang-switcher .lang-tag, .lang-section .lang-tag, .footer-bottom-langs .footer-lang').forEach(btn => {
    btn.addEventListener('click', function () {
      const parent = this.parentElement;
      parent.querySelectorAll('.lang-tag, .footer-lang').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const lang = this.getAttribute('data-lang') || this.textContent.trim().slice(0, 2).toLowerCase();
      translatePage(lang);
      
      // Update navbar lang button label if it exists
      document.querySelectorAll('.lang-switcher .lang-tag').forEach(b => {
        const label = lang === 'hi' ? 'HI' : lang === 'mr' ? 'MR' : 'EN';
        b.textContent = label + ' \u25be';
      });
    });
  });
}

// Close lang dropdown when clicking outside
window.addEventListener('click', () => {
  document.querySelectorAll('.lang-dropdown').forEach(d => d.style.display = 'none');
});

// Load saved language on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const savedLang = localStorage.getItem('carbn-lang') || 'en';
  
  // Init dynamic session/profile links first (rebuilds nav)
  initUserSessionUI();
  
  // Then init lang switchers (attaches dropdown to navbar)
  initLangSwitchers();
  translatePage(savedLang);
  
  // Set active class on corresponding switcher tags
  document.querySelectorAll('.mobile-lang-switcher .lang-tag, .lang-section .lang-tag').forEach(b => {
    const bLang = b.getAttribute('data-lang') || 'en';
    if (bLang === savedLang) b.classList.add('active');
    else b.classList.remove('active');
  });
});

// ── TOAST SYSTEM ──
let toastContainer = null;

function getToastContainer() {
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }
  return toastContainer;
}

function showToast(type, title, message, duration = 4000) {
  const container = getToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const icons = { success: '✓', info: '🔔', warn: '⚡', error: '✕' };

  toast.innerHTML = `
    <div class="toast-icon">${icons[type] || '!'}</div>
    <div>
      <div class="toast-title">${title}</div>
      ${message ? `<div class="toast-msg">${message}</div>` : ''}
    </div>
  `;

  container.appendChild(toast);

  if (duration > 0) {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  return toast;
}

// ── INTERSECTION OBSERVER FOR ANIMATIONS ──
const animObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('anim-in');
      animObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('[data-anim]').forEach(el => {
  el.classList.add('anim-ready');
  animObserver.observe(el);
});

// ── OTP INPUT HANDLING ──
function initOTPInputs(containerSelector) {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  const inputs = container.querySelectorAll('input[data-otp]');

  inputs.forEach((input, idx) => {
    input.addEventListener('input', (e) => {
      const val = e.target.value.replace(/\D/g, '').slice(-1);
      e.target.value = val;

      if (val && idx < inputs.length - 1) {
        inputs[idx + 1].focus();
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !input.value && idx > 0) {
        inputs[idx - 1].focus();
      }
    });

    input.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasted = e.clipboardData.getData('text').replace(/\D/g, '');
      inputs.forEach((inp, i) => {
        inp.value = pasted[i] || '';
      });
      const lastFilled = Math.min(pasted.length, inputs.length - 1);
      inputs[lastFilled].focus();
    });
  });
}

// ── ACTIVE NAV HIGHLIGHTING ──
function setActiveNavLink(path) {
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && path.includes(href.replace('.html', ''))) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

setActiveNavLink(window.location.pathname);

// ── UPLOAD ZONE DRAG HANDLING ──
document.querySelectorAll('.upload-zone').forEach(zone => {
  zone.addEventListener('dragover', e => {
    e.preventDefault();
    zone.classList.add('dragging');
  });

  zone.addEventListener('dragleave', () => zone.classList.remove('dragging'));

  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('dragging');
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(zone, file);
  });

  const fileInput = zone.querySelector('input[type=file]');
  if (fileInput) {
    zone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
      if (e.target.files[0]) handleFileUpload(zone, e.target.files[0]);
    });
  }
});

function handleFileUpload(zone, file) {
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
  const maxSize = 5 * 1024 * 1024; // 5MB

  if (!allowedTypes.includes(file.type)) {
    showToast('error', 'Invalid file type', 'Please upload PDF, JPG, or PNG files only.');
    return;
  }

  if (file.size > maxSize) {
    showToast('error', 'File too large', 'Maximum file size is 5MB.');
    return;
  }

  // Show success state
  zone.innerHTML = `
    <div style="font-size:28px;margin-bottom:8px">✅</div>
    <div style="font-size:14px;color:var(--leaf);font-weight:500">${file.name}</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px">${(file.size / 1024).toFixed(0)} KB · Uploaded ✓</div>
  `;

  showToast('success', 'Document uploaded', `${file.name} uploaded successfully.`);
}

// ── COPY TO CLIPBOARD ──
function copyToClipboard(text, successMsg = 'Copied!') {
  navigator.clipboard.writeText(text).then(() => {
    showToast('success', successMsg, '');
  }).catch(() => {
    showToast('error', 'Copy failed', 'Please copy manually.');
  });
}

// ── USER PROFILE AND LOGOUT SYSTEM ──
function initUserSessionUI() {
  const isFarmerLoggedIn = localStorage.getItem('carbn-farmer-logged') === 'true';
  const isBuyerLoggedIn = localStorage.getItem('carbn-buyer-logged') === 'true';

  // Inject Profile + Logout buttons dynamically in the header/navbar if elements exist
  const navActions = document.querySelector('.nav-actions');
  if (navActions) {
    if (isFarmerLoggedIn) {
      const farmerName = localStorage.getItem('carbn-farmer-name') || 'Rajan Patil';
      const savedLang = localStorage.getItem('carbn-lang') || 'en';
      const langLabel = savedLang === 'hi' ? 'HI' : savedLang === 'mr' ? 'MR' : 'EN';
      navActions.innerHTML = `
        <div class="lang-switcher" id="nav-lang-switcher">
          <button class="lang-tag active" data-lang="en">${langLabel} ▾</button>
        </div>
        <div class="profile-dropdown-wrapper">
          <button class="badge badge-sold profile-btn" onclick="toggleProfileDropdown()">🌾 ${farmerName} ▾</button>
          <div class="profile-dropdown-menu" id="profile-dropdown">
            <a href="#" onclick="openProfileModal('farmer'); return false;">👤 Edit Profile</a>
            <a href="farmer-dashboard.html">📊 Dashboard</a>
            <a href="#" onclick="logoutUser('farmer'); return false;" style="color:var(--red);">🚪 Logout</a>
          </div>
        </div>
      `;
    } else if (isBuyerLoggedIn) {
      const buyerName = localStorage.getItem('carbn-buyer-name') || 'Tata Motors CSR';
      navActions.innerHTML = `
        <div class="profile-dropdown-wrapper">
          <button class="badge badge-sold profile-btn" onclick="toggleProfileDropdown()">🏢 ${buyerName} ▾</button>
          <div class="profile-dropdown-menu" id="profile-dropdown">
            <a href="#" onclick="openProfileModal('buyer'); return false;">👤 Edit Profile</a>
            <a href="buyer-dashboard.html">📊 Dashboard</a>
            <a href="#" onclick="logoutUser('buyer'); return false;" style="color:var(--red);">🚪 Logout</a>
          </div>
        </div>
      `;
    }
  }

  // Handle mobile menu dynamically too
  const mobileMenuInner = document.querySelector('.mobile-menu-inner');
  if (mobileMenuInner) {
    const ctas = mobileMenuInner.querySelector('.mobile-menu-ctas');
    if (ctas) {
      if (isFarmerLoggedIn) {
        ctas.innerHTML = `
          <button class="btn btn-secondary" onclick="openProfileModal('farmer')" style="flex:1">👤 Profile</button>
          <button class="btn btn-danger" onclick="logoutUser('farmer')" style="flex:1">🚪 Logout</button>
        `;
      } else if (isBuyerLoggedIn) {
        ctas.innerHTML = `
          <button class="btn btn-secondary" onclick="openProfileModal('buyer')" style="flex:1">👤 Profile</button>
          <button class="btn btn-danger" onclick="logoutUser('buyer')" style="flex:1">🚪 Logout</button>
        `;
      }
    }
  }
}

function toggleProfileDropdown() {
  const menu = document.getElementById('profile-dropdown');
  if (menu) {
    menu.classList.toggle('open');
  }
}

// Close profile dropdown when clicking outside
window.addEventListener('click', (e) => {
  if (!e.target.matches('.profile-btn')) {
    const menus = document.querySelectorAll('.profile-dropdown-menu');
    menus.forEach(m => m.classList.remove('open'));
  }
});

function openProfileModal(type) {
  // Check if modal already exists
  let modalOverlay = document.getElementById('global-profile-modal');
  if (modalOverlay) modalOverlay.remove();

  modalOverlay = document.createElement('div');
  modalOverlay.id = 'global-profile-modal';
  modalOverlay.className = 'profile-modal-overlay';

  if (type === 'farmer') {
    const name = localStorage.getItem('carbn-farmer-name') || 'Rajan Patil';
    const phone = localStorage.getItem('carbn-farmer-phone') || '98765 43210';
    const state = localStorage.getItem('carbn-farmer-state') || 'MH';
    const landSize = localStorage.getItem('carbn-farmer-land') || '5';

    modalOverlay.innerHTML = `
      <div class="profile-modal">
        <div class="modal-title">👤 Edit Farmer Profile</div>
        <div class="modal-sub">Update your personal and farm details below</div>
        <div class="form-group">
          <label class="form-label">Full Name</label>
          <input class="input" type="text" id="prof-name" value="${name}">
        </div>
        <div class="form-group">
          <label class="form-label">Mobile Number</label>
          <input class="input" type="text" id="prof-phone" value="${phone}">
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">State</label>
            <select class="input" id="prof-state" style="appearance:none">
              <option value="MH" ${state === 'MH' ? 'selected' : ''}>Maharashtra</option>
              <option value="PB" ${state === 'PB' ? 'selected' : ''}>Punjab</option>
              <option value="MP" ${state === 'MP' ? 'selected' : ''}>Madhya Pradesh</option>
              <option value="TG" ${state === 'TG' ? 'selected' : ''}>Telangana</option>
              <option value="HR" ${state === 'HR' ? 'selected' : ''}>Haryana</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Farm Size (acres)</label>
            <input class="input" type="number" id="prof-land" value="${landSize}">
          </div>
        </div>
        <div class="flex gap-12" style="margin-top:20px">
          <button class="btn btn-secondary" style="flex:1" onclick="closeProfileModal()">Cancel</button>
          <button class="btn btn-primary" style="flex:1" onclick="saveFarmerProfile()">Save Changes</button>
        </div>
      </div>
    `;
  } else {
    const name = localStorage.getItem('carbn-buyer-name') || 'Tata Motors CSR';
    const email = localStorage.getItem('carbn-buyer-email') || 'priya@tatamotors.com';
    const company = localStorage.getItem('carbn-buyer-company') || 'Tata Motors';

    modalOverlay.innerHTML = `
      <div class="profile-modal">
        <div class="modal-title">👤 Edit CSR Profile</div>
        <div class="modal-sub">Update your corporate details below</div>
        <div class="form-group">
          <label class="form-label">Authorized Name</label>
          <input class="input" type="text" id="prof-name" value="${name}">
        </div>
        <div class="form-group">
          <label class="form-label">Work Email</label>
          <input class="input" type="email" id="prof-email" value="${email}">
        </div>
        <div class="form-group">
          <label class="form-label">Company Name</label>
          <input class="input" type="text" id="prof-company" value="${company}" disabled>
        </div>
        <div class="flex gap-12" style="margin-top:20px">
          <button class="btn btn-secondary" style="flex:1" onclick="closeProfileModal()">Cancel</button>
          <button class="btn btn-sky" style="flex:1" onclick="saveBuyerProfile()">Save Changes</button>
        </div>
      </div>
    `;
  }

  document.body.appendChild(modalOverlay);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeProfileModal();
  });
}

function closeProfileModal() {
  const modal = document.getElementById('global-profile-modal');
  if (modal) modal.remove();
}

function saveFarmerProfile() {
  const name = document.getElementById('prof-name').value.trim();
  const phone = document.getElementById('prof-phone').value.trim();
  const state = document.getElementById('prof-state').value;
  const land = document.getElementById('prof-land').value;

  if (!name || !phone) {
    showToast('error', 'Error', 'Name and Phone fields are required.');
    return;
  }

  localStorage.setItem('carbn-farmer-name', name);
  localStorage.setItem('carbn-farmer-phone', phone);
  localStorage.setItem('carbn-farmer-state', state);
  localStorage.setItem('carbn-farmer-land', land);

  showToast('success', 'Profile updated', 'Your farmer details were updated successfully.');
  closeProfileModal();
  initUserSessionUI();

  // Reload page to reflect name changes if on dashboard
  setTimeout(() => window.location.reload(), 800);
}

function saveBuyerProfile() {
  const name = document.getElementById('prof-name').value.trim();
  const email = document.getElementById('prof-email').value.trim();

  if (!name || !email) {
    showToast('error', 'Error', 'Name and Email fields are required.');
    return;
  }

  localStorage.setItem('carbn-buyer-name', name);
  localStorage.setItem('carbn-buyer-email', email);

  showToast('success', 'Profile updated', 'Your corporate details were updated successfully.');
  closeProfileModal();
  initUserSessionUI();

  setTimeout(() => window.location.reload(), 800);
}

function logoutUser(type) {
  localStorage.removeItem('carbn-token');
  if (type === 'farmer') {
    localStorage.removeItem('carbn-farmer-logged');
    localStorage.removeItem('carbn-farmer-name');
  } else {
    localStorage.removeItem('carbn-buyer-logged');
    localStorage.removeItem('carbn-buyer-name');
  }
  showToast('info', 'Logged out', 'You have successfully logged out.');
  setTimeout(() => {
    window.location.href = 'index.html';
  }, 1200);
}

window.openProfileModal = openProfileModal;
window.closeProfileModal = closeProfileModal;
window.saveFarmerProfile = saveFarmerProfile;
window.saveBuyerProfile = saveBuyerProfile;
window.logoutUser = logoutUser;
window.toggleProfileDropdown = toggleProfileDropdown;

// Expose globally
window.showToast = showToast;
window.copyToClipboard = copyToClipboard;
window.initOTPInputs = initOTPInputs;
window.closeMobileMenu = closeMobileMenu;
