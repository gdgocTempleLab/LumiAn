export interface CountyData {
  code: string
  name: string
  districts: DistrictData[]
}

export interface DistrictData {
  code: string
  name: string
  zipCode: string
  villages: string[]
}

export const taiwanAddressData: CountyData[] = [
  {
    code: '100', name: '台北市',
    districts: [
      { code: '100', name: '中正區', zipCode: '100', villages: ['建國里', '南門里', '龍光里', '永昌里'] },
      { code: '103', name: '大同區', zipCode: '103', villages: ['延平里', '大有里', '玉泉里'] },
      { code: '104', name: '中山區', zipCode: '104', villages: ['正義里', '中山里', '朱馥里'] },
      { code: '105', name: '松山區', zipCode: '105', villages: ['莊敬里', '東光里', '精忠里'] },
      { code: '106', name: '大安區', zipCode: '106', villages: ['和平里', '光信里', '龍門里'] },
      { code: '108', name: '萬華區', zipCode: '108', villages: ['福星里', '萬壽里', '新安里'] },
      { code: '110', name: '信義區', zipCode: '110', villages: ['三張里', '五常里', '松隆里'] },
      { code: '111', name: '士林區', zipCode: '111', villages: ['福林里', '天母里', '蘭雅里'] },
      { code: '112', name: '北投區', zipCode: '112', villages: ['中心里', '溫泉里', '長安里'] },
      { code: '114', name: '內湖區', zipCode: '114', villages: ['湖濱里', '碧山里', '金龍里'] },
      { code: '115', name: '南港區', zipCode: '115', villages: ['三重里', '中研里', '南港里'] },
      { code: '116', name: '文山區', zipCode: '116', villages: ['景美里', '木柵里', '政大里'] },
    ],
  },
  {
    code: '200', name: '基隆市',
    districts: [
      { code: '200', name: '仁愛區', zipCode: '200', villages: ['文安里', '德厚里'] },
      { code: '201', name: '信義區', zipCode: '201', villages: ['義昭里', '孝德里'] },
      { code: '202', name: '中正區', zipCode: '202', villages: ['正義里', '和平里'] },
      { code: '203', name: '中山區', zipCode: '203', villages: ['通化里', '仁正里'] },
      { code: '204', name: '安樂區', zipCode: '204', villages: ['安和里', '定國里'] },
      { code: '205', name: '暖暖區', zipCode: '205', villages: ['暖暖里', '碇內里'] },
      { code: '206', name: '七堵區', zipCode: '206', villages: ['永安里', '實踐里'] },
    ],
  },
  {
    code: '300', name: '新竹市',
    districts: [
      { code: '300', name: '東區', zipCode: '300', villages: ['光復里', '建華里', '關新里'] },
      { code: '300', name: '北區', zipCode: '300', villages: ['中正里', '武陵里'] },
      { code: '300', name: '香山區', zipCode: '300', villages: ['頂埔里', '香山里'] },
    ],
  },
  {
    code: '400', name: '台中市',
    districts: [
      { code: '400', name: '中區', zipCode: '400', villages: ['大誠里', '繼光里'] },
      { code: '401', name: '東區', zipCode: '401', villages: ['東勢里', '東英里'] },
      { code: '402', name: '南區', zipCode: '402', villages: ['江川里', '和平里'] },
      { code: '403', name: '西區', zipCode: '403', villages: ['土庫里', '公正里'] },
      { code: '404', name: '北區', zipCode: '404', villages: ['建德里', '金華里'] },
      { code: '406', name: '北屯區', zipCode: '406', villages: ['舊社里', '平心里'] },
      { code: '407', name: '西屯區', zipCode: '407', villages: ['惠來里', '逢甲里'] },
      { code: '408', name: '南屯區', zipCode: '408', villages: ['文山里', '三厝里'] },
      { code: '411', name: '太平區', zipCode: '411', villages: ['太平里', '坪林里'] },
      { code: '412', name: '大里區', zipCode: '412', villages: ['大里里', '大元里'] },
      { code: '413', name: '霧峰區', zipCode: '413', villages: ['本堂里', '甲寅里'] },
      { code: '414', name: '烏日區', zipCode: '414', villages: ['烏日里', '三和里'] },
      { code: '420', name: '豐原區', zipCode: '420', villages: ['豐原里', '北湳里', '西湳里', '南嵩里', '翁子里', '圳寮里'] },
      { code: '421', name: '后里區', zipCode: '421', villages: ['墩南里', '墩北里'] },
      { code: '422', name: '石岡區', zipCode: '422', villages: ['石岡里', '金星里'] },
      { code: '423', name: '東勢區', zipCode: '423', villages: ['東安里', '北興里'] },
      { code: '424', name: '和平區', zipCode: '424', villages: ['南勢里', '天輪里'] },
      { code: '426', name: '新社區', zipCode: '426', villages: ['新社里', '復盛里'] },
      { code: '427', name: '潭子區', zipCode: '427', villages: ['潭秀里', '甘蔗里'] },
      { code: '428', name: '大雅區', zipCode: '428', villages: ['大雅里', '秀山里'] },
      { code: '429', name: '神岡區', zipCode: '429', villages: ['神岡里', '庄前里'] },
      { code: '432', name: '大肚區', zipCode: '432', villages: ['大肚里', '頂街里'] },
      { code: '433', name: '沙鹿區', zipCode: '433', villages: ['沙鹿里', '洛泉里'] },
      { code: '434', name: '龍井區', zipCode: '434', villages: ['龍井里', '忠和里'] },
      { code: '435', name: '梧棲區', zipCode: '435', villages: ['梧南里', '大庄里'] },
      { code: '436', name: '清水區', zipCode: '436', villages: ['清水里', '西寧里'] },
      { code: '437', name: '大甲區', zipCode: '437', villages: ['大甲里', '順天里'] },
      { code: '438', name: '外埔區', zipCode: '438', villages: ['外埔里', '大東里'] },
      { code: '439', name: '大安區', zipCode: '439', villages: ['大安里', '中庄里'] },
    ],
  },
  {
    code: '500', name: '彰化縣',
    districts: [
      { code: '500', name: '彰化市', zipCode: '500', villages: ['光復里', '中正里'] },
      { code: '505', name: '鹿港鎮', zipCode: '505', villages: ['鹿港里', '順興里'] },
      { code: '510', name: '員林市', zipCode: '510', villages: ['員林里', '三橋里'] },
    ],
  },
  {
    code: '600', name: '嘉義市',
    districts: [
      { code: '600', name: '東區', zipCode: '600', villages: ['東川里', '安寮里'] },
      { code: '600', name: '西區', zipCode: '600', villages: ['竹村里', '福全里'] },
    ],
  },
  {
    code: '700', name: '台南市',
    districts: [
      { code: '700', name: '中西區', zipCode: '700', villages: ['大涼里', '小西里'] },
      { code: '701', name: '東區', zipCode: '701', villages: ['東安里', '東光里'] },
      { code: '702', name: '南區', zipCode: '702', villages: ['文華里', '大林里'] },
      { code: '704', name: '北區', zipCode: '704', villages: ['北華里', '成功里'] },
      { code: '708', name: '安平區', zipCode: '708', villages: ['文平里', '平通里'] },
      { code: '709', name: '安南區', zipCode: '709', villages: ['安順里', '安西里'] },
    ],
  },
  {
    code: '800', name: '高雄市',
    districts: [
      { code: '800', name: '新興區', zipCode: '800', villages: ['大明里', '信義里'] },
      { code: '801', name: '前金區', zipCode: '801', villages: ['文化里', '社內里'] },
      { code: '802', name: '苓雅區', zipCode: '802', villages: ['苓雅里', '建軍里'] },
      { code: '804', name: '鼓山區', zipCode: '804', villages: ['鼓山里', '壽山里'] },
      { code: '806', name: '前鎮區', zipCode: '806', villages: ['前鎮里', '忠誠里'] },
      { code: '807', name: '三民區', zipCode: '807', villages: ['三民里', '十全里'] },
      { code: '830', name: '鳳山區', zipCode: '830', villages: ['鳳山里', '中山里'] },
    ],
  },
  {
    code: '220', name: '新北市',
    districts: [
      { code: '220', name: '板橋區', zipCode: '220', villages: ['板橋里', '光復里'] },
      { code: '221', name: '汐止區', zipCode: '221', villages: ['汐止里', '長安里'] },
      { code: '231', name: '新店區', zipCode: '231', villages: ['新店里', '安康里'] },
      { code: '234', name: '永和區', zipCode: '234', villages: ['永和里', '光復里'] },
      { code: '235', name: '中和區', zipCode: '235', villages: ['中和里', '復興里'] },
      { code: '241', name: '三重區', zipCode: '241', villages: ['三重里', '大同里'] },
      { code: '242', name: '新莊區', zipCode: '242', villages: ['新莊里', '立功里'] },
      { code: '247', name: '蘆洲區', zipCode: '247', villages: ['蘆洲里', '正義里'] },
      { code: '251', name: '淡水區', zipCode: '251', villages: ['淡水里', '竹圍里'] },
    ],
  },
  {
    code: '320', name: '桃園市',
    districts: [
      { code: '320', name: '中壢區', zipCode: '320', villages: ['中壢里', '興國里'] },
      { code: '330', name: '桃園區', zipCode: '330', villages: ['桃園里', '中山里'] },
      { code: '333', name: '龜山區', zipCode: '333', villages: ['龜山里', '嶺頂里'] },
      { code: '334', name: '八德區', zipCode: '334', villages: ['八德里', '大安里'] },
      { code: '338', name: '蘆竹區', zipCode: '338', villages: ['蘆竹里', '南崁里'] },
    ],
  },
]
